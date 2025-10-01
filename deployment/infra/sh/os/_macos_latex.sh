#!/usr/bin/env bash
# https://www.tug.org/mactex/beginners.html
# To avoid ! LaTeX Error: File `tcolorbox.sty' not found. error.
# https://stackoverflow.com/a/59851436

# Setup proxy first and verify the connection.
# GODEBUG=netdns=go alpaca -C "http://pac.internal.cba/cba.pac" -u ${USER} -d ${DOMAIN}
export http_proxy='http://localhost:3128'
export https_proxy='http://localhost:3128'
curl -I https://www.google.com

# https://tex.stackexchange.com/a/521842
# sudo -E brew install --cask mactex
sudo -E brew install --cask basictex

# Set the TeX Live package repository to a CTAN mirror
sudo tlmgr repository set http://mirror.ctan.org/systems/texlive/tlnet
sudo -E sodo tlmgr update --all --self

# https://tex.stackexchange.com/a/147090
tlmgr init-usertree

# You'll need to install additional packages as needed
tlmgr install tcolorbox
tlmgr install pgf
tlmgr install xcolor
tlmgr install collection-fontsrecommended
tlmgr install collection-latexextra
tlmgr install underscore
