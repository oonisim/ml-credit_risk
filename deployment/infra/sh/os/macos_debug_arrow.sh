#!/bin/bash
echo "=== Apache Arrow Debug Information ==="

# Check if Arrow is installed via Homebrew
if brew list apache-arrow >/dev/null 2>&1; then
    echo "✓ Arrow installed via Homebrew"
    ARROW_PREFIX="$(brew --prefix apache-arrow)"
    echo "  Location: $ARROW_PREFIX"

    # Check for CMake config files
    if [ -f "$ARROW_PREFIX/lib/cmake/Arrow/ArrowConfig.cmake" ]; then
        echo "✓ ArrowConfig.cmake found"
    else
        echo "✗ ArrowConfig.cmake NOT found"
        echo "  Expected at: $ARROW_PREFIX/lib/cmake/Arrow/ArrowConfig.cmake"
    fi
else
    echo "✗ Arrow not installed via Homebrew"
fi

# Check conda installation
if [ -n "$CONDA_PREFIX" ]; then
    echo "✓ Conda environment active: $CONDA_PREFIX"
    if [ -f "$CONDA_PREFIX/lib/cmake/Arrow/ArrowConfig.cmake" ]; then
        echo "✓ Arrow found in conda environment"
    else
        echo "✗ Arrow not found in conda environment"
    fi
else
    echo "ℹ No conda environment active"
fi

# Check system paths
echo "Searching for ArrowConfig.cmake in system paths:"
find /usr/local /opt/homebrew -name "ArrowConfig.cmake" 2>/dev/null || echo "Not found in system paths"

# Check pkg-config
if command -v pkg-config >/dev/null 2>&1; then
    if pkg-config --exists arrow; then
        echo "✓ Arrow found via pkg-config"
        echo "  Version: $(pkg-config --modversion arrow)"
        echo "  Libs: $(pkg-config --libs arrow)"
    else
        echo "✗ Arrow not found via pkg-config"
    fi
fi

# Environment variables
echo "Current CMAKE_PREFIX_PATH: ${CMAKE_PREFIX_PATH:-<not set>}"
echo "Current PKG_CONFIG_PATH: ${PKG_CONFIG_PATH:-<not set>}"
