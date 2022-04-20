from pwn import *
import http.server
from functools import partial
from httpserver import ServeDirectoryWithHTTP
from http import HTTPStatus
from time import sleep
import urllib3
from rich import pretty, print
from rich.console import Console

pretty.install()
urllib3.disable_warnings()

lasturi = ""

def PwnServeDirectoryWithHTTP(hostname="0.0.0.0",directory=".",port=80):
    """
    Serves up files from the current directory, tracks the last URI
    requested and logs messages to pwntools. Does this in a separate 
    thread.
    """

    class HTTPHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self) -> None:
            global lasturi
            lasturi = self.path
            if lasturi == "/FINISHED":
                self.send_response(HTTPStatus.OK)
                self.copyfile(BytesIO(b"Hack the planet!"), self.wfile)
                return
            return super().do_GET()

        def log_message(self, format, *args):
            log.info(format, *args)
            
    handler = partial(HTTPHandler, directory=directory)
    return ServeDirectoryWithHTTP(directory=directory,hostname=hostname, port=port, handler=handler, logger=_logger)

def getLastURI():
    """
    Returns the last URI serviced by the HTTP server.
    """
    return lasturi

def _logger(format, *args):
    log.info(format + " ".join(map(str, args)))

