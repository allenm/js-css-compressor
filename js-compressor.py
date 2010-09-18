#!/usr/bin/python2.6

import httplib, urllib, sys, os

# Define the parameters for the POST request and encode them in
# a URL-safe format.


def compressor():
    ''' compressor and combine the javascript files. This script use the google closure REST API '''
    code_urls = [('code_url',v) for v in sys.argv[2].split(";")]
    code_urls.extend([('compilation_level', 'SIMPLE_OPTIMIZATIONS'),('output_format', 'text'),('output_info', 'compiled_code'),])

    params = urllib.urlencode(code_urls)

    # Always use the following value for the Content-type header.
    headers = { "Content-type": "application/x-www-form-urlencoded" }
    conn = httplib.HTTPConnection('closure-compiler.appspot.com')
    conn.request('POST', '/compile', params, headers)
    response = conn.getresponse()
    data = response.read()
    print data
    conn.close
    donejs = open(sys.argv[1],'w')
    donejs.write(data)
    donejs.close()

if(sys.argv.__len__() == 3):
    compressor()
else:
    print 'This script must have two parameters.\n The first is the filename which you want store\
the data after compress.\n The second is the urls of javascript file which you want\
compress, if you have more than one javascript file want to compress, use ";" to \
partition them.'
