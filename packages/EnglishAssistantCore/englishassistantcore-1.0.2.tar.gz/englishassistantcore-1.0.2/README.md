# English Assistant Core		 
This project is related to the implementation of the English Assistant Application, which helps us to learn English as an assistant. And, Also this package has the ability to translate from English to Persian.
## Instruction

1. Install [Python](https://www.python.org/).



2. Install [English Assistant Core](https://github.com/yasharsajadi/EnglishAssistantCore)

Windows:
```
pip install EnglishAssistantCore
```
Linux:
```
pip3 install EnglishAssistantCore
```

## Usage
```
#Get a string as a list.
List = ["Hello"]
#List = ["Hello, I am WinCento and this is a test message for you, which is written with code and by my own library. This library has the ability to speak 1 languages. and can adjust the speaking rate in it."]

#Prepare the text and core.
_text = List[0]
_core = Core()

#Configurate core.
_core.set_voice('en') #language
_core.set_rate(140) #rate

#Speak:
_core.speak(_text)

#Record:
import os
_core.record(_text,os.path.join(os.path.join(os.path.dirname(__file__)),'output.mp3'))

#Tag_spacy:
_tag = _core.find_tag_spacy(_text)
_expo = _core.tag_translator_spacy(_tag)
print(_text+" is "+_expo)

#Tag_pickle(optional):
# _tag = _core.find_tag_pickle(_text)
# _expo = _core.tag_translator_pickle(_tag)
# print(_text+" is "+_expo)

#Translate To Persian - Online
_core.set_translator_lang()
_trans = _core.translate_action(_text)
print(_trans)

#Pronunciation
_pron = _core.find_pronunc(list(filter(None, re.split(r'\s|\.|,', _text))))
print(_pron)
```




