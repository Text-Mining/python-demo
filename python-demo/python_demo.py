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
    return response.text    # return utfReverse(response.text.encode("utf-8"))
    
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
# result: ولی اگر دکمه مکث رو لمس کنیم کلا متن چندین صفحه جابه جا میشه و دیگه نمیشه فهمید کدوم آیه تلاوت می‌شود باید چی کنیم؟.

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
# resuilt: ["من با دوستم به مدرسه می‌رفتیم","و در آنجا مشغول به تحصیل بودیم .","سپس به دانشگاه راه یافتیم"

######################## Call Tokenizer ############################
url =  baseUrl + "PreProcessing/Tokenize"
payload = u"\"من با دانشجویان دیگری برخورد کردم\""
print(callApi(url, payload, tokenKey))
# rsult: ["من","با","دانشجویان","دیگری","برخورد","کردم"]

url =  baseUrl + "PreProcessing/TokenizeWithType"
payload = u"\"اخبار 20:30 مورخ 1398/2/22 اعلام کرد شرکت T.E.T مبلغ 200.57 میلیون ارزش دارد!!!  😒 @Khabar_Alaki -- email: hi@text-mining.ir\""
print(callApi(url, payload, tokenKey))
#result: [{"key":"اخبار","value":"Word"},{"key":"20:30 ","value":"DateTime"},{"key":"مورخ","value":"Word"},{"key":"1398/2/22","value":"DateTime"},{"key":"اعلام","value":"Word"},{"key":"کرد","value":"Word"},{"key":"شرکت","value":"Word"},{"key":"T.E.T","value":"Abbreviation"},{"key":"مبلغ","value":"Word"},{"key":"200.57","value":"Number"},{"key":"میلیون","value":"Word"},{"key":"ارزش","value":"Word"},{"key":"دارد","value":"Word"},{"key":"!!!","value":"Separator"},{"key":"😒","value":"Emoji"},{"key":"@Khabar_Alaki","value":"SocialId"},{"key":"--","value":"Separator"},{"key":"email","value":"Word"},{"key":":","value":"Separator"},{"key":"hi@text-mining.ir","value":"Email"}]

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
# result: [["من","با","دوستم","به","مدرسه","می‌رفتیم"],["و","در","آنجا","مشغول","به","تحصیل","بودیم","."],["سپس","به","دانشگاه","راه","یافتیم"]]

########################## Call Stemmer ##########################
url =  baseUrl + "Stemmer/LemmatizeText2Text"
payload = u'"من با دانشجویان دیگری برخورد کردم. سپس به آنها گفتم\nمن با شما کارهای زیادی دارم"'
print(callApi(url, payload, tokenKey))
''' result: 
من با دانشجو دیگر بر خورد کرد. سپس به آن گفت
من با شما کار زیاد داشت
'''

url =  baseUrl + "Stemmer/LemmatizePhrase2Phrase"
payload = u'{"phrases": [{ "word": "دریانوردانی" }, { "word": "فرشتگان" }], "checkSlang": false}'
print(callApi(url, payload, tokenKey))
# result: [{"wordComment":"","simplePos":"","rootWords":["دریانورد","دریا"],"verbInformation":null,"sentenceNumber":0,"wordNumberInSentence":0,"startCharIndex":0,"word":"دریانوردانی","tags":{},"firstRoot":"دریانورد","wordCount":1,"length":11,"isVerb":false,"isPunc":false},{"wordComment":"","simplePos":"","rootWords":["فرشته"],"verbInformation":null,"sentenceNumber":0,"wordNumberInSentence":0,"startCharIndex":0,"word":"فرشتگان","tags":{},"firstRoot":"فرشته","wordCount":1,"length":7,"isVerb":false,"isPunc":false}]

