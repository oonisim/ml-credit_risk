# https://www.tug.org/mactex/beginners.html
# To avoid ! LaTeX Error: File `tcolorbox.sty' not found. error.
# https://stackoverflow.com/a/59851436

# Setup proxy first and verify the connection.
# https://tex.stackexchange.com/a/521842
sudo -E brew install --cask mactex
sudo -E brew install --cask basictex

# https://tex.stackexchange.com/a/147090
tlmgr init-usertree

# You'll need to install additional packages as needed
# sudo tlmgr update --self
tlmgr install tcolorbox
tlmgr install pgf
tlmgr install xcolor
tlmgr install collection-fontsrecommended
tlmgr install collection-latexextra

