#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""This script allow users to translate a string
from one language to another with Google translate"""


import inflect
p = inflect.engine()



if __name__ == '__main__':
    tr_text='translate from one language to another with Google translate'
    print (p.plural("stark"))
    print (p.singular_noun("bosses"))
