# -*- coding: utf-8 -*-
import os
import sys
import string
import re
import time
#import locale
from collections import Counter, OrderedDict
from nltk.corpus import wordnet as wn



from WordNet.Lemmatizer import Lemmatizer
from translate_func3 import translate

##from PyDictionary import PyDictionary




# The method creates a list of files in a 'path' folder
def GetAllFiles(path):
    try:
        return [os.path.join(path, file) for file in os.listdir(path)]
    except Exception:
        raise Exception('Path "%s" does not exists' % path)

# The method parses the file gets out of all words
def ParseBook(file):
    if file.endswith(".txt") or file.endswith(".srt"):
        return ParseTxtFile(file)
    else:
        print('Warning: The file format is not supported: "%s"' %file)


# The method parses the file in txt format
def ParseTxtFile(txtFile):
    try:
        fl = open(txtFile, "r").read()
        print('Processing file: "%s"' %os.path.basename(txtFile))
        return fl.encode('ascii', 'xmlcharrefreplace').decode('ascii')
    except Exception as e:
        print('Error opening "%s"' % txtFile, e)


def thesaurus(word):
    ss=wn.synsets(word)
    lms=wn.lemmas(word)
    if ss:
        pt=200
        defl=''
        for lem in lms:
            if lem.count() == 0:
                lem_count=100
            else: lem_count=lem.count()
            if lem._lexname_index == 0:
                lem_lex_index=1
            else: lem_lex_index=lem._lexname_index/100

            if pt > lem_count+lem_lex_index:
                pt = lem_count+lem_lex_index
                defl=lem.synset().definition()
#                defl=defl+markgreen('['+str(lem.count())+'.'+str(lem._lexname_index)+']'+lem.synset().definition()+';<br>')
 #           else:
#                defl=defl+'['+str(lem.count())+'.'+str(lem._lexname_index)+']'+lem.synset().definition()+';<br>'


    #    ssddf = ss[0].definition()

   #     for ssitem in ss:
  #          curdegf=ssitem.lexname
        return defl # ss[0].definition()
    else:
        return ''

def markblue(text):
    return '<font color="#000088">'+text+'</font>'

def markred(text):
    return '<font color="#ff0000">'+text+'</font>'

def markgreen(text):
    return '<font color="#005500">'+text+'</font>'



def highlightentry(word, text):
    word_only = re.compile(r"\b"+word.replace('.', '\.').replace(' ', "[^a-zA-Z]+")+r"\b", re.IGNORECASE) # removed |re.VERBOSE
    match = word_only.sub("<strong>"+word+"</strong>", text)
    return match

def endotentry(word, text):
    word_only = re.compile(r"\b"+word.replace('.','\.').replace(' ',"[^a-zA-Z]+")+r"\b", re.IGNORECASE) # removed |re.VERBOSE
    match = word_only.sub("<strong>"+word[0]+"...</strong>", text)
    return match

def extractentry(word, lemmas, text):
    strip = string.whitespace + string.punctuation + string.digits + "\"'"
    orother = word
    if word.lower() in lemmas:
        orother=lemmas[word.lower()]
    orother=orother.rstrip(strip)
    word_only = re.compile(r"[!,;\.\?][^!,;\.\?]*.{0,10}?[^-]\b"+orother.replace('.','\.').replace(' ',"[^a-zA-Z]+")+r"s?\b'?[^-].{0,10}[^!,;\.\?]*[!,;\.\?]", re.IGNORECASE|re.DOTALL) #add !, ?; replace * -> {0:n}|re.VERBOSE
    match = word_only.findall(text)
    for m in range(len(match)):
        match[m] = match[m].lstrip(strip)
    return highlightentry(orother, '&nbsp;'+'<br>'.join(match[:examples_limit]))

