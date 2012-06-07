# -*- coding: utf-8 -*-
# Author:  Arthur Helfstein Fragoso
# Email: arthur@life.net.br
# Based on: "hello-world plugin", "aprendiendoTTS" and "Japanese Support"
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
#   GoogleTTS plugin for Anki 2.0
version = '0.2.0-Alpha 1'
#
#   Any problems, comments, please post in this thread:  (or email me: arthur@life.net.br )
#
#   http://groups.google.com/group/ankisrs/browse_thread/thread/98177e2770659b31
#
#  Edited on 2012-04-24
#  
########################### Announcements #######################################
#
# GoogleTTS is still being ported to Anki 2.0, at the moment it can only read on the fly.
#
# I'm working on porting the MP3 Generator and the MP3 Mass Generator, and I will release it as soon as possible.
#
#
########################### Instructions #######################################
# 
# In your cards, you can add: [GTTS:language_code:text] and GoogleTTS will read it for you. 
# you may have many different languages in the same field
# note that each tag is limited to 100 characters.
# example: [GTTS:en:Hello, whats your name?] [GTTS:zh:你好吗？] [GTTS:ja:はい]
#
# so if you want GoogleTTS to read a field for you, you can edit your card's model and leave it like:
# [GTTS:en:{{Field Name}}]
#
# To hide the [GTTS::] tag and everything inside it in a card model (only) (thanks Rdamon for the idea)
# <!-- [GTTS:en:{{Field Name}}] -->
#
# to hide it while editing a card, the only way I know is:
# <span style="color:#ffffff;">[GTTS:en:Hello World]</span>
#
# it will only read the cards on the Anki Desktop, if you want it on the mobile, you need to generate the MP3 files.
#
## Proxy - If you use a proxy connection, GoogleTTS plugin will use the configuration
# from Anki's proxy confirguration (Settings > Preferences > Network > Proxy) 
# it will only take effect after restarting Anki. If Anki's proxy configuration is
# empty, it will try to use the Operational System proxy configuration.
#
# Thanks Scott Otterson for contributing with the proxy code.
#
#######################################
#
# Some personal recomendation:
# I encourage you to watch the documentary movie: "Zeitgeist: Moving Forward"
# It's probably the most important movie you could ever watch.
# http://www.youtube.com/watch?v=4Z9WVZddH9w
#
# I also recommend a website to live your live to the full potential:
# http://www.highexistence.com/
#
########################### Settings #######################################
from PyQt4.QtCore import *
TTS_read_field = {}
TTS_tags_only, TTS_if_no_tag_read_whole = [1,2]


# Key to get the [GTTS::] tags in the Question field pronounced
TTS_KEY_Q=Qt.Key_F3

# Key to get the [GTTS::] tags in the Answer field pronounced
TTS_KEY_A=Qt.Key_F4

# Key to get the whole Question field pronounced, if there is a [GTTS::] tags, it will only read the tags
TTS_KEY_Q_ALL=Qt.Key_F6

# Key to get the whole Answer field pronounced, if there is a [GTTS::] tags, it will only read the tags
TTS_KEY_A_ALL=Qt.Key_F7



#sorry, the TTS won't recite it automatically when there is a sound file in the Question/Answer

# Option to automatically recite the Question field as it appears:
automaticQuestions = False 			 # disable the automatic recite
#automaticQuestions = TTS_tags_only               # recite only [GTTS::] tags in the Questions as it appears
#automaticQuestions = TTS_if_no_tag_read_whole    # always recite the whole, but if there is a [GTTS::], it will only read the tags

# Option to automatically recite the Answers field as it appears
#automaticAnswers = False                         # disable the automatic recite
#automaticAnswers = TTS_tags_only                 # recite only [GTTS::] tags in the Answers as it appears
#automaticAnswers = TTS_if_no_tag_read_whole      # always recite the whole, but if there is a [GTTS::], it will only read the tags


#subprocessing is enabled by default
# on MS Windows XP or older, there is a bug of cutting the ending of a speech occasionally, so you may want to disable it.
#if it's disable(false), Anki will be frozen while GoogleTTS recites the speech. 
#subprocessing = False
subprocessing = True


