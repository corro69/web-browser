#!/bin/bash
mkdir /opt/dweb/
echo creating /opt/dweb/ directory
cp dweb.py /opt/dweb/
echo copying dweb.py to /opt/dweb/
cp read_bookmarks.py /opt/dweb/
echo copying read_bookmarks to /opt/dweb/
cp settings_read.py /opt/dweb
echo copying settings_read.py to /opt/dweb/
cp dweb_settings.py /opt/dweb
echo copying dweb_settings to /opt/dweb/
cp /images -r /opt/dweb/

echo creating .config files
mkdir .config/dweb
touch .config/dweb/dweb-settings.ini
touch .config/dweb/bookmarks.dat
echo installation completed
