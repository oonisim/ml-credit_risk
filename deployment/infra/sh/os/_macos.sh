check_docker_desktop_cli() {
    echo "Checking Docker Desktop CLI support on macOS..."

    # Check if Docker CLI is installed
    if ! command -v docker >/dev/null 2>&1; then
        echo "Docker CLI not found"
        echo "Install Docker Desktop from: https://docs.docker.com/desktop/mac/install/"
        return 1
    fi
    echo "Docker CLI found: $(which docker)"

    # Check if docker desktop command exists
    echo "Testing 'docker desktop' command..."
    if docker desktop --help >/dev/null 2>&1; then
        echo "'docker desktop' command is available"

        if docker info >/dev/null 2>&1; then
            echo "Docker daemon and desktop is already running"
            return 0
        fi

        # Try to start Docker Desktop
        echo "Attempting to start Docker Desktop..."
        if docker desktop start; then
            echo "'docker desktop start' command executed successfully"
            echo "Waiting for Docker to be ready..."
            local counter=0
            while [ $counter -lt 60 ]; do
                if docker info >/dev/null 2>&1; then
                    echo "Docker Desktop started successfully after ${counter} seconds"
                    return 0
                fi
                sleep 2
                counter=$((counter + 2))
            done
            echo "Docker not responding after 60 seconds"
            return 1
        else
            echo "'docker desktop start' failed"
            return 1
        fi
    else
        echo "'docker desktop' command not available. Install docker desktop for MacOS"
        return 1
    fi
}

if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Installing get text, OpenMP, cmake, apache arrow C++ lib, and PostgreSQL client..."
    brew install gettext libomp libpq cmake apache-arrow && brew link --force gettext

    echo
    echo "Setting PATH environment variable for PostgreSQL client..."
    if [[ ":$PATH:" != *":/opt/homebrew/opt/libpq/bin:"* ]]; then
       echo 'export PATH="/opt/homebrew/opt/libpq/bin:$PATH"' >> ~/.bash_profile
       export PATH="/opt/homebrew/opt/libpq/bin:$PATH"
       echo "Added /opt/homebrew/opt/libpq/bin to PATH"
    else
       echo "/opt/homebrew/opt/libpq/bin is already in PATH"
    fi

    echo
    echo "Setting PATH environment variable for PostgreSQL client..."

    # To install psycopg2-binary on Apple silicon
    # https://github.com/psycopg/psycopg2/issues/1434
    # ```
    # export LDFLAGS="-L$(brew --prefix openssl)/lib"
    # export CPPFLAGS="-I$(brew --prefix openssl)/include"
    # ```
    echo
    echo "Checking openssl as the requirement for psycopg2..."
    if ! brew list openssl &>/dev/null; then
        echo "OpenSSL not found via Homebrew. Installing..."
        brew install openssl && brew link openssl
    else
        echo "OpenSSL is already installed via Homebrew"
    fi

    echo
    check_docker_desktop_cli
fi
