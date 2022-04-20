#!/bin/env python3 

import argparse
from distutils.dir_util import mkpath
from apputil import *
from config import *

SCRIPTSDIR = "shells.src"

def main(outputdir,ip,port=9000):
    with log.progress("Make shells") as p:
        mkpath(outputdir)
        port = str(port)
        scripts = os.listdir("{}/".format(SCRIPTSDIR))
        for script in scripts:
            contents = open("{}/{}".format(SCRIPTSDIR,script),"r").read()
            contents = contents.replace("${SHELLCATCHER}", ip)
            contents = contents.replace("${SHELLPORT}", port)
            with open("{}/{}".format(outputdir,script),"w") as news:
                news.write(contents)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="IP catching shells")
    parser.add_argument("port", help="port catching shells")

    args = parser.parse_args()
    main(args.ip,args.port)
