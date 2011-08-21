#!/usr/bin/python2.6
# @author: allenm, oldj
#
# @link: https://github.com/allenm/js-css-compressor
#

import httplib
import urllib
import sys
import os
import re


def analyFile(filename):
    ''' analy the file content , judge use which kind compressor.
    if the file has 'ImportJavscirpt.url' keyword ,use the compress merge file method, else use compress single file method'''

    if not os.path.isfile(filename):
        print 'Error: "%s" is not a valid file!' % filename
        return False
        
    p = re.compile('ImportJavscript\.url')
    content = open(filename).read()
    if p.search(content):
        compressMergeFile(filename)
    else:
        compressSingleFile(filename)

    

def compressMergeFile(filename):
    ''' analy the merge file, compress the file which inclube by the merge file and the filename have not the 'min' keyword'''
    f = open(filename)
    while True:
        line = f.readline()
        if not line: break
        handleMergeLine(line,filename)
    f.close

def handleMergeLine(line,filename):
    ''' analy one line of merge file, if It's a effective import line , then judge the file should be compress or not! '''
    p = re.compile('ImportJavscript\.url\([\'\"]http://style.china.alibaba.com/js/(.*[^(?:min)]\.js)[\'\"]\)')
    m = p.search(line)
    if m:
        localFile = findLocalFile(m.group(1),filename)
        if localFile:
            showCompress = raw_input('('+m.group(1)+') Is this file should be compress? (y/n)')
            if showCompress is 'y':
                compressSingleFile(localFile)



def findLocalFile(url,filename):
    ''' find local file by the url and the origin filename '''
    absPath = os.path.abspath(filename)
    p = re.compile('^(.*/js/).*')
    m = p.search(absPath)
    if m:
        localFile = m.group(1)+os.sep.join(url.split('/'))
        return localFile
    else:
        print "find local file failure, check you style directory , is it a common style of alicn structure"
        return False


def compressSingleFile(filename):
    if not os.path.isfile(filename):
        print 'Error: "%s" is not a valid file!' % filename
        return False

    content = unicode(open(filename).read(),'gbk').encode('utf8')

    output = compressor(content)

    savename = filename.replace('.js','-min.js')

    # print info
    print 'DATA:'
    print '-' * 50
    print output.rstrip()
    print '-' * 50
    print '>> output: %s (%.2fK)' % (savename, len(output) / 1024.0)


    donefile = open(savename, 'w')
    donefile.write(output)
    donefile.close()


# Define the parameters for the POST request and encode them in
# a URL-safe format.
def compressor(jscode):
    ''' compressor the javascript code use the google closure REST API '''

    code = [
            ('js_code',jscode),
            ('compilation_level', 'WHITESPACE_ONLY'),
            ('output_format', 'text'),
            ('output_info', 'compiled_code'),
        ]

    params = urllib.urlencode(code)

    # Always use the following value for the Content-type header.
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    conn = httplib.HTTPConnection('api.allenm.me')
    conn.request('POST', '/closure/compile', params, headers)
    response = conn.getresponse()
    #data = unicode(response.read()).encode('gbk')
    data = response.read()
    conn.close()

    return data


if __name__ == "__main__":

    if sys.argv.__len__() >= 2:
        analyFile(sys.argv[1])
    else:
        print '''This script must contain at least one parameter.
        the first parameter is the the script filename which you want compress
        '''
