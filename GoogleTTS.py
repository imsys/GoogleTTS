# -*- coding: utf-8 -*-
# Author:  Arthur Helfstein Fragoso
# Email: arthur@life.net.br
# Based on: "hello-world plugin" and "aprendiendoTTS"
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
#   GoogleTTS plugin

########################### Settings #######################################

from PyQt4.QtCore import *
# the KEY to press to get the answer pronounced
TTS_KEY_A=Qt.Key_F4
# the KEY to press to get the question pronounced
TTS_KEY_Q=Qt.Key_F3

#The player that will be executed by the Operation System
#in might work in windows I didn't try, you probably needs the full pach C:/..../mplayer.exe
TTS_player = 'mplayer'
#Language code
TTS_language = 'en'

"""
Supported Languages

Good:
en - English
fr - French
de - German
ht - Haitian Creole
hi - Hindi
it - Italian
es - Spanish

Wierd robotic voices:
af - Afrikaans 
sq - Albanian
hy - Armenian
ca - Catalan
zh - Chinese - only pinyin with numbers (ni3hao3)
hr - Croatian
cs - Czech
da - Danish
nl - Dutch
fi - Finnish
el - Greek
hu - Hungarian
is - Icelandic
id - Indonesian
lv - Latvian
mk - Macedonian
no - Norwegian
pl - Polish
pt - Portuguese
ro - Romanian
ru - Russian
sr - Serbian
sk - Slovak
sw - Swahili
sv - Swedish
tr - Turkish
vi - Vietnamese
cy - Welsh
"""


######################### End of Settings ##################################
import os, subprocess
from ankiqt import mw
from ankiqt.ui import utils
from anki.utils import stripHTML
from subprocess import Popen

def newKeyPressEvent(evt):
    if (mw.state == 'showAnswer' or mw.state == 'showQuestion'):
	if (evt.key() == TTS_KEY_Q):
		subprocess.Popen([TTS_player, 'http://translate.google.com/translate_tts?tl='+TTS_language+'&q="'+ stripHTML(mw.currentCard.question) +'"'])
	elif (mw.state=='showAnswer' and evt.key() == TTS_KEY_A):
		subprocess.Popen([TTS_player, 'http://translate.google.com/translate_tts?tl='+TTS_language+'&q="'+ stripHTML(mw.currentCard.answer) +'"'])
	evt.accept()
    return oldEventHandler(evt)

oldEventHandler = mw.keyPressEvent
mw.keyPressEvent = newKeyPressEvent

mw.registerPlugin("Google TTS", 0)
