#!/usr/bin/env python
# -*- coding: latin-1 -*-
import urllib.request as urllib2

def translate(to_translate, to_langage="ru", langage="auto"):
    """Return the translation using google translate
    you must shortcut the langage you define (French = fr, English = en, Spanish = es, etc...)
    if you don't define anything it will detect it or use english by default
    Example:
    print(translate("salut tu vas bien?", "en"))
    hello you alright?"""
    agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
    before_trans = 'class="t0">'

    c=0
    part_size = 50
    result=[]
    while c<len(to_translate.split('\n')):

        cut_tr_text='\n'.join(to_translate.split('\n')[c:c+part_size])
        c += part_size
        link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (to_langage, langage, cut_tr_text.replace('\n','.!%20').replace(" ", "+"))
        request = urllib2.Request(link, headers=agents)
        page = urllib2.urlopen(request).read().decode()
        p1=page.find(before_trans)
        l1=len(before_trans)
        result_part = page[page.find(before_trans)+len(before_trans):]
        result_part = result_part.split("<")[0].replace('.! ','\n')
        result.extend(result_part.split("\n"))
    return result

if __name__ == '__main__':
    tr_text='translate\nfrom\none language to another\nwith Google\ntranslate'
    print (translate(tr_text))
