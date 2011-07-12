# -*- coding: utf-8 -*-
# Author:  Arthur Helfstein Fragoso
# Email: arthur@life.net.br
# Based on: "hello-world plugin" and "aprendiendoTTS"
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
#   GoogleTTS plugin
version = '0.0.11'
#
#   Any problems, comments, please post in this thread:  (or email me)
#
#   http://groups.google.com/group/ankisrs/browse_thread/thread/98177e2770659b31
#
#  Edited on Saturday, 29 January
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

# quote (encode) special characters for mp3 file names:
# Windows users should have their mp3 files quoted (True), if you want to try, the system encoding should be the same as the language you are learning. and in the Table slanguage, the right charset should be set there. (it may not work, do this only if you know what you are doing. If you want it really want it, install Linux! :D
# Unix users don't need to quote (encode) special characters. so you can set it as False if you want.
# it will work alright sync with AnkiMobile, but it won't work with AnkiWeb
quote_mp3 = True	# sp%C3%A9cial.mp3 %E3%81%AF%E3%81%84.mp3 %E4%BD%A0%E5%A5%BD.mp3
#quote_mp3 = False  # spécial.mp3 はい.mp3　你好.mp3


#subprocessing is disabled by default on MS Windows,
#if you enable it (true), it *may or may not* result in a bug of cut the ending of a speech occasionally
#if it's disable(false), Anki will be frozen while GoogleTTS is reciting the speech. 
#so you can try if you want. For Unix users, it works normally with subprocessing, you can just ignore it.
MSwin_subprocess = False
#MSwin_subprocess = True

#Language code
TTS_language = 'en'


#Supported Languages       
# code , Language, windows charset encoding
slanguages = [['af', 'Afrikaans'],
['sq', 'Albanian'],
['ar', 'Arabic', 'cp1256'],
['hy', 'Armenian', 'armscii-8'],
['ca', 'Catalan'],
['zh', 'Chinese', 'cp936'],
['hr', 'Croatian'],
['cs', 'Czech'],
['da', 'Danish'],
['nl', 'Dutch'],
['en', 'English'],
['fi', 'Finnish'],
['fr', 'French'],
['de', 'German'],
['el', 'Greek', 'cp1253'],
['ht', 'Haitian Creole'],
['hi', 'Hindi'],
['hu', 'Hungarian'],
['is', 'Icelandic'],
['id', 'Indonesian'],
['it', 'Italian'],
['ja', 'Japanese', 'cp932'],
['ko', 'Korean', 'cp949'],
['la', 'Latin'],
['lv', 'Latvian'],
['mk', 'Macedonian'],
['no', 'Norwegian'],
['pl', 'Polish'],
['pt', 'Portuguese'],
['ro', 'Romanian'],
['ru', 'Russian', 'cp1251'],
['sr', 'Serbian'],
['sk', 'Slovak'],
['es', 'Spanish'],
['sw', 'Swahili'],
['sv', 'Swedish'],
['tr', 'Turkish', 'cp1254'],
['vi', 'Vietnamese', 'cp1258'],
['cy', 'Welsh']]


######################### End of Settings ##################################
import os, subprocess, re, sys
from ankiqt import mw
from anki import sound
from anki.utils import stripHTML
from subprocess import Popen, PIPE, STDOUT
from urllib import quote_plus
from ankiqt.ui import view,facteditor,utils
from anki.hooks import wrap
from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import *
from PyQt4.QtSvg import *

language_generator = TTS_language
file_max_length = 255 #filename max length for Unix

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

def get_language_id(language_code):
	x = 0
	for d in slanguages:
		if d[0]==language_code:
			return x
		x = x + 1

