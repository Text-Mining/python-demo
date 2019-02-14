# -*- coding: utf-8 -*-
try:
    # Fix UTF8 output issues on Windows console.
    # Does nothing if package is not installed
    from win_unicode_console import enable
    enable()
except ImportError:
    pass

def utfReverse(s):
    # CAVEAT: this will mess up characters that are
    # more than 2 bytes long in utf 16
    u = s.decode("utf-8")
    return u[::-1].encode("utf-8")
# print(utfReverse('\"من با دانشجویان دیگری برخورد کردم\"'))

######################################################################

import requests
import json

def callApi(url, data, tokenKey):    
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + tokenKey,
        'Cache-Control': "no-cache"
    }
    response = requests.request("POST", url, data=data, headers=headers)
    return response.text.encode("utf-8")
    # return utfReverse(response.text.encode("utf-8"))
    
##################### Get Token by Api Key ##########################
baseUrl = "http://api.text-mining.ir/api/"
url = baseUrl + "Token/GetToken"
querystring = {"apikey":"YOUR_API_KEY"}
response = requests.request("GET", url, params=querystring)
data = json.loads(response.text)
tokenKey = data['token']

######################## Call Normalizer ############################
url =  baseUrl + "PreProcessing/NormalizePersianWord"
payload = "{\"text\":\"تست ها\", \"refineSeparatedAffix\":true}"
print(callApi(url, payload, tokenKey))

######################## Call Tokenizer ############################
url =  baseUrl + "PreProcessing/Tokenize"
payload = "\"من با دانشجویان دیگری برخورد کردم\""
print(callApi(url, payload, tokenKey))

############# Call Sentence Splitter and Tokenizer #################
url =  baseUrl + "PreProcessing/SentenceSplitterAndTokenize"
payload = '''{\"text\": \"من با دانشجویان دیگری برخورد کردم. سپس به آنها گفتم\nمن با شما کارهای زیادی دارم\",
    \"checkSlang\": true, 
    \"normalize\": true, 
    \"normalizerParams\": {
        \"text\": \"don't care\",
        \"replaceWildChar\": true,
        \"replaceDigit\": true,
        \"refineSeparatedAffix\": true,
        \"refineQuotationPunc\": false
    },
    \"complexSentence\": false
}'''
print(callApi(url, payload, tokenKey))

########################## Call Stemmer ##########################
url =  baseUrl + "Stemmer/LemmatizeText2Text"
payload = '"من با دانشجویان دیگری برخورد کردم. سپس به آنها گفتم\nمن با شما کارهای زیادی دارم"'
print(callApi(url, payload, tokenKey))

#################### Call Spell Corrector ########################
url =  baseUrl + "TextRefinement/SpellCorrector"
payload = '''{\"text\": \"فهوه با مبات میجسبد\",
            \"checkSlang\": true, 
            \"normalize\": true, 
            \"candidateCount\": 2}'''
print(callApi(url, payload, tokenKey))

################## Call Swear Word Detector ######################
url =  baseUrl + "TextRefinement/SwearWordTagger"
payload = '\"خـــــــرررررهای دیووووونههه  -   صکس  س.ک.س ی  \r\n بیپدرومادر\"'
result = json.loads(callApi(url, payload, tokenKey))
## for item in result: ...
print(result)

################ Call Slang to Formal Converter ##################
url =  baseUrl + "TextRefinement/FormalConverter"
payload = '''"اگه اون گزینه رو کلیک کنین، یه پنجره باز میشه که میتونین رمز عبورتون رو اونجا تغییر بدین
    داشتم مي رفتم برم، ديدم گرفت نشست، گفتم بذار بپرسم ببينم مياد نمياد ديدم ميگه نميخوام بيام بذار برم بگيرم بخوابم نمیتونم بشینم.
    کتابای خودتونه
    نمیدونم چی بگم که دیگه اونجا نره
    ساعت چن میتونین بیایین؟"'''
print(callApi(url, payload, tokenKey))