url =  baseUrl + "Stemmer/LemmatizeText2Phrase"
payload = u'{"text": "دانشجویان زیادی به مدارس استعدادهای درخشان راه پیدا نخواهند کرد که با مشکلات بعدی مواجه شوند.", "checkSlang": false}'
result = json.loads(callApi(url, payload, tokenKey))
for phrase in result:
    print("("+phrase['word']+":"+phrase['firstRoot']+") ")
''' result:
(دانشجویان:دانشجو)
(زیادی:زیاد)
(به:به)
(مدارس:مدرسه)
(استعدادهای:استعداد)
(درخشان:درخشان)
(راه:راه)
(پیدا:پیدا)
(نخواهند کرد:نکرد)
(که:که)
(با:با)
(مشکلات:مشکل)
(بعدی:بعد)
(مواجه:مواجه)
(شوند:شد)
(.:.)
'''

url =  baseUrl + "Stemmer/LemmatizeWords2Phrase"
payload = u'["دریانوردانی", "جزایر", "فرشتگان", "تنها"]'
result = json.loads(callApi(url, payload, tokenKey))
for phrase in result:
    print("("+phrase['word']+":"+phrase['firstRoot']+") ")
''' result:
(دریانوردانی:دریانورد)
(جزایر:جزیره)
(فرشتگان:فرشته)
(تنها:تنها)
'''

#################### Call Spell Corrector ########################
url =  baseUrl + "TextRefinement/SpellCorrector"
payload = u'''{\"text\": \"فهوه با مبات میجسبد\",
            \"checkSlang\": true, 
            \"normalize\": true, 
            \"candidateCount\": 2}'''
print(callApi(url, payload, tokenKey))
# result: قهوه با {نبات,ملات} {می‌چسبد,می‌جنبد}

################ Call Spell Corrector in Context ##################
url =  baseUrl + "TextRefinement/SpellCorrectorInContext"
payload = u'''{\"text\": \"ستر حیوانی است که در صحرا با مقدار کم آب زندگی میکند\",
            \"normalize\": true, 
            \"candidateCount\": 3}'''
print(callApi(url, payload, tokenKey))
# result: {شتر,سطر,سفر} {حیوانی,حیوان,یونانی} {است,دست,هست} که در {صحرا,صفرا,صدرا} با {مقدار,مدار,مقدر} کم آب {زندگی,بندگی,زدگی} {می‌کند,می‌کند,مکند}

################## Call Swear Word Detector ######################
url =  baseUrl + "TextRefinement/SwearWordTagger"
payload = u'"خـــــــرررررهای دیووووونههه  -   صکس  س.ک.س ی  \r\n بیپدرومادر"'
result = json.loads(callApi(url, payload, tokenKey))
## for item in result: ...
print(result)
# result: {'خرررررهای': 'MildSwearWord', 'دیووووونههه': 'MildSwearWord', 'صکس': 'StrongSwearWord', 'س.ک.س': 'StrongSwearWord', 'ی بیپدرومادر': 'StrongSwearWord'}

################ Call Slang to Formal Converter ##################
url =  baseUrl + "TextRefinement/FormalConverter"
payload = u'''"اگه اون گزینه رو کلیک کنین، یه پنجره باز میشه که میتونین رمز عبورتون رو اونجا تغییر بدین
    داشتم مي رفتم برم، ديدم گرفت نشست، گفتم بذار بپرسم ببينم مياد نمياد ديدم ميگه نميخوام بيام بذار برم بگيرم بخوابم نمیتونم بشینم.
    کتابای خودتونه
    نمیدونم چی بگم که دیگه اونجا نره
    ساعت چن میتونین بیایین؟"'''
print(callApi(url, payload, tokenKey))
''' result:
اگر آن گزینه را کلیک کنید، یک پنجره باز می‌شود که می‌توانید رمز عبورتان را آنجا تغییر بدهید
داشتم می‌رفتم بروم، دیدم گرفت نشست، گفتم بگذار بپرسم ببینم می‌آید نمی‌آید دیدم می‌گوید نمی‌خواهم بیایم بگذار بروم بگیرم بخوابم نمی‌توانم بنشینم.
کتاب‌های خودتان است
نمی‌دانم چه بگویم که دیگر آنجا نرود
ساعت چند می‌توانید بیایید؟
'''