def readdict(filename):
    wordsdict = []
    if os.path.exists(filename):
        #print("File ", path, " doesn't exists")
        fldict = open(filename,"r").read()
        fldict = fldict.lower()
        wordsdict = fldict.split('\n')
        if wordsdict[-1]=='': wordsdict.pop()                 #removing last empty item at the end
    else:
        open(filename, 'w').close()
    return wordsdict

def text2words(text):
    wordPattern = re.compile("((?:[a-zA-Z]+[-\.']?)*(?:&#[0-9]+;)*[a-zA-Z]+)")
    result = wordPattern.findall(text)
    return result

def extractshort(text):
    shortPattern = re.compile("[^a-z]((?:[a-z]{1,3}\.)*[a-z]{1,3})\.")
    result = shortPattern.findall(text.lower())
    return result

def extractabbr(text):
    abbrPattern = re.compile("([A-Z]{2,3})[^a-zA-Z]")
    result = abbrPattern.findall(text)
    return result


##    flout=""
##    spaceset = 1
##    for i in range(len(text)) :
##        if (text[i].isspace() or text[i] in ("<",">")) and spaceset == 0 :   #rework isspace
##            flout += ' '
##            spaceset = 1
##        elif text[i].isalpha() or (text[i-1].isalpha() and text[i+1].isalpha()):     #first and last?
##            spaceset = 0
##            flout += text[i]#.lower() #rework without to lower
##    words = flout.split(' ')
##    if words[-1]=='': words.pop()#removing last empty item at the end

def countwords(words, short):
    """Removes/Replaces endings of words and Counts new words"""
    ends = {"'s":None, "`s":None, "n't":"not", "'d":"had", "'ll":"will", "'re":"are", "'m":"am", "'ve":"have"} #, "in'":('ing',None), "'em":("them", None)
    ntends = {"won't":'will', "can't":'can', "ain't":'are', "an't":'am'}
    wordcounts = {}
    lemmas = Counter()
    #lemmas = defaultdict(list)
    wordcounts = Counter()
    lemmatizer = Lemmatizer(pathToWordNetDict)
#    wordcopy=words[:] # делаем копию чтобы кол-во элементов не выехало за макс индекс
    for s in range(len(words)-1,-1, -1):
        if "'" in words[s]:
            for ending in ends:       #list(ends.keys())
                if words[s][-len(ending):].lower() == ending:
                    if ending == "n't" and words[s].lower() in ntends:
                        words.insert(s+1, "not")
                        words[s]=(ntends[words[s].lower()])
                    else:
                        words[s]=words[s][:-len(ending)]
                        if ends[ending] != None: words.insert(s+1, ends[ending])
                    break
    for curword in words:
        lemma = lemmatizer.GetLemma(curword.lower())
        if (lemma == "") or (' ' in curword) or ('-' in curword and curword.count("-")>lemma.count("-")): # испраляем ошибки лемматайзера. последнее - если он съел часть составного слова
            lemma=curword.lower()
            if (lemma in short) or (curword in short):
                lemmas[lemma] = curword+'.'
                #lemma = curword+'.'

        elif lemma != curword:
            lemmas[lemma] = curword

      #  wordcounts[lemma] = wordcounts.get(lemma, 0) + 1
        wordcounts[lemma] += 1
      #  if lemma=='ca':
      #      exit(0)
    return words, wordcounts,lemmas

def newwords(wordcounts, wordsdict):
    X = set(wordsdict)
    Y = set([i for i in wordcounts])    #UTF-8 problem
    yonly = [item for item in Y if item not in X]
    unknownwordscounts = {w: wordcounts[w] for w in yonly}
    pairs = list(unknownwordscounts.items())
#    pairs.sort(key=lambda a: a[1], reverse=True)
    return pairs


#--------------Main start--------------------------------
starttime=time.time()
examples_limit=3