def TTS_read(text, language=TTS_language):
	text = re.sub("\[sound:.*?\]", "", stripHTML(text.encode('utf-8').replace("\n", "")))
	address = 'http://translate.google.com/translate_tts?tl='+language+'&q='+ quote_plus(text)
	if subprocess.mswindows:
		if MSwin_subprocess:
			subprocess.Popen(['mplayer.exe', '-ao', 'win32', '-slave', '-user-agent', "'Mozilla/5.0'", address], startupinfo=si, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
		else:
			subprocess.Popen(['mplayer.exe', '-ao', 'win32', '-slave', '-user-agent', "'Mozilla/5.0'", address], startupinfo=si, stdin=PIPE, stdout=PIPE, stderr=STDOUT).communicate()
	else:
		subprocess.Popen(['mplayer', '-slave', '-user-agent', "'Mozilla/5.0'", address], stdin=PIPE, stdout=PIPE, stderr=STDOUT)


def TTS_record(text, language=TTS_language):
	text = re.sub("\[sound:.*?\]", "", stripHTML(text.encode('utf-8').replace("\n", "")))
	address = 'http://translate.google.com/translate_tts?tl='+language+'&q='+ quote_plus(text)
	if quote_mp3: #re.sub removes \/:*?"<>|[]. from the file name
		file = quote_plus(re.sub('[\\\/\:\*\?"<>|\[\]\.]*', "",text))+'.mp3'
		if len(file) > file_max_length:
			file = file[0:file_max_length-4] +'.mp3'
	else:
		file = re.sub('[\\\/\:\*\?"<>|\[\]\.]*', "",text)+'.mp3'
		if len(file) > file_max_length:
			file = file[0:file_max_length-4] +'.mp3'
		if subprocess.mswindows:
			file = file.decode('utf-8').encode(slanguages[get_language_id(language)][2])
	if subprocess.mswindows:
		subprocess.Popen(['mplayer.exe', '-ao', 'win32', '-slave', '-user-agent', "'Mozilla/5.0'", address, '-dumpstream', '-dumpfile', file], startupinfo=si, stdin=PIPE, stdout=PIPE, stderr=STDOUT).wait()
		if not quote_mp3:
			return file.decode(slanguages[get_language_id(language)][2])
	else:
		subprocess.Popen(['mplayer', '-slave', '-user-agent', "'Mozilla/5.0'", address, '-dumpstream', '-dumpfile', file], stdin=PIPE, stdout=PIPE, stderr=STDOUT).wait()
	return file.decode('utf-8')


## Check pressed key
def newKeyPressEvent(evt):
	pkey = evt.key()
	if (mw.state == 'showAnswer' or mw.state == 'showQuestion'):
		if (pkey == TTS_KEY_Q):
			TTS_read(mw.currentCard.question,TTS_language)
		elif (mw.state=='showAnswer' and pkey == TTS_KEY_A):
			TTS_read(mw.currentCard.answer,TTS_language)
		else:
			for key in TTS_read_field:
				if TTS_read_field[key] == pkey:
					TTS_read(mw.currentCard.fact.get(key, 0),TTS_language)
					break
	evt.accept()
	return oldEventHandler(evt)

def GTTSredisplay(self):
	if (mw.state == 'showQuestion' and automaticQuestions) :
		TTS_read(mw.currentCard.question,TTS_language)
	elif (mw.state=='showAnswer' and automaticAnswers) :
		TTS_read(mw.currentCard.answer,TTS_language)

oldEventHandler = mw.keyPressEvent
mw.keyPressEvent = newKeyPressEvent
view.View.redisplay = wrap(view.View.redisplay, GTTSredisplay,"after")




class Ui_Dialog1(object):
	def setupUi(self, Dialog, factedit):
		Dialog.setObjectName("Dialog")
		Dialog.resize(400, 300)
		Dialog.setWindowTitle("GoogleTTS :: MP3 File Generator")
		self.gridLayout = QtGui.QGridLayout(Dialog)
		self.gridLayout.setContentsMargins(10, 10, 10, 10)
		self.comboboxlabel = QtGui.QLabel(Dialog)
		self.comboboxlabel.setText("Language:")
		self.combobox = QtGui.QComboBox()
		self.combobox.addItems([d[1] for d in slanguages])
		self.combobox.setCurrentIndex(get_language_id(language_generator))
		self.textEditlabel = QtGui.QLabel(Dialog)
		self.textEditlabel.setText("Text:")
		self.charleft = QtGui.QLabel(Dialog)
		self.charleft.setText("Characters left: 100")
		self.charleft.setToolTip(_("GoogleTTS can read up to 100 characters, no more than that, sorry :'("))
		self.textEdit = QtGui.QTextEdit(Dialog)
		self.textEdit.setAcceptRichText(False)
		self.textEdit.setObjectName("textEdit")

		self.gridLayout.addWidget(self.comboboxlabel, 0, 0, 1, 1)
		self.gridLayout.addWidget(self.combobox, 1, 0, 1, 1)
		self.gridLayout.addWidget(self.textEditlabel, 0, 1, 1, 1)
		self.gridLayout.addWidget(self.charleft, 0, 2, 1, 1)
		self.gridLayout.addWidget(self.textEdit, 1, 1, 1, 2)
		self.buttonBox = QtGui.QDialogButtonBox(Dialog)
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel)
		self.buttonBox.setObjectName("buttonBox")
		self.gridLayout.addWidget(self.buttonBox, 3, 1, 1, 3)
		self.previewbutton = QtGui.QPushButton(Dialog)
		self.previewbutton.setObjectName("preview")
		self.previewbutton.setText("Preview")
		self.gridLayout.addWidget(self.previewbutton, 2, 1, 1, 2)

		QtCore.QObject.connect(self.textEdit, QtCore.SIGNAL("textChanged()"), lambda self=self: self.charleft.setText("Characters left: "+ str(100-len(unicode(self.textEdit.toPlainText()).encode('utf-8')))))
		QtCore.QObject.connect(self.previewbutton, QtCore.SIGNAL("clicked()"), lambda self=self: TTS_read(unicode(self.textEdit.toPlainText()), slanguages[self.combobox.currentIndex()][0]))
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
		QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
		QtCore.QMetaObject.connectSlotsByName(Dialog)


