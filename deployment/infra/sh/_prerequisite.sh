#!/usr/bin/env bash
#--------------------------------------------------------------------------------
# Verify or setup prerequisite to deploy the FEAST tutorial with PostgreSQL,
# - POSTGRES_PASSWORD environment variable for the postgres admin user.
# - PostgreSQL client to rum psql.
#--------------------------------------------------------------------------------

echo "--------------------------------------------------------------------------------"
echo "Setting up OS prerequisite..."
echo "--------------------------------------------------------------------------------"
case "${OSTYPE}" in
  linux-gnu*)
    if [[ "$(uname -s)" == "Linux" && -r /etc/os-release ]]; then
      # Read distro ID (like "ubuntu", "debian", "rhel", "centos", "fedora", "amzn")
      distro=$(. /etc/os-release && echo "$ID")

      case "${distro}" in
        ubuntu|debian)
          echo "Detected Debian-based distro: ${distro}."
          . os/_ubuntu.sh
          ;;

        rhel|centos|fedora|amzn)
          echo "Detected RHEL-based distro: ${distro}."
          . os/_redhat.sh
          ;;

        *)
          echo "Unsupported Linux distro: ${distro}." >&2
          exit 1
          ;;
      esac
    fi
    ;;
  darwin*)
    echo "Detected MacOS ${distro}"
    . os/_macos.sh
    ;;
  *)
    echo "$OSTYPE is not supported."
    exit 1
    ;;
esac

if [[ -z "${POSTGRES_PASSWORD}" ]]; then
  echo
  echo "--------------------------------------------------------------------------------"
  echo "Setting up administrative prerequisite..."
  echo "--------------------------------------------------------------------------------"
  echo "Provide a new password for the Docker PostgreSQL administration."
  echo "Alternatively, set the environment variable POSTGRES_PASSWORD as" \
       "'export POSTGRES_PASSWORD=... before running this script."
  read -r -s -p "> " POSTGRES_PASSWORD
  echo
  if [[ -z "${POSTGRES_PASSWORD}" ]]; then
    echo "Error: POSTGRES_PASSWORD cannot be empty" >&2
    exit 1
  fi
  export "POSTGRES_PASSWORD=${POSTGRES_PASSWORD}"
  trap 'unset POSTGRES_PASSWORD' EXIT
fi


