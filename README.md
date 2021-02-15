# The-Watcher-Discord-Bot
A Discord Watcher bot for the game Rust.
Yes i play the game Rust by Facepunch and i want to keep track of players who login and log out and how long they played for, so i created a discord bot to do this for me.

I have this Bot running on a Raspberry pi4 with DietPi Operating system so it runs 24/7.

Note: this can work for other games too just i only care about Rust ;-)

## Prerequisites for this project to work:

You need python 3.7 or higher to run this project.

py -3 -m pip install -U discord.py

py -3 -m pip install -U requests

py -3 -m pip install -U beautifulsoup4

## To start a terminal in DietPi
xterm -e python3.7 /root/Desktop/The-Watcher-Discord-Bot/main.py

## To have the Discord Bot launch on login to the DietPi Desktop

1. /root
2. right click and show hidden files
3. go in to the .config folder
4. then in the autostart folder
5. make a file (myfile.desktop)
6. in the file put the following

[Desktop Entry]
Encoding=UTF-8
Type=Application
Name=<GUI Controller>
Comment=
Exec= python3.7 /root/Desktop/The-Watcher-Discord-Bot/main.py
StartupNotify=false
Terminal=true
Hidden=false

The above code will launch the python files in a visible terminal window.
Obviously i put my files on the desktop so you should do the same or choose your own location.

## In the Setup Folder enter in your setup, there is an explaination on how to set it up too.

I will update with pictures later on so that you can see what the bot does.

Philip M



