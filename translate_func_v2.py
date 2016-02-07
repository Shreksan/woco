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
        response=urllib2.urlopen('https://www.google.com.ua',timeout=1) #74.125.228.100
    except urllib2.URLError as err: return []
    portion_size=10

    try:
        url = "https://www.googleapis.com/language/translate/v2?%s"
        api_key='AIzaSyDeOontva7XOStZRJBgfDYNHQSIrKdwyW0'
        list_of_params = {'key' : api_key, 'source' : 'en',   'target' : 'ru' }
        c=0
		## http://translate.google.com/translate_a/t?client=x&text=hello\nworld&sl=cs&tl=en
        result=[]
        while c<len(tr_text.split('\n')):

            cut_tr_text='\n'.join(tr_text.split('\n')[c:c+portion_size])
            c += portion_size
            list_of_params.update({'q' :  cut_tr_text})

            request = urllib2.Request(url % urllib.parse.urlencode(list_of_params),
               headers={ 'User-Agent': 'Mozilla/5.0', 'Accept-Charset': 'utf-8' })
            res = urllib2.urlopen(request).read()












            fixed_json = re.sub(r',{2,}', ',', res.decode()).replace(',]', ']')
            data = json.loads(fixed_json)

            #simple translation
            for i in range(len(data[0])):
               result.append(data[0][i][0])  #.encode('cp1251', 'replace').decode('cp1251'))
        return result
    except Exception as e:
        print(e)
        return []


#def define(tr_text):
#http://www.urbandictionary.com/define.php?term=negatory


if __name__ == '__main__':
    tr_text='translate from one language to another with Google translate'
    print (translate(tr_text))
