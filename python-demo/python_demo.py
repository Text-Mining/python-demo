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
    response = requests.request("POST", url, data=data.encode("utf-8"), headers=headers)
    return response.text
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
payload = u"{\"text\":\"ولــے اگــر دڪــمــه مــڪــث رو لــمــس ڪــنــیــم ڪــلــا مــتــن چــنــدیــن صــفــحــه جــابــه جــا مــیــشــه و دیــگــه نــمــیــشــه فــهمــیــد ڪــدوم آیــه تــلــاوت مــی شود بــایــد چــے ڪــنــیــم؟.\", \"refineSeparatedAffix\":true}"
print(callApi(url, payload, tokenKey))

##################### Call Sentence Splitter ########################
url =  baseUrl + "PreProcessing/SentenceSplitter"
payload = u'''{\"text\": \"من با دوستم به مدرسه می رفتیم و در آنجا مشغول به تحصیل بودیم. سپس به دانشگاه راه یافتیم\",
    \"checkSlang\": true, 
    \"normalize\": true, 
    \"normalizerParams\": {
        \"text\": \"don't care\",
        \"RefineQuotationPunc \": false
    },
    \"complexSentence\": true
}'''
print(callApi(url, payload, tokenKey))

######################## Call Tokenizer ############################
url =  baseUrl + "PreProcessing/Tokenize"
payload = u"\"من با دانشجویان دیگری برخورد کردم\""
print(callApi(url, payload, tokenKey))

############# Call Sentence Splitter and Tokenizer #################
url =  baseUrl + "PreProcessing/SentenceSplitterAndTokenize"
payload = u'''{\"text\": \"من با دوستم به مدرسه می رفتیم و در آنجا مشغول به تحصیل بودیم. سپس به دانشگاه راه یافتیم\",
    \"checkSlang\": true, 
    \"normalize\": true, 
    \"normalizerParams\": {
        \"text\": \"don't care\",
        \"replaceWildChar\": true,
        \"replaceDigit\": true,
        \"refineSeparatedAffix\": true,
        \"refineQuotationPunc\": false
    },
    \"complexSentence\": true
}'''
print(callApi(url, payload, tokenKey))

########################## Call Stemmer ##########################
url =  baseUrl + "Stemmer/LemmatizeText2Text"
payload = u'"من با دانشجویان دیگری برخورد کردم. سپس به آنها گفتم\nمن با شما کارهای زیادی دارم"'
print(callApi(url, payload, tokenKey))

url =  baseUrl + "Stemmer/LemmatizePhrase2Phrase"
payload = u'{"phrases": [{ "word": "دریانوردانی" }, { "word": "فرشتگان" }], "checkSlang": false}'
print(callApi(url, payload, tokenKey))

url =  baseUrl + "Stemmer/LemmatizeText2Phrase"
payload = u'{"text": "دانشجویان زیادی به مدارس استعدادهای درخشان راه پیدا نخواهند کرد که با مشکلات بعدی مواجه شوند.", "checkSlang": false}'
result = json.loads(callApi(url, payload, tokenKey))
for phrase in result:
    print("("+phrase['word']+":"+phrase['firstRoot']+") ")

url =  baseUrl + "Stemmer/LemmatizeWords2Phrase"
payload = u'["دریانوردانی", "جزایر", "فرشتگان", "تنها"]'
result = json.loads(callApi(url, payload, tokenKey))
for phrase in result:
    print("("+phrase['word']+":"+phrase['firstRoot']+") ")

#################### Call Spell Corrector ########################
url =  baseUrl + "TextRefinement/SpellCorrector"
payload = u'''{\"text\": \"فهوه با مبات میجسبد\",
            \"checkSlang\": true, 
            \"normalize\": true, 
            \"candidateCount\": 2}'''
print(callApi(url, payload, tokenKey))

################ Call Spell Corrector in Context ##################
url =  baseUrl + "TextRefinement/SpellCorrectorInContext"
payload = u'''{\"text\": \"ستر حیوانی است که در صحرا با مقدار کم آب زندگی میکند\",
            \"normalize\": true, 
            \"candidateCount\": 3}'''
print(callApi(url, payload, tokenKey))

################## Call Swear Word Detector ######################
url =  baseUrl + "TextRefinement/SwearWordTagger"
payload = u'"خـــــــرررررهای دیووووونههه  -   صکس  س.ک.س ی  \r\n بیپدرومادر"'
result = json.loads(callApi(url, payload, tokenKey))
## for item in result: ...
print(result)

