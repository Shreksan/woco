#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""This script allow users to translate a string
from one language to another with Google translate"""

import sys
import re
import urllib
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import json

import itertools

def print_params(data):
    """print parameters from list"""
    for val in data:
        if isinstance(val, basestring):
            print ("\t " + val)

def translate(tr_text):

    try:
        response=urllib2.urlopen('http://74.125.228.100',timeout=1)
    except urllib2.URLError as err: return []

    url = "http://translate.google.com/translate_a/t?%s"
    list_of_params = {'client' : 't',
                      'hl' : 'en',
                      'multires' : '1', }
    c=0
    result=[]
    while c<len(tr_text.split('\n')):

        cut_tr_text='\n'.join(tr_text.split('\n')[c:c+50])
        c += 50
        list_of_params.update({'text' : cut_tr_text,
                               'sl' : 'en',
                               'tl' : 'ru' })

        request = urllib2.Request(url % urllib.parse.urlencode(list_of_params),
           headers={
           'User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
           'Accept-Encoding: gzip',
           'Accept-Charset: ISO-8859-1,UTF-8;q=0.7,*;q=0.7',
           'Cache-Control: no-cache',
           'Accept-Language: de,en;q=0.7,en-us;q=0.3'
})
        res = urllib2.urlopen(request).read()

        fixed_json = re.sub(r',{2,}', ',', res.decode()).replace(',]', ']')
        data = json.loads(fixed_json)

        #simple translation
        for i in range(len(data[0])):
           result.append(data[0][i][0])  #.encode('cp1251', 'replace').decode('cp1251'))
    return result


#def define(tr_text):
#http://www.urbandictionary.com/define.php?term=negatory


if __name__ == '__main__':
    tr_text='translate from one language to another with Google translate'
    print (translate(tr_text))