######################## Call POS-Tagger ############################
url =  baseUrl + "PosTagger/GetPos"
payload = u'"احمد و علی به مدرسه پایین خیابان می رفتند"'
result = json.loads(callApi(url, payload, tokenKey))
for phrase in result:
    print("("+phrase['word']+","+phrase['tags']['POS']['item1']+") ")
''' result:
(احمد,N)
(و,CON)
(علی,N)
(به,P)
(مدرسه,N)
(پایین,ADJ)
(خیابان,N)
(می‌رفتند,V)
(.,)
'''

############################ Call NER ###############################
url =  baseUrl + "NamedEntityRecognition/Detect"
payload = u'"احمد عباسی به تحصیلات خود در دانشگاه آزاد اسلامی در مشهد ادامه داد"'
result = json.loads(callApi(url, payload, tokenKey))
for phrase in result:
    print("("+phrase['word']+","+phrase['tags']['NER']['item1']+") ")
''' result:
{احمد,B-PER}
{عباسی,I-PER}
{به,O}
{تحصیلات,O}
{خود,O}
{در,O}
{دانشگاه,B-ORG}
{آزاد,I-ORG}
{اسلامی,I-ORG}
{در,O}
{مشهد,I-LOC}
{ادامه,O}
{داد,O}
'''

##################### Call Language Detection #######################
url =  baseUrl + "LanguageDetection/Predict"
payload = u'"شام ییبسن یا یوخ. سن سیز بوغازیمنان گتمیر شام. به به نه قشه یردی. ساغ اول سیز نئجه سیز. نئجه سن؟ اوشاقلار نئجه دیر؟ سلام لاری وار سیزین کی لر نئجه دیر. یاخچی"'
print(callApi(url, payload, tokenKey))
# result: azb

################## Call Sentiment Classification ####################
url =  baseUrl + "SentimentAnalyzer/SentimentClassifier" # output:  0:Negative  1:Neutral  2:Positive
payload = u"\"اصلا خوب نبود\""
print(callApi(url, payload, tokenKey)) 
# result: 0

###################### Call Text Similarity #########################
url =  baseUrl + "TextSimilarity/ExtractSynonyms"
payload = u"\"احسان\""
print(callApi(url, payload, tokenKey))
# result: ["احسان","نیکی کردن","نیکوکاری","بخشش","نیکی","خوبی","نیکویی","انعام","نکویی","اکرام","صنع","فضل","لطف","منت","نزل","نعمت","نیکی_کردن","احسان (نام)","احسان_(نام)"]

url =  baseUrl + "TextSimilarity/GetMostSimilarWord"
payload = u'''{
    "word": "روحانی", 
    "topN": "50"}'''
print(callApi(url, payload, tokenKey))
# result: ["دولت","آقای","احمدی‌نژاد","رئیس‌جمهور","رییس‌جمهور","انتخابات","برجام","اصلاحات","خاتمی","طلبان","حسن","ترامپ","مچکرررریم","استغفار_نمیکنید","جناب","هاشمی","جهانگیری","مردم","ریاست‌جمهوری","اقتصادی","انقلاب","اختلاف_سپاه_ارتش","مجلس","سخنان","حمایت","تدبیر","سیاسی","سخنرانی","اصلاح","اصولگرایان","ظریف","اقای","انتخاباتی","مسئولین","آمریکا","شورای","جمهوری","رفسنجانی","ملت","برخروشیده‌اند","دولت_غربگرا_و_سازشگر","رهبری","جامعه","گفته","مطرح","دکتر","مناظره_روحانی_با_خودش","اصلاح‌طلب","فرصت_بیشتری","ابقای_علی_اوسط_هاشمی"]

