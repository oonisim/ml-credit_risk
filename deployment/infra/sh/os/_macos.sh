# Install Mac OSX PostgreSQL client.
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Installing Mac OSX PostgreSQL client..."
    brew install libpq
    echo "Setting PATH environment varialbe for PostgreSQL client..."
   if [[ ":$PATH:" != *":/opt/homebrew/opt/libpq/bin:"* ]]; then
       echo 'export PATH="/opt/homebrew/opt/libpq/bin:$PATH"' >> ~/.bash_profile
       export PATH="/opt/homebrew/opt/libpq/bin:$PATH"
       echo "Added /opt/homebrew/opt/libpq/bin to PATH"
   else
       echo "/opt/homebrew/opt/libpq/bin is already in PATH"
   fi
fi
