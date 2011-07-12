# -*- coding: utf-8 -*-
# Author:  Arthur Helfstein Fragoso
# Email: arthur@life.net.br
# Based on: "hello-world plugin" and "aprendiendoTTS"
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
#   GoogleTTS plugin
#
#   Any problems, comments, please post in this thread:  (or email me)
#
#   http://groups.google.com/group/ankisrs/browse_thread/thread/98177e2770659b31
#
#  Edited on Sunday, 16 January 2:23:46 p.m.(GMT + 0:00)
#  
########################### Settings #######################################

from PyQt4.QtCore import *
TTS_read_field = {}


# Key to get the Answer pronounced
TTS_KEY_A=Qt.Key_F4

# Key to get the question pronounced
TTS_KEY_Q=Qt.Key_F3


# Option to automatically recite questions as they appear
automaticQuestions = False
#automaticQuestions = True

# Option to automatically recite answers as they appear
automaticAnswers = False
#automaticAnswers = True


# Keys to get the fields pronounced, case sensitive
# uncomment and change in a way that works for you,
# you can add as many as you want
# examples:
#TTS_read_field['Field Name'] =  Qt.Key_F9
#TTS_read_field['Front'] =  Qt.Key_F5
#TTS_read_field['Back'] = Qt.Key_F6
#TTS_read_field['Reading'] =  Qt.Key_F7
#TTS_read_field['Text'] = Qt.Key_F8
#all the avaliable keys are in http://doc.trolltech.com/qtjambi-4.4/html/com/trolltech/qt/core/Qt.Key.html


#Language code
TTS_language = 'en'


"""
Supported Languages

af - Afrikaans 
sq - Albanian
ar - Arabic
hy - Armenian
ca - Catalan
zh - Chinese
hr - Croatian
cs - Czech
da - Danish
nl - Dutch
en - English
fi - Finnish
fr - French
de - German
el - Greek
ht - Haitian Creole
hi - Hindi
hu - Hungarian
is - Icelandic
id - Indonesian
it - Italian
ja - Japanese
ko - Korean
la - Latin
lv - Latvian
mk - Macedonian
no - Norwegian
pl - Polish
pt - Portuguese
ro - Romanian
ru - Russian
sr - Serbian
sk - Slovak
es - Spanish
sw - Swahili
sv - Swedish
tr - Turkish
vi - Vietnamese
cy - Welsh
"""


######################### End of Settings ##################################
import os, subprocess, re, sys
from ankiqt import mw
from anki import sound
from anki.utils import stripHTML
from subprocess import Popen, PIPE, STDOUT
from ankiqt.ui import view
from anki.hooks import wrap

# mplayer for windows
if subprocess.mswindows:
	dir = os.path.dirname(os.path.abspath(sys.argv[0]))
	os.environ['PATH'] += ";" + dir
	si = subprocess.STARTUPINFO()
	try:
		si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
	except:
		# python2.7+
		si.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW

def TTS_read(text):
	if text:
		address = 'http://translate.google.com/translate_tts?tl='+TTS_language+'&q="'+ re.sub("\[sound:.*?\]", "", stripHTML(text).encode('utf-8')) +'"' 
		if subprocess.mswindows:
			subprocess.Popen(['mplayer.exe', '-ao', 'win32', '-slave', '-user-agent', "'Mozilla/5.0'", address], startupinfo=si, stdin=PIPE, stdout=PIPE, stderr=STDOUT).communicate()
                else:
			subprocess.Popen(['mplayer', '-slave', '-user-agent', "'Mozilla/5.0'", address], stdin=PIPE, stdout=PIPE, stderr=STDOUT)

## Check pressed key
def newKeyPressEvent(evt):
    pkey = evt.key()
    if (mw.state == 'showAnswer' or mw.state == 'showQuestion'):
	if (pkey == TTS_KEY_Q):
		TTS_read(mw.currentCard.question)
	elif (mw.state=='showAnswer' and pkey == TTS_KEY_A):
		TTS_read(mw.currentCard.answer)
	else:
		for key in TTS_read_field:
			if TTS_read_field[key] == pkey:
				TTS_read(mw.currentCard.fact.get(key, 0))
				break
	evt.accept()
    return oldEventHandler(evt)

def GTTSredisplay(self):
        if (mw.state == 'showQuestion' and automaticQuestions) :
		TTS_read(mw.currentCard.question)
	elif (mw.state=='showAnswer' and automaticAnswers) :
        	TTS_read(mw.currentCard.answer)

oldEventHandler = mw.keyPressEvent
mw.keyPressEvent = newKeyPressEvent
view.View.redisplay = wrap(view.View.redisplay, GTTSredisplay,"after")


mw.registerPlugin("Google TTS", 0)
