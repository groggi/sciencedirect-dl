'''
            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                    Version 2, December 2004

 Copyright (C) 2012 Gregor Wegberg <code@wegberg.ch>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.
'''

import urllib
import urllib2
import string
import sys
import tempfile
import os
import subprocess
from BeautifulSoup import BeautifulSoup

def main():
    url = ""
    
    if(len(sys.argv) != 2):
        print("Please provide an URL")
        return
    else:
        url = sys.argv[1]
        
    # get page
    userAgent = 'Mozilla/5 (Windows) Gecko'
    headers = {'User-Agent': userAgent}
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    
    page = response.read()
    soup = BeautifulSoup(page)
    
    # extract list of PDFs
    pdfTags = soup.findAll('a', target='newPdfWin')
    pdfUrlList = []
    for result in pdfTags:
        pdfUrlList.append(result['href'])
        
    # download PDFs
    localPdfFiles = []
    for pdfUrl in pdfUrlList:
        print("Downloading: %s" % (pdfUrl))
        fileRequest = urllib2.Request(pdfUrl, headers=headers)
        file = urllib2.urlopen(fileRequest)
        localFile = tempfile.NamedTemporaryFile(delete=False)
        localPdfFiles.append(localFile.name)
        localFile.write(file.read())
        localFile.close()
    
    # merge PDFs
    command = ["pdftk"]
    command.extend(localPdfFiles)
    command.extend(["cat", "output", "out.pdf"])
    subprocess.Popen(command, shell=False).wait()
    
    # clean up temp files
    for localFile in localPdfFiles:
        os.remove(localFile)
    
    
if __name__ == '__main__':
    main()