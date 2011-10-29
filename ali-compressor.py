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

class CompressJs:
    """ compress single js file, or supply a js merge file ,then find the files which should be compress , compress one by one , and 
    replace the filename in merge file to the compressed filename """

    def __init__(self, uInput):
        self.uInput = uInput
        if self.isMergeFile():
            self.handleMergeFile()
        else:
            self.compressSingleFile(self.uInput)

    def isMergeFile(self):
        ''' judge the user input is a merge file or not , the judge rule is find the "ImportJavscript.url" keyword '''
        if not os.path.isfile(self.uInput):
            print 'Error: "%s" is not a valid file!' % self.uInput 
            raise Exception(' the file you input is not a valid file')

        p = re.compile('ImportJavscript\.url')
        content = open(self.uInput).read()
        if p.search(content):
            return True
        else:
            return False

    def handleMergeFile(self):
        ''' analy the merge file, compress the file which inclube by the merge file and the filename have not the 'min' keyword'''

        p = re.compile('ImportJavscript\.url\([\'\"]http://.*/js/(.*(?<!(?:min))+\.js)[\'\"]\)')
        f = open(self.uInput)
        shouldCompress = []
        lineNos = []
        lineNo = 0
        for line in f.readlines():
            m = p.search(line)
            if m :
                filepath = self.findLocalFile(m.group(1))
                needCompress = raw_input('('+m.group(1)+') Is this file should be compressed? (y/n)')
                if needCompress is 'y' or needCompress is 'Y' :
                    shouldCompress.append(filepath)
                    lineNos.append(lineNo)
            lineNo += 1
        
        self.shouldCompress = shouldCompress
        self.lineNos = lineNos
        self.compress1by1()
        self.modifyMergeFile()


    def findLocalFile(self,url):
        ''' find local file by the url and the origin filename '''
        absPath = os.path.abspath(self.uInput)
        sep = os.sep
        if sep == '\\': # for windows
            sep = '\\\\' # for regexp
        p = re.compile('^(.*'+sep+'js'+sep+').*')
        m = p.search(absPath)
        if m:
            localFile = m.group(1)+os.sep.join(url.split('/'))
            return localFile
        else:
            print "find local file failure, check your style directory , is it a common style of alicn structure"
            raise Exception('find local file failure ,please check your style directory')

    def compress1by1(self):
        ''' comprss the file in self.shouldCompress one by one'''
        if len(self.shouldCompress) is 0:
            return False

        print '*'*10+' compressing , please wait a few seconds '+'*'*10
        for v in self.shouldCompress:
            self.compressSingleFile(v)

    def modifyMergeFile(self):
        ''' modify the merge file , replace the filename to the compressed file '''
        if len(self.lineNos) is 0:
            return False

        tmp = ''
        f = open(self.uInput)
        lineNo = 0
        shouldModifyNos = self.lineNos
        nearestNo = shouldModifyNos.pop(0)
        for line in f.readlines():
            if lineNo is nearestNo:
                tmp += line.replace('.js','-min.js')
                if len(shouldModifyNos) is 0:
                    nearestNo = -1
                else:
                    nearestNo = shouldModifyNos.pop(0)
            else:
                tmp += line
            lineNo += 1
        f.close()
        print '*'*10 + ' The new merge File is: '+ '*'*10
        print tmp
        print '*'*10 +' compress success , please check '+ '*'*10

        modified = open(self.uInput,'w')
        modified.write(tmp)
        modified.close()





    
    def compressSingleFile(self,filepath):
        ''' compress single file and display the result '''
        if not os.path.isfile(filepath):
            print 'Error: "%s" is not a valid file!' % filename
            raise Exception('read file failure')

        content = unicode(open(filepath).read(),'gbk').encode('utf8')

        output = self.compressor(content)

        savename = filepath.replace('.js','-min.js')

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
    def compressor(self,jscode):
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
        #analyFile(sys.argv[1])
        CompressJs(sys.argv[1])
    else:
        print '''This script must contain at least one parameter.
        the first parameter is the the script filename which you want compress
        '''
    if sys.platform == 'win32': # for the exe
        raw_input('press enter to exit')
