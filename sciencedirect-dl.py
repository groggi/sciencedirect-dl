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
import argparse
from BeautifulSoup import BeautifulSoup

def downloadBook(url, outFilePath):
    userAgent = 'Mozilla/5 (Windows) Gecko'
    headers = {'User-Agent': userAgent}
    counter = 0
         
    # get page
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
        print("Downloading PDF %s of %s" % (len(localPdfFiles) + 1,
            len(pdfUrlList)))
        fileRequest = urllib2.Request(pdfUrl, headers=headers)
        file = urllib2.urlopen(fileRequest)
        localFile = tempfile.NamedTemporaryFile(delete=False)
        localPdfFiles.append(localFile.name)
        localFile.write(file.read())
        localFile.close()
    
    # merge PDFs
    print("Merging downloaded PDF files to: %s" % (outFilePath))
    command = ["pdftk"]
    command.extend(localPdfFiles)
    command.extend(["cat", "output", outFilePath])
    subprocess.Popen(command, shell=False).wait()
    
    # clean up temp files
    print("Cleaning up temporary files")
    for localFile in localPdfFiles:
        os.remove(localFile)
    
    print("Done.")
    
if __name__ == '__main__':
    # argument parser setup
    argparser = argparse.ArgumentParser(
        description='Download Script for www.sciencedirect.com')
    
    argparser.add_argument('url', action="store",
        help="URL to the specific Book to download")
    
    argparser.add_argument('output', action="store",
        help="Filepath to save the output to (PDF)")
    
    args = argparser.parse_args()
    
    downloadBook(args.url, args.output)
