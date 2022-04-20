# PWNServer
This is an idea I got from [IPPSEC](https://ippsec.rocks) which was to spin up a webserver with some useful tools at the beginning of CTF or job even because you know you'll probably need one. This one kind of got of hand, or maybe its just super useful, either way it does provide tools that I find handy in most jobs.

Currently **PWNServer** is focused on Linux targets. I will add Windows stuff at a later date.

## Requirements

This should work on just about any Linux system. It was developed on Python 3.9.12. It should run on earlier versions, but I haven't tested it on any.

## Installation

Get the code from github:
```
git clone https://github.com/kdirectorate/pwnserver.git
cd pwnserver
```
I highly recommend you create a virtual environment for this app. It is very easy to do:
```
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cp config.py.example config.py
```
*config.py* contains your configuration settings and won't be overwritten if you update your copy of **PWNServer**. You should look it over to make sure it is acceptable to you. Especially the 1st few options:
```
USERNAME
APPNAME
WEBSERVERPORT
LPORT
SERVERPATH
```
However, everything should work out of the box.

## Usage

To start the server run the setup.py program:

```
. .venv/bin/activate
./setup.py [YOURPUBLICIP]
```
By default this will do the following things:

1. Delete (if necessary) and create the "/tmp/PWNServer" directory (TEMPDIR); and
2. Copy all the files in the "html" directory to "(TEMPDIR)/html"; and
3. Copy a variety of Linux privesc tools from their repositories to "(TEMPDIR)/html/bin" and create a tarball of them; and
4. Generate a bunch of reverse shell scripts using [YOURPUBLICIP] and *LPORT* from **config.py** and put them in "(TEMPDIR)/html/shells" (see shells.src); and
5. Generate a one-off SSH key into "(TEMPDIR)/html/sshkey[& .pub]" and add it to your active keys via *ssh-add*; and
6. Display a list of common commands you may need so you can just copy/paste instead of typing them; and
7. Startup a web server serving files in the "(TEMPDIR)/html" directory.

You can take the webserver down by sending it the URI "/QUIT" remotely, or of course just **CTRL-C**. When you get back to pwning things you can skip most of the steps and just run the webserver via:
```
./setup.py -w [YOURPUBLICIP]
```
Don't worry, if  your IP has changed this will regenerate the reverse shell scripts. Mostly it just won't redownload all the tools from step 3. The full list of options is:
```
usage: Eb13l-Webserver [-h] [-w] [-p P] [-l L] ip

Setup Attacker webserver with the usual naughty tools.

positional arguments:
  ip          IP of our attacking box.

optional arguments:
  -h, --help  show this help message and exit
  -w          Start webserver only.
  -p P        Webserver port.
  -l L        Shell catcher port.

Be ethically naughty.
```

## Maintenance
I recommend you fork this project so that you can then store your custom **config.py** file in github. You may want to periodically check config.py.example to make sure any changes made to the list of packages to download get replicated to your config.py. 

# How it should look
![screenshot](screenshot.png)