pathToWordNetDict=".\\lib\\nltk_data\\corpora\\wordnet\\"
path_dict = ".\\lib\\std_dict.txt"
path_userdict = ".\\lib\\user_dict.txt"
path_targetdict = ".\\lib\\target_dict.txt"
path_phrasal = ".\\lib\\phrasal_verbs.txt"
pathToBooks = ".\input"
pathResult = ".\output"

htmlbeginpaste="""<!doctype html><html><head><meta http-equiv="Content-Type" content="text/html; charset=windows-1251"><title>Result Top 1000</title></head><body>    <style>
  p {
    margin: 5px;
    cursor: pointer;
  }
  p:hover {
color: DarkGreen;
  }
  </style>

    <script type="text/javascript">
    var a = []
function CopyP(Element) {
    sw = document.getElementById('container');
    curtext=Element.innerHTML.toString()
    if(!(curtext in a)) {
    sw.innerHTML=sw.innerHTML+Element.innerHTML +'<br>' ;
    a[curtext]=true}
    return false;
}
</script>
<table border=1><tr><th>Word</th><th width="25%">Definition</th><th>Google translate</th><th>Entry</th></tr>
"""

htmlendpaste="""</table><br>
<div  onclick="$selset()"   id="container"  class="javascript" style="font-family: 'Lucida Console', 'Courier New', Courier, monospaced; font-size:95%; background:#F1F1E9; padding:5px 10px; margin-left:2px; width: 30%;"></div>
<script type="text/javascript">//<![CDATA[
$selset = function() {
    var target = document.getElementById('container');
    var rng, sel;
    if ( document.createRange ) {
        rng = document.createRange();
        rng.selectNode( target )
        sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange( rng );
    } else {
        var rng = document.body.createTextRange();
        rng.moveToElementText( target );
        rng.select();
    }
}
</script>


</div></body></html>
"""
emptyrow='<tr><td></td><td></td><td></td><td></td></tr>'




try:
    if not os.path.exists(pathToBooks):
        os.makedirs(pathToBooks)
        raise Exception('Place your files into "%s" folder' %pathToBooks)
    if not os.listdir(pathToBooks):
        raise Exception('Place your files into "%s" folder' %pathToBooks)
    if not os.path.exists(pathResult):
        os.makedirs(pathResult)
    if not (os.path.exists(pathToWordNetDict) and os.path.exists(path_dict)):
        raise Exception('Dictionary files not found')

except Exception as e:
    print(e)
    input("\nPress any key to exit")
    sys.exit(1)
    print('Still working')


wordsdict = readdict(path_dict)+readdict(path_userdict)
wordsphrasal = readdict(path_phrasal)
targetlist=readdict(path_targetdict)

tizer = Lemmatizer(pathToWordNetDict)
##dictionary=PyDictionary()

listBooks = GetAllFiles(pathToBooks)
#--------------------------------------------------------
for book in listBooks:
    fl = ParseBook(book)
    if fl is None: continue
    fl = re.sub('\d+\r?\n\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d\r?\n',' \n',fl) #if subtitles
    fl = re.sub('</?.>',' ',fl) #if subtitles with <i> tags
    #--------------------------------------------------------
    short=extractshort(fl)
    abbr=extractabbr(fl)
    words, wordcounts, lemmas = countwords(text2words(fl), short)  #words - big and small as is; wordcounts - all to small

    #--------------------------------------------------------
    sentences=list(filter(None, fl.replace('!','.').replace('?','.').split('.')))
    firsts= Counter()
    for sentence in sentences:
        if text2words(sentence):
            firsts[text2words(sentence)[0]] += 1

    #--------------------------------------------------------
    phraselist = []
    phrverblist = []
    for i in range(1, len(words)):
        # Get two adjacent elements.
        a = words[i - 1].lower()
        b = words[i].lower()
        # merge two elements.
        if (a not in wordsdict) and (b not in wordsdict) and a!=b:
            # проверку на отсутствие спецсимволов между словами
            real_entry=re.search((a+'\s+'+b), fl, re.IGNORECASE|re.DOTALL)
            if real_entry:
            # проверку на фразу с заглавными
                real_entry_lower=re.search((a+'\s+'+b), fl, re.DOTALL)
                if real_entry_lower and  real_entry.group()==real_entry_lower.group():
                  phraselist.append(a+' '+b)
                else:
                  phraselist.append((a+' '+b).title())
        if (a+' '+b) in wordsphrasal:
            phrverblist.append(a+' '+b)
            phrverblist.append(a+' '+b)
    phrases, phrasecounts, trash = countwords(phraselist+phrverblist, short)
