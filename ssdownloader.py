#! /usr/bin/env python3

import sys, re
from urllib import request
from xml.dom.minidom import parseString

class Manager:
    def __init__(self, jnlp):
        file = open(jnlp)
        data = file.read()
        file.close()
        print(data)
        dom = parseString(data)
        self.order = Order(re.sub(r'</?argument>', '', dom.getElementsByTagName('argument')[0].toxml()))

class Order:
    def __init__(self, url):
        self.url = url
        file = request.urlopen(self.url)
        data = file.read()
        file.close()
        dom = parseString(data)
        self.settings = Settings(
            re.sub(r'</?type>', '', dom.getElementsByTagName('type')[0].toxml()),
            re.sub(r'</?maxconnections>', '', dom.getElementsByTagName('maxconnections')[0].toxml()),
            re.sub(r'</?retry>', '', dom.getElementsByTagName('retry')[0].toxml()),
            re.sub(r'</?resume>', '', dom.getElementsByTagName('resume')[0].toxml()),
            re.sub(r'</?image>', '', dom.getElementsByTagName('image')[0].toxml()),
            re.sub(r'</?title>', '', dom.getElementsByTagName('title')[0].toxml()),
            re.sub(r'</?artist>', '', dom.getElementsByTagName('artist')[0].toxml()),
            re.sub(r'</?date>', '', dom.getElementsByTagName('date')[0].toxml()),
        )
        self.parseFile()

    def parseFile(self):
        file = request.urlopen(self.url)
        data = file.read()
        file.close()
        dom = parseString(data)
        self.downloads = []
        for node in dom.getElementsByTagName('download'):
            self.downloads.append(
                Download(
                    re.sub(r'</?tracknum>', '', parseString(node.toxml()).getElementsByTagName('tracknum')[0].toxml()),
                    re.sub(r'</?title>', '', parseString(node.toxml()).getElementsByTagName('title')[0].toxml()),
                    re.sub(r'</?url>', '', parseString(node.toxml()).getElementsByTagName('url')[0].toxml()),
                    re.sub(r'</?filesize>', '', parseString(node.toxml()).getElementsByTagName('filesize')[0].toxml()),
                    re.sub(r'</?filename>', '', parseString(node.toxml()).getElementsByTagName('filename')[0].toxml())
                )
            )

class Settings:
    def __init__(self, type, maxconnections, retry, resume, image, title, artist, date):
        self.type = type
        self.maxconnections = maxconnections
        self.retry = retry
        self.resume = resume
        self.image = image
        self.title = title
        self.artist = artist
        self.date = date

class Download:
    def __init__(self, tracknum, title, url, filesize, filename):
        self.tracknum = tracknum
        self.title = title
        self.url = url
        self.filesize = filesize
        self.filename = filename

    def download(self, destination):
        download = request.urlopen(self.url)
        output = open(destination + '/' + self.filename, 'wb')
        output.write(download.read())
        output.close()

def main(argv=None):
    if argv is None:
        argv = sys.argv
    if len(argv) < 3:
        print('NAME')
        print('    ssdownloader - Short for Simon & Schuster Downloader')
        print('')
        print('SYNOPSIS')
        print('    ssdownloader [jnlp-file] [save-location]')
        print('')
        print('DESCRIPTION')
        print('    A simple tool to download your purchases from Simon & Scheuster, bypassing their Java applet.')
        print('')
        print('    jnlp-file')
        print('        The location of the jnlp file.')
        print('')
        print('    save-location')
        print('        Local directory to save the files.')
        print('')
        print('AUTHOR')
        print('    Jack David Baucum <maxolasersquad@gmail.com>')
        print('    http://maxolasersquad.blogspot.com')
        print('')
        print('COPYRIGHT')
        print('    License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.')
        print('    This is free software: you are free to change and redistribute it.  There is NO WARRANTY, to the extent permitted by law.')
    else:
        manager = Manager(argv[1])
        for download in manager.order.downloads:
            print('Saving ' + download.filename)
            download.download(argv[2])

if __name__ == "__main__":
    sys.exit(main())
