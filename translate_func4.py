#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""This script allow users to translate a string
from one language to another with Google translate"""

import requests

session = requests.session()
p = session.get('http://translate.google.com/translate_a/t?client=x&text=hello%0Aworld&sl=cs&tl=en')
print ('headers', p.headers)
print ('cookies', requests.utils.dict_from_cookiejar(session.cookies))
print ('html',  p.text)