#    phrverbs, phrverbcounts, trash = countwords(wordsphrasal)

    phrasecounts2 = {}
    for phrase in phrasecounts:
        if phrasecounts[phrase] >1:
            phrasecounts2[phrase]= phrasecounts[phrase]
            if wordcounts[phrase.split()[0]]-phrasecounts[phrase]<2 and wordcounts[phrase.split()[1]]-phrasecounts[phrase]<2:
                phrasecounts2[phrase] = wordcounts[phrase.split()[0]]+wordcounts[phrase.split()[1]]
                # это не совсем честный способ - но пока так


    #--------------------------------------------------------

    pairs = newwords(wordcounts, wordsdict)
#    print(locale.getpreferredencoding())
    print('Total words =', len(words))
    print('Unknown words (distinct) =', len(pairs))

    pairs.extend(list(phrasecounts2.items()))
    pairs.sort(key=lambda a: a[1], reverse=True)

 ##   fl = fl.replace('.','..').replace('!','!.').replace('?','!.')
    #--------------------------------------------------------
#    try:
    if not os.path.exists(pathResult):
        raise Exception('No such directory: "%s"' %pathResult)
#        unknownwords = writeresults(pairs, fl, lemmas) # better to split this function
#    """Calculates total quantity of unknown words and prints all words to html table"""
    resultfile=os.path.splitext(os.path.basename(book))[0]
    output = open(os.path.join(pathResult, resultfile+'.htm'), mode='w', encoding='cp1251', errors='xmlcharrefreplace')
    finaloutput=htmlbeginpaste
#    output.writelines(r''+htmlbeginpaste+r'')
    unknownwords = 0
    persoutput=''
    otheroutput=''
    goodoutput=''
    targetoutput=''
    sosos=OrderedDict(pairs).keys()
    translated_list=iter(translate('\n'.join(sosos)))
    for w in pairs:
     #   if google is unavailable
        try:
           GTword=next(translated_list)
        except: GTword='---'
        finalword = w[0]
        if w[0].upper() in abbr:
            finalword = w[0].upper()
        else:
            finalword = w[0]
        explan1=thesaurus(finalword)
        feature=explan1

      # adding second description if word was lemmatized
        if lemmas[finalword]:
              explan2=thesaurus(lemmas[finalword])
              try:
                GTword2=translate(lemmas[finalword])[0]
              except: GTword2='---'

       #       feature='1: '+feature+'<br>'+'2: '+explan2
       #       GTword='1: '+GTword+'<br>'+'2: '+GTword2


