#!/usr/bin/env bash
#--------------------------------------------------------------------------------
# Install Python dependency packages for the tutorial.
#--------------------------------------------------------------------------------
set -eo pipefail
DIR="$(realpath "$(dirname "${0}")")"
cd "${DIR}" || exit 1

check_virtual_env() {
    # Check for conda or pip virtual environment has been activated for this session.
    if [[ -z "${VIRTUAL_ENV:-}" && -z "${CONDA_DEFAULT_ENV:-}" ]]; then
        echo "Please activate a virtual environment first (conda or pip)"
        return 1
    fi
    if [[ -n "${CONDA_DEFAULT_ENV:-}" ]]; then
        export VIRTUAL_ENV="${CONDA_PREFIX}"
    else
        export VIRTUAL_ENV="${VIRTUAL_ENV:?'Activate Virtual Environment First'}"
    fi
    echo "Virtual environment detected: ${VIRTUAL_ENV}"
    return 0
}

install_requirements() {
    # Install Python packages from requirements.txt
    if [[ ! -f "requirements.txt" ]]; then
        echo "Error: requirements.txt not found in current directory"
        return 1
    fi
    echo "Installing packages from requirements.txt"
    if pip install -r requirements.txt; then
        echo "Package installation completed successfully"
        return 0
    else
        echo "Package installation failed"
        return 1
    fi
}

echo
echo "--------------------------------------------------------------------------------"
echo "Start installing Python packages for the tutorial..."
echo "--------------------------------------------------------------------------------"
echo "Verifying the python virtual environment..."
check_virtual_env || exit 1

echo
echo "Setting up OS dependent requirement for Python package installations..."
case "${OSTYPE}" in
    linux-gnu*)
        if [[ "$(uname -s)" == "Linux" && -r /etc/os-release ]]; then
            distro=$(. /etc/os-release && echo "$ID")
            case "${distro}" in
                ubuntu|debian)
                    echo "Detected Debian-based distro: ${distro}."
                    if [[ -f "os/_ubuntu.sh" ]]; then
                        . os/_ubuntu.sh
                    else
                        echo "Warning: os/_ubuntu.sh not found, skipping OS setup"
                    fi
                    ;;
                rhel|centos|fedora|amzn)
                    echo "Detected RHEL-based distro: ${distro}."
                    if [[ -f "os/_redhat.sh" ]]; then
                        . os/_redhat.sh
                    else
                        echo "Warning: os/_redhat.sh not found, skipping OS setup"
                    fi
                    ;;
                *)
                    echo "Unsupported Linux distro: ${distro}." >&2
                    exit 1
                    ;;
            esac
        else
            echo "Cannot determine Linux distribution" >&2
            exit 1
        fi
        ;;
    darwin*)
        echo "Detected macOS"
        if [[ -f "os/_macos.sh" ]]; then
            . os/_macos.sh
        else
            echo "Warning: os/_macos.sh not found."
            exit 1
        fi
        ;;
    *)
        echo "${OSTYPE} is not supported."
        exit 1
        ;;
esac

echo
echo "Installing Python packages..."
install_requirements || exit 1
