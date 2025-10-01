# opnenssl on macOS required for psycopg2 and psycopg2-binary
if [[ "$OSTYPE" == "darwin"* ]]; then
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
