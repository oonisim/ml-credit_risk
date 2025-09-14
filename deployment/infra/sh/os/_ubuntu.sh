if [[ "$(uname -s)" == "Linux" && -r /etc/os-release ]]; then
  distro=$(. /etc/os-release && echo "$ID")
  case "$distro" in
    ubuntu|debian)
      echo "Installing ${distro} Python and PostgreSQL client..."
      sudo apt-get update && sudo apt-get install -y \
        python3.11 python3.11-dev python3.11-venv \
        python3-pip build-essential libssl-dev libffi-dev \
        postgresql-client libpq-dev
      sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
      ;;
    *)
      # No-op for other distros
      ;;
  esac
fi