def GTTS_Factedit_button(self):
	global language_generator
	self.initMedia()
	w = self.focusedEdit()
	if w:
		self.saveFields()
		cur = w.textCursor()
		pos = cur.position()
		d = QDialog(self.parent)
		form = Ui_Dialog1()
		form.setupUi(d, self)
		
		if d.exec_():
				  language_generator = slanguages[form.combobox.currentIndex()][0]
				  file = TTS_record(unicode(form.textEdit.toPlainText()), language_generator)
				  self._addSound(file, widget=w, copy=False)
				  #cur.setPosition(-1)
				  #w.setTextCursor(cur)
				  self.saveFields()

def GTTS_Fact_edit_setupFields(self):
	GoogleTTS = QPushButton(self.widget)
	GoogleTTS.setFixedHeight(20)
	GoogleTTS.setFixedWidth(20)
	GoogleTTS.setCheckable(True)
	GoogleTTS.connect(GoogleTTS, SIGNAL("clicked()"), lambda self=self: GTTS_Factedit_button(self))
	GoogleTTS.setIcon(QIcon(":/icons/speaker.png"))
	GoogleTTS.setToolTip(_("GoogleTTS :: MP3 File Generator (Ctrl+g)"))
	GoogleTTS.setShortcut(_("Ctrl+g"))
	GoogleTTS.setFocusPolicy(Qt.NoFocus)
	#GoogleTTS.setEnabled(False)
	self.iconsBox.addWidget(GoogleTTS)
	GoogleTTS.setStyle(self.plastiqueStyle)


facteditor.FactEditor.setupFields = wrap(facteditor.FactEditor.setupFields, GTTS_Fact_edit_setupFields,"after")
GTTS_Fact_edit_setupFields(mw.editor)




class GTTS_option_menu_Dialog(object):
	def setupUi(self, Dialog):
		Dialog.setObjectName("Dialog")
		Dialog.resize(400, 300)
		Dialog.setWindowTitle("GoogleTTS")

		buttonBox = QDialogButtonBox(Dialog);
		buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32));
		buttonBox.setOrientation(QtCore.Qt.Horizontal);
		buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel);
		verticalLayoutWidget = QtGui.QWidget(Dialog);
		verticalLayoutWidget.setGeometry(QtCore.QRect(20, 70, 357, 151));
		verticalLayout = QtGui.QVBoxLayout(verticalLayoutWidget);
		verticalLayout.setContentsMargins(0, 0, 0, 0);
		label_2 = QtGui.QLabel(verticalLayoutWidget);
		label_2.setText("Choose the language that will be used by GoogleTTS");

		verticalLayout.addWidget(label_2);

		self.combobox = QtGui.QComboBox(verticalLayoutWidget);
		self.combobox.addItems([d[1] for d in slanguages])
		self.combobox.setCurrentIndex(get_language_id(TTS_language))

		verticalLayout.addWidget(self.combobox);

		label = QtGui.QLabel(verticalLayoutWidget);
		label.setText("This will be reset when you close Anki. For a permanent change, you have to edit the GoogleTTS.py file.");
		label.setWordWrap(True);

		verticalLayout.addWidget(label)

		label_3 = QtGui.QLabel(Dialog)
		label_3.setGeometry(QtCore.QRect(100, 10, 200, 51))
		label_3.setText("GoogleTTS")
		font = QtGui.QFont()
		font.setBold(True)
		font.setPointSize(27)
		label_3.setFont(font)
		label_4 = QtGui.QLabel(Dialog)
		label_4.setGeometry(QtCore.QRect(190, 50, 111, 17))
		label_4.setText("Version "+version)

		QtCore.QObject.connect(buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
		QtCore.QObject.connect(buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
		QtCore.QMetaObject.connectSlotsByName(Dialog)



def GTTS_option_menu():
	global TTS_language
	d = QDialog()
	form = GTTS_option_menu_Dialog()
	form.setupUi(d)
	if d.exec_():
		TTS_language = slanguages[form.combobox.currentIndex()][0]


mw.mainWin.GoogleTTS = QtGui.QAction('GoogleTTS', mw)
mw.mainWin.GoogleTTS.setStatusTip('GoogleTTS')
mw.mainWin.GoogleTTS.setEnabled(True)
mw.mainWin.GoogleTTS.setIcon(QtGui.QIcon(":/icons/speaker.png"))
mw.connect(mw.mainWin.GoogleTTS, QtCore.SIGNAL('triggered()'), GTTS_option_menu)
mw.mainWin.menuTools.addAction(mw.mainWin.GoogleTTS)



mw.registerPlugin("Google TTS", 0)



