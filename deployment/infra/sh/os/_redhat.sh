if [[ "$(uname -s)" == "Linux" && -r /etc/os-release ]]; then
  distro=$(sed -n 's/^NAME="\([^"]*\)"/\1/p' /etc/os-release)
  case "$distro" in
    rhel|centos|fedora|amzn)
      echo "Installing ${distro} Python and PostgreSQL client..."
      sudo dnf update -y && sudo dnf install -y \
        python3.11 python3.11-pip python3.11-devel \
        postgresql-devel

      # Some RHEL distros use "alternatives" instead of update-alternatives
      if command -v alternatives >/dev/null 2>&1; then
        sudo alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
      fi
      ;;

    *)
      ;;
  esac
fi


start_docker_engine_rhel() {
    echo "🚀 Starting Docker Engine on RHEL..."
    if docker info >/dev/null 2>&1; then
        echo "✅ Docker Engine is already running"
        return 0
    fi

    if ! command -v docker >/dev/null 2>&1; then
        echo "Docker Engine not installed. Install Docker."
        return 1
    fi
    if ! systemctl list-unit-files | grep -q docker.service; then
        echo "Docker service not found. Docker Engine may not be properly installed"
        return 1
    fi

    echo "Starting Docker Engine service..."
    if sudo systemctl start docker; then
        echo "⏳ Waiting for Docker daemon to be ready..."
        local counter=0
        while [ $counter -lt 30 ]; do
            if docker info >/dev/null 2>&1; then
                echo "Docker Engine is ready after ${counter} seconds"
                if ! systemctl is-enabled --quiet docker; then
                    echo "🔧 Enabling Docker auto-start..."
                    sudo systemctl enable docker
                    echo "Docker will now start automatically on boot"
                fi

                return 0
            fi
            printf "."
            sleep 1
            counter=$((counter + 1))
        done

        echo ""
        echo "Docker daemon not responding after 30 seconds"
        echo "Checking Docker service status:"
        sudo systemctl status docker --no-pager -l
        return 1

    else
        echo "Failed to start Docker service"
        echo "Docker service status:"
        sudo systemctl status docker --no-pager -l

        echo ""
        echo "📋 Docker service logs (last 20 lines):"
        sudo journalctl -u docker --no-pager -l -n 20
        return 1
    fi
}

check_docker_engine_rhel() {
    echo "🔍 Checking Docker Engine on RHEL..."
    if ! command -v docker >/dev/null 2>&1; then
        echo "Docker Engine not installed. Install Docker."
        return 1
    fi

    if docker info >/dev/null 2>&1; then
        echo "✅ Docker Engine daemon is running"
        docker system info --format "Server Version: {{.ServerVersion}}"
        docker system info --format "Storage Driver: {{.Driver}}"
        docker system info --format "Cgroup Driver: {{.CgroupDriver}}"
        docker system info --format "Operating System: {{.OperatingSystem}}"
        docker system info --format "Architecture: {{.Architecture}}"

    else
        echo "Docker Engine daemon is not running"
        echo ""
        start_docker_engine_rhel
    fi

    # Check Docker service status
    echo ""
    echo "🔧 Docker Service Status:"
    if systemctl is-active --quiet docker; then
        echo "✅ Docker service is active"
        if systemctl is-enabled --quiet docker; then
            echo "✅ Docker service is enabled (auto-start)"
        else
            echo "⚠️  Docker service is not enabled for auto-start"
            echo "💡 Enable with: sudo systemctl enable docker"
        fi
    else
        echo "❌ Docker service is not active"
        echo "💡 Start with: sudo systemctl start docker"
    fi

    # Check user permissions
    echo ""
    echo "👤 Docker User Permissions:"
    if groups "$USER" | grep -q docker; then
        echo "✅ User '$USER' is in docker group"
    else
        echo "⚠️  User '$USER' is NOT in docker group"
        echo "💡 Add user to docker group:"
        echo "   sudo usermod -aG docker $USER"
        echo "   # Then log out and back in"
    fi

    return 0
}

check_docker_engine_rhel