#Language code
TTS_language = 'en'



#Supported Languages       
# code , Language, windows charset encoding
slanguages = [['af', 'Afrikaans', 'cp1252'], #or iso-8859-1
['sq', 'Albanian',	'cp1250'], #or iso 8859-16
['ar', 'Arabic',	'cp1256'], #or iso-8859-6
['hy', 'Armenian',	'armscii-8'],
['ca', 'Catalan',	'cp1252'], #or iso-8859-1
['zh', 'Chinese',	'cp936'],
['hr', 'Croatian',	'cp1250'], #or iso-8859-2
['cs', 'Czech',		'cp1250'], #or iso-8859-2
['da', 'Danish',	'cp1252'], #or iso-8859-1
['nl', 'Dutch',		'cp1252'], #or iso-8859-1
['en', 'English',	'cp1252'], #or iso-8859-1
['fi', 'Finnish',	'cp1252'], #or iso-8859-1
['fr', 'French',	'cp1252'], #or iso-8859-1
['de', 'German',	'cp1252'], #or iso-8859-1
['el', 'Greek',		'cp1253'], #or iso-8859-7
['ht', 'Haitian Creole','cp1252'], #or iso-8859-1
['hi', 'Hindi',		'cp1252'], #or iso-8859-1
['hu', 'Hungarian',	'cp1250'], #or iso-8859-2
['is', 'Icelandic',	'cp1252'], #or iso-8859-1
['id', 'Indonesian'],
['it', 'Italian',	'cp1252'], #or iso-8859-1
['ja', 'Japanese',	'cp932'], #or shift_jis, iso-2022-jp, euc-jp
['ko', 'Korean',	'cp949'], #or euc-kr
['la', 'Latin'],
['lv', 'Latvian',	'cp1257'], #or iso-8859-13
['mk', 'Macedonian',	'cp1251'], #iso-8859-5
['no', 'Norwegian',	'cp1252'], #or iso-8859-1
['pl', 'Polish',	'cp1250'], #or iso-8859-2
['pt', 'Portuguese',	'cp1252'], #or iso-8859-1
['ro', 'Romanian',	'cp1250'], #or iso-8859-2
['ru', 'Russian',	'cp1251'], #or koi8-r, iso-8859-5
['sr', 'Serbian',	'cp1250'], # cp1250 for latin, cp1251 for cyrillic
['sk', 'Slovak',	'cp1250'], #or iso-8859-2
['es', 'Spanish',	'cp1252'], #or iso-8859-1
['sw', 'Swahili',	'cp1252'], #or iso-8859-1
['sv', 'Swedish',	'cp1252'], #or iso-8859-1
['tr', 'Turkish',	'cp1254'], #or iso-8859-9
['vi', 'Vietnamese',	'cp1258'],
['cy', 'Welsh',		'iso-8859-14']]


#Address to the TTS service
TTS_ADDRESS = 'http://translate.google.com/translate_tts'

######################### End of Settings ##################################
import os, subprocess, re, sys, urllib
#from ankiqt import mw
from anki import sound
from anki.sound import playFromText
from anki.utils import stripHTML
#from anki.facts import Fact
from subprocess import Popen, PIPE, STDOUT
from urllib import quote_plus
#from ankiqt.ui import view,facteditor,utils
from anki.hooks import wrap
from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import *
from PyQt4.QtSvg import *
import simplejson
from aqt.reviewer import Reviewer

language_generator = TTS_language
file_max_length = 255 # Max filename length for Unix

# Prepend http proxy if one is being used.  Scans the environment for
# a variable named "http_proxy" for all operating systems
# proxy code contributted by Scott Otterson
proxies = urllib.getproxies()

if len(proxies)>0 and "http" in proxies:
	proxStr = re.sub("http:", "http_proxy:", proxies['http'])
	TTS_ADDRESS = proxStr + "/" + TTS_ADDRESS




