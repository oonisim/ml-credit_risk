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
