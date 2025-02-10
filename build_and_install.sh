#!/bin/bash
# Build executable
[ -e build ] && rm -r build
[ -e dist ] && rm -r dist
[ -e Main2.spec ] && rm Main2.spec
[ -e Main2.rpm ] && rm Main2.rpm
pyinstaller --onefile -n "Main2EXECUTABLE" --add-data="users.db:." --add-data="finestra.ui:." -w main.py

# Create folders
[ -e pkg ] && rm -r pkg
mkdir -p pkg/opt/main2
mkdir -p pkg/usr/share/applications
mkdir -p pkg/usr/share/icons/hicolor/scalable/apps

# Copy files
cp -r "dist/Main2" "pkg/opt/main2"
cp -f main2.desktop pkg/usr/share/applications

# Change permissions
sudo find "pkg/opt/main2/Main2" -type f -exec chmod 755 -- {} +
sudo find pkg/usr/share -type f -exec chmod 644 -- {} +

# Create package
fpm -C pkg -s dir -t rpm -n "mainLinux" -v 0.0.1 -p Main2.rpm

# Install package
sudo apt remove mainLinux
sudo apt install ./Main2.rpm