url =  baseUrl + "TextSimilarity/GetSyntacticDistance"
payload = u'{"string1": "ایرانی ها", "string2": "ایرانیان", "distanceFunc": 2}'  # JaccardDistance
print(callApi(url, payload, tokenKey))
# result: 0.333333343

url =  baseUrl + "TextSimilarity/GetStatisticalDistance"
payload = u'''{
    "string1": "روحانی", 
    "string2": "جسمانی"}'''
print(callApi(url, payload, tokenKey))
# result: 0.905992568

url =  baseUrl + "TextSimilarity/SentenceSimilarityBipartiteMatching"
payload = u'''{
    "string1": "حمله مغولها به ایران", 
    "string2": "حملات مغولان به ایران", 
    "distanceFunc": 2}'''  # JaccardDistance
print(callApi(url, payload, tokenKey))
# result: 0.80357146263122559

url =  baseUrl + "TextSimilarity/SentenceSimilarityWithIntersectionMatching"
payload = u'''{
    "string1": "حمله مغولها به ایران", 
    "string2": "حملات مغولان به ایران", 
    "distanceFunc": 2,
    "minDistThreshold": 0.3}'''  # حداقل فاصله دو کلمه برای انطباق (یکسان فرض نمودن) آنها
print(callApi(url, payload, tokenKey))
# result: 0.75

url =  baseUrl + "TextSimilarity/SentenceSimilarityWithNGramMatching"
payload = u'''{
    "string1": "حمله مغولها به ایران", 
    "string2": "حملات مغولان به ایران", 
    "distanceFunc": 2,
    "minDistThreshold": 0.3}'''  # حداقل فاصله دو کلمه برای انطباق (یکسان فرض نمودن) آنها
print(callApi(url, payload, tokenKey))
# result: 0.714285708963871

url =  baseUrl + "TextSimilarity/SentenceSimilarityWithNearDuplicateDetector"
payload = u'''{
    "string1": "حمله مغولها به ایران", 
    "string2": "حملات مغولان به ایران"}'''
print(callApi(url, payload, tokenKey))
# result: 0.5

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
''' result:
{
    "امارات": 75.26119828977285,
    "توسعه انرژی": 23.99621570204974,
    "۷۰۰ میلیون درهم": 21.95849183879027,
    "مناطق شمالی": 20.25414682800825,
    "سرمایه‌گذاری هنگفت امارات": 17.670494399999686
}
'''

url =  baseUrl + "InformationRetrieval/StopWordRemoval"
payload = u'''"تیم متن کاوی فارسی‌یار با مجموعه‌ای از فارغ التحصیلان دانشگاه‌های صنعتی شریف، تربیت مدرس و فردوسی مشهد از سال ۱۳۹۰ بصورت تخصصی در زمینه پردازش زبان طبیعی مشغول به فعالیت است. در سال ۱۳۹۶ در جهت فعالیت پژوهشی عمیق­‌تر در زمینه پردازش متون برای زبان فارسی، این گروه با آزمایشگاه متن کاوی و یادگیری ماشین پژوهشگاه علوم و فناوری اطلاعات ایران (ایرانداک) همکاری تنگاتنگی داشته است."'''
print(callApi(url, payload, tokenKey))
# result: تیم متن کاوی فارسی‌یار مجموعه‌ای فارغ التحصیلان دانشگاه‌های صنعتی شریف، تربیت مدرس فردوسی مشهد سال ۱۳۹۰ تخصصی پردازش زبان طبیعی مشغول فعالیت. سال ۱۳۹۶ فعالیت پژوهشی عمیق‌تر پردازش متون زبان فارسی، گروه آزمایشگاه متن کاوی یادگیری ماشین پژوهشگاه علوم فناوری اطلاعات ایران (ایرانداک) همکاری تنگاتنگی.