################ Call Slang to Formal Converter ##################
url =  baseUrl + "TextRefinement/FormalConverter"
payload = u'''"اگه اون گزینه رو کلیک کنین، یه پنجره باز میشه که میتونین رمز عبورتون رو اونجا تغییر بدین
    داشتم مي رفتم برم، ديدم گرفت نشست، گفتم بذار بپرسم ببينم مياد نمياد ديدم ميگه نميخوام بيام بذار برم بگيرم بخوابم نمیتونم بشینم.
    کتابای خودتونه
    نمیدونم چی بگم که دیگه اونجا نره
    ساعت چن میتونین بیایین؟"'''
print(callApi(url, payload, tokenKey))

######################## Call POS-Tagger ############################
url =  baseUrl + "PosTagger/GetPos"
payload = u'"احمد و علی به مدرسه پایین خیابان می رفتند"'
result = json.loads(callApi(url, payload, tokenKey))
for phrase in result:
    print("("+phrase['word']+","+phrase['tags']['POS']['item1']+") ")

############################ Call NER ###############################
url =  baseUrl + "NamedEntityRecognition/Detect"
payload = u'"احمد عباسی به تحصیلات خود در دانشگاه آزاد اسلامی در مشهد ادامه داد"'
result = json.loads(callApi(url, payload, tokenKey))
for phrase in result:
    print("("+phrase['word']+","+phrase['tags']['NER']['item1']+") ")

##################### Call Language Detection #######################
url =  baseUrl + "LanguageDetection/Predict"
payload = u'"شام ییبسن یا یوخ. سن سیز بوغازیمنان گتمیر شام. به به نه قشه یردی. ساغ اول سیز نئجه سیز. نئجه سن؟ اوشاقلار نئجه دیر؟ سلام لاری وار سیزین کی لر نئجه دیر. یاخچی"'
print(callApi(url, payload, tokenKey))

################## Call Sentiment Classification ####################
url =  baseUrl + "SentimentAnalyzer/SentimentClassifier"
payload = u"\"اصلا خوب نبود\""
print(callApi(url, payload, tokenKey))

###################### Call Text Similarity #########################
url =  baseUrl + "TextSimilarity/ExtractSynonyms"
payload = u"\"احسان\""
print(callApi(url, payload, tokenKey))

url =  baseUrl + "TextSimilarity/GetSyntacticDistance"
payload = u'{"string1": "ایرانی ها", "string2": "ایرانیان", "distanceFunc": 2}'  # JaccardDistance
print(callApi(url, payload, tokenKey))

url =  baseUrl + "TextSimilarity/SentenceSimilarityBipartiteMatching"
payload = u'''{
    "string1": "حمله مغولها به ایران", 
    "string2": "حملات مغولان به ایران", 
    "distanceFunc": 2}'''  # JaccardDistance
print(callApi(url, payload, tokenKey))

url =  baseUrl + "TextSimilarity/SentenceSimilarityWithIntersectionMatching"
payload = u'''{
    "string1": "حمله مغولها به ایران", 
    "string2": "حملات مغولان به ایران", 
    "distanceFunc": 2,
    "minDistThreshold": 0.3}'''  # حداقل فاصله دو کلمه برای انطباق (یکسان فرض نمودن) آنها
print(callApi(url, payload, tokenKey))

url =  baseUrl + "TextSimilarity/SentenceSimilarityWithNGramMatching"
payload = u'''{
    "string1": "حمله مغولها به ایران", 
    "string2": "حملات مغولان به ایران", 
    "distanceFunc": 2,
    "minDistThreshold": 0.3}'''  # حداقل فاصله دو کلمه برای انطباق (یکسان فرض نمودن) آنها
print(callApi(url, payload, tokenKey))

url =  baseUrl + "TextSimilarity/SentenceSimilarityWithNearDuplicateDetector"
payload = u'''{
    "string1": "حمله مغولها به ایران", 
    "string2": "حملات مغولان به ایران"}'''
print(callApi(url, payload, tokenKey))

################ Call Information Retrieval Function(s) ##################
url =  baseUrl + "InformationRetrieval/KeywordExtraction"
payload = u'''{
    "text": "سرمایه گذاری هنگفت امارات در توسعه انرژی
امارات در مناطق شمالی این کشور بیش از ۷۰۰ میلیون درهم در توسعه انرژی سرمایه گذاری می‌کند.
محمد صالح مدیرکل اداره برق امارات در نشست خبری اعلام کرد که امارات متحده عربی از امسال تا سال ۲۰۲۲ میلادی ۸ پروژه مهم انرژی به منظور توسعه و گسترش برق مناطق شمالی امارات اجرا خواهد کرد.
وی افزود: این طرح‌ها با هزینه‌ای بالغ بر ۷۰۰ میلیون درهم احداث و تکمیل خواهد شد.", 
    "minWordLength": 3,
    "maxWordCount": 3,
    "minKeywordFrequency": 1,
    "resultKeywordCount": 5,
    "method": "TFIDF"}'''
print(callApi(url, payload, tokenKey))