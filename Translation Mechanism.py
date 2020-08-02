"""
This program does two things in case a text is in a different language. 
It transliterates it first into the original language using a request to the Google Input Tools.
Then, it translates the text into the target language.
"""

"""
Importing the requisite libraries. We are using the Python http.client library and
the Google Translate API (THIS WAS PAID FOR).
"""

import http.client
from google.cloud import translate_v2 as translate

"""
Dictionary of supported languages. 
Only Hindi has been shown here, but any language can be added with its valid code and abbreviation.
"""
dict_lang  =  {
        'hi': 'hi-t-i0-und'
        }

"""
#Helper method to send a request to the online input tools
"""
def request(input, itc):
    conn = http.client.HTTPSConnection('inputtools.google.com')
    conn.request('GET', '/request?text=' + input + '&itc=' + itc + '&num=1&cp=0&cs=1&ie=utf-8&oe=utf-8&app=test')
    res = conn.getresponse()
    return res

"""
Driver method to perform the actual transliteration.
"""
def driver(input, itc):
    output = ''
    if ' ' in input:
        input = input.split(' ')
        for i in input:
            res = request(input = i, itc = itc)
            res = res.read()
            if i==0:
                output = str(res, encoding = 'utf-8')[14+4+len(i):-31]
            else:
                output = output + ' ' + str(res, encoding = 'utf-8')[14+4+len(i):-31]
    else:
        res = request(input = input, itc = itc)
        res = res.read()
        output = str(res, encoding = 'utf-8')[14+4+len(input):-31]
    return output

"""
This method is just a checking mechanism to conduct transliteration if the language is supported.
Arguments:
    text2 - The language to be transliterated
    lang_code - The code of the language
"""
def transliterator(text2, lang_code):
    if lang_code in dict_lang:
        return driver(text2, dict_lang[lang_code])
    else:
        return "null"
 
"""
This method converts the transliterated text to English.
Arguments:
    text2 - The text to be translated
    translator - A translator object of the Google Translate API
"""

def translate_to_english(text2, translator):
    output = translator.translate(
        text2,
        target_language = "en"
        )
    return output

"""
Language processing final method.
Arguments:
    text - The text to be translated
    translator - A translator object of the Google Translate API

This API also use the Google Translate API for language detection
"""

def language_processor(text, translator):
    
    #Language detection
    text_lang = translator.detect_language(text)['language']

    #If the language is another, then get back the transliterated text
    if text_lang != 'en':
        transliterated_text = transliterator(text, text_lang)
        #In case we do not support this language again
        if transliterated_text == "null":
            output = "This language is not supported by our system yet."
        else:
            output = translate_to_english(transliterated_text, translator)['translatedText']
    else:
        output = text
    
    return output