# mplayer for windows
if subprocess.mswindows:
	file_max_length = 100 #guess of a filename max length for Windows (filename +path = 255)
	dir = os.path.dirname(os.path.abspath(sys.argv[0]))
	os.environ['PATH'] += ";" + dir
	si = subprocess.STARTUPINFO()
	try:
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	except:
		# python2.7+
		si.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW


######## utils
def get_language_id(language_code):
	x = 0
	for d in slanguages:
		if d[0]==language_code:
			return x
		x = x + 1

def playTTSFromText(text):
	address = []
	for match in re.findall("\[GTTS:(.*?):(.*?)\]", text, re.M|re.I):
		speakit = []
		sentence = match[1]
		sentence = re.sub("\[sound:.*?\]", "", stripHTML(sentence.replace("\n", "")).encode('utf-8'))
		if len(sentence) > 100:
			utils.showInfo(sentence)
			split1 = sentence.split('.')
			for item1 in split1:
				if len(item1) > 100:
					utils.showInfo(item1)
					split2 = sentence.split(',')
					for item2 in split2:
						if len(item2) < 100:
							speakit.append(item2)
				else:
					speakit.append(item1)
		else:
			speakit.append(sentence)
		for item in speakit:
			address.append(TTS_ADDRESS+'?tl='+match[0]+'&q='+ quote_plus(item))
	if subprocess.mswindows:
		param = ['mplayer.exe', '-ao', 'win32', '-slave', '-user-agent', "'Mozilla/5.0'"]
		param.extend(address)
		if subprocessing:
			subprocess.Popen(param, startupinfo=si, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
		else:
			subprocess.Popen(param, startupinfo=si, stdin=PIPE, stdout=PIPE, stderr=STDOUT).communicate()
	else:
		param = ['mplayer', '-slave', '-user-agent', "'Mozilla/5.0'"]
		param.extend(address)
		if subprocessing:
			subprocess.Popen(param, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
		else:
			subprocess.Popen(param, stdin=PIPE, stdout=PIPE, stderr=STDOUT).communicate()

######################################### Keys and AutoRead

## Check pressed key
def newKeyHandler(self, evt):
	pkey = evt.key()
	if (self.state == 'answer' or self.state == 'question'):
		if (pkey == TTS_KEY_Q):
			playTTSFromText(self.card.q())  #read the GTTS tags
		elif (pkey == TTS_KEY_Q_ALL):
			if re.findall("\[GTTS:(.*?):(.*?)\]", self.card.q(), re.M|re.I):
				playTTSFromText(self.card.q()) #read the GTTS tags
			else:
				TTS_read(self.card.q(),TTS_language) #read the the whole field
		elif (self.state=='answer' and pkey == TTS_KEY_A):
			playTTSFromText(self.card.a()) #read the GTTS tags
		elif (self.state=='answer' and pkey == TTS_KEY_A_ALL):
			if re.findall("\[GTTS:(.*?):(.*?)\]", self.card.a(), re.M|re.I):
				playTTSFromText(self.card.a()) #read the GTTS tags
			else:
				TTS_read(self.card.a(),TTS_language)  #read the the whole field
#		else:
#			for key in TTS_read_field:
#				if TTS_read_field[key] == pkey:
#					TTS_read(self.currentCard.fact.get(key, 0),TTS_language)
#					break
	evt.accept()



def GTTSautoread(toread, automatic):
	if not sound.hasSound(toread):
		if automatic == TTS_tags_only:
			playTTSFromText(toread)
		if automatic == TTS_if_no_tag_read_whole:
			if re.findall("\[GTTS:(.*?):(.*?)\]", toread, re.M|re.I):
				playTTSFromText(toread)
			else:
				TTS_read(toread,TTS_language)

def GTTS_OnQuestion(self):
	GTTSautoread(self.card.q(), automaticQuestions)

def GTTS_OnAnswer(self):
	GTTSautoread(self.card.a(), automaticAnswers)



Reviewer._keyHandler = wrap(Reviewer._keyHandler, newKeyHandler, "before")
Reviewer._showQuestion = wrap(Reviewer._showQuestion, GTTS_OnQuestion, "after")
Reviewer._showAnswer  = wrap(Reviewer._showAnswer, GTTS_OnAnswer, "after")