#            if explan2 and feature!=explan2:
#               if feature:
#                 feature=feature+'<br>'
#               feature=feature+lemmas[finalword]+' - '+explan2


      # 2-3 letters
        if (w[0].upper() in abbr):
            feature=markblue('[Abbr]')+feature

      # non-english word
        if ('&#' in w[0]):
            feature=markblue('[Non-english word]')+feature

      # may be with capital letter or whitespace
        if (w[0] not in words):
           if (w[0].capitalize() in words):
                finalword = w[0].capitalize()
                if firsts[finalword]<w[1]:
                   if GTword[0].isupper():
                      feature=markblue('[Personal name]')+markgreen(feature)
                   elif finalword.lower() not in targetlist:
                      feature=markblue('[Semi-Personal name]')+feature
           elif (w[0] in phraselist) or (w[0].title() in phraselist):
                if not feature:
                    d12={f:thesaurus(f) for f in finalword.lower().split(' ')}
                    a_list=';<br>'.join([str(key) + ': ' + str(value) for key, value in d12.items() if (key.lower() not in wordsdict and value)])
                    if a_list:
                        feature=feature+markblue("[Word by word definition] ")+a_list
                feature=markblue('[Word-combination]') + feature
                unknownwords -= w[1]
                if (w[0].title() in phraselist): finalword = w[0].title()
           elif (w[0] in phrverblist):
                feature=markgreen(feature)+markblue('[Phrasal verb]')
                unknownwords -= w[1]-1

      # no description = thesaurus doesn't know this word
        if not feature:
            if lemmas[finalword]:
                #лематизированная форма не дала ничего полезного - заменяем всё на оригинал
                finalword=lemmas[finalword]
                GTword=GTword2
                feature=explan2

              # Word with dashes
            if '-' in finalword:
                d12={f:thesaurus(f) for f in finalword.lower().split('-')}
                a_list=';<br>'.join([str(key) + ': ' + str(value) for key, value in d12.items() if (key.lower() not in wordsdict and value)])
                if a_list:
                    feature=feature+markblue("[Word by word definition] ")+a_list
                else:
                    feature=' '


            # still no description
            if not feature:
                # Google doesn't know this word
                if (GTword[0] in string.ascii_letters):
                   feature=markgreen(feature)+markred('[Misspelling]')
                else:
                   feature=markgreen(feature)+markred('[Unknown]')

            # series of up to 3 letters with .
            if (w[0] in short):
                # перенести это в функцию опредения сокращений
                real_short=re.search("[^-'A-Za-z\.]"+w[0]+"[^-A-Za-z\.]", fl, re.IGNORECASE|re.DOTALL)
                if not real_short:
                    feature=markblue('[Shortening]')+feature
       #gjrf не знаю         finalword=lemmas[finalword]
       #gjrf не знаю         GTword=translate(finalword)[0]
##                    finalword=finalword+'.'
        else:
          if lemmas[finalword] != 0:
            # не знаю почему только здесь, но пусть будет
              if explan2 and explan1!=explan2:
                   feature=feature+'<br>'+lemmas[finalword]+' - '+explan2
                   GTword=GTword+'<br>'+GTword2
              if tizer.IsIrregular(lemmas[finalword]):
                   feature=markblue('{Irregular}')+feature
     #         if (w[0] in short):
    #               feature=markblue('[Shortening-else]')+feature

##            beetergtword, bettermean = '',''
##            try:
##                bettermean=str(dictionary.meaning(finalword))
##                beetergtword=str(dictionary.translate(finalword,'ru'))
##            except: pass

        GTword = GTword
        feature = feature
        nextline='<tr><td valign=top><p Onclick = "return CopyP(this);">'+finalword+r'</p></td><td valign=top>'+feature+r'</td><td valign=top>'+GTword+r'</td><td>'+extractentry(finalword, lemmas,'. '+fl+' .')+r'</td></tr>'
     #   output.writelines(nextline)
     #   finaloutput += nextline
        if '[' in feature:
            if 'Personal name' in feature:
                 persoutput += nextline
            else:
                 otheroutput += nextline
        elif finalword.lower() in targetlist:
            targetoutput += nextline
        else:
            goodoutput += nextline
        unknownwords += w[1]
  #  output.writelines(htmlendpaste)
    finaloutput += targetoutput+emptyrow+goodoutput+otheroutput+persoutput+htmlendpaste
    output.writelines(finaloutput)
    output.close()

#    except Exception as e:
 #       print(e)





    print('Known words =', round(100-100*unknownwords/len(words)), '%')
#    print('Time =', time.time()-starttime)
input("--------------------------------------------------------\nFinished\nPress any key to exit")
