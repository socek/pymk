import os
import shutil
import urllib2
import urlparse
from zipfile import ZipFile


# this code is from
# http://stackoverflow.com/questions/862173/how-to-download-a-file-using-python-in-a-smarter-way
def download(url, fileName=None):
    def getFileName(url, openUrl):
        if 'Content-Disposition' in openUrl.info():
            # If the response has Content-Disposition, try to get filename from
            # it
            cd = dict(map(
                lambda x: x.strip().split(
                    '=') if '=' in x else (x.strip(), ''),
                openUrl.info()['Content-Disposition'].split(';')))
            if 'filename' in cd:
                filename = cd['filename'].strip("\"'")
                if filename:
                    return filename
        # if no filename was found above, parse it out of the final URL.
        return os.path.basename(urlparse.urlsplit(openUrl.url)[2])

    r = urllib2.urlopen(urllib2.Request(url))
    try:
        fileName = fileName or getFileName(url, r)
        with open(fileName, 'wb') as f:
            shutil.copyfileobj(r, f)
    finally:
        r.close()

# end of external code


def extract_egg(source_path, destination_path):
    zipfile = ZipFile(source_path)
    zipfile.extractall(destination_path)
    zipfile.close()
    os.unlink(source_path)
