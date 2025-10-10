check_macos_libpq() {
    local libpq_path="/opt/homebrew/opt/libpq/bin"
    local export_line="export PATH=\"$libpq_path:\$PATH\""

    if [[ ":$PATH:" != *":$libpq_path:"* ]]; then
        # Add to bash profile if not already there
        if ! grep -Fxq "$export_line" ~/.bash_profile 2>/dev/null; then
            echo "$export_line" >> ~/.bash_profile
            echo "Added '${export_line}' to ~/.bash_profile"
        fi

        # Add to zsh profile if not already there
        if ! grep -Fxq "$export_line" ~/.zshrc 2>/dev/null; then
            echo "$export_line" >> ~/.zshrc
            echo "Added '${export_line}' to ~/.zshrc"
        fi

        # Export for current session
        export PATH="$libpq_path:$PATH"
        echo "Added $libpq_path to PATH for current session"
    fi

    # Verify psql is now available
    if command -v psql >/dev/null 2>&1; then
        echo "psql $(psql --version) is now available: $(which psql)"
    else
        echo "Error: psql is not available."
        exit 1
    fi

}


if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Verifying the psql availability..."
    check_macos_libpq

    echo
    echo "Verifying opnenssl on macOS required for psycopg2 and psycopg2-binary..."
    OPENSSL_PATH=$(brew --prefix openssl 2>/dev/null ||
                  brew --prefix openssl@1.1 2>/dev/null ||
                  brew --prefix openssl@3 2>/dev/null)

    if [[ -n "$OPENSSL_PATH" && -d "$OPENSSL_PATH" ]]; then
        echo "OpenSSL found at: $OPENSSL_PATH"
    else
        echo "OpenSSL not found. Installing..."
        brew install openssl
        OPENSSL_PATH=$(brew --prefix openssl 2>/dev/null ||
                      brew --prefix openssl@1.1 2>/dev/null ||
                      brew --prefix openssl@3 2>/dev/null)
    fi

    export LDFLAGS="-L$OPENSSL_PATH/lib"
    export CPPFLAGS="-I$OPENSSL_PATH/include"
fi
