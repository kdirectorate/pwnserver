#!/bin/env python3 

import shutil
import requests
from apputil import *
from config import *

def main(fullpath):

    def webcopy(url):
        prjname = url.split("/")[-1]
        with log.progress(f"Copying {prjname}") as p:
            r = requests.get(url)
            with open(f"{fullpath}/{prjname}","wb") as f: 
                totalbits = 0
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        totalbits += 1024
                        p.status(str(totalbits*1025) + "KB...")
                        f.write(chunk)
                
    # def gitclone(pkg):
    #     prjname = pkg.split("/")[-1]
    #     with log.progress(f"Cloning {prjname}") as p:
    #         Repo.clone_from(f"{pkg}",f"{OUTDIR}/{prjname}")

    with log.progress("Staging tools: ") as p:
        log.info(f"Output path: {fullpath}")

        # for pkg,fname in git_packages:
        #     gitclone(pkg)
        for url in linux_web_files:
            webcopy(url)

        with log.progress(f"Making tarball linprivesc.tgz") as p:
            os.system(f"tar -zcf {fullpath}/../linprivesc.tgz {fullpath}/*")

if __name__ == "__main__":

    def usage():
        sys.stderr.write(
            "usage: %s OURIP OURPORT\n" % sys.argv[0]
        )
        sys.exit(1)

    if len(sys.argv) < 3:
        usage()

    OURIP = sys.argv[1]
    OURPORT = sys.argv[2]

    main(OURIP,OURPORT)
