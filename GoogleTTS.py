# -*- coding: utf-8 -*-
# Author:  Arthur Helfstein Fragoso
# Email: arthur@life.net.br
# Based on: "hello-world plugin", "aprendiendoTTS" and "Japanese Support"
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
#   GoogleTTS plugin
version = '0.1.3'
#
#   Any problems, comments, please post in this thread:  (or email me)
#
#   http://groups.google.com/group/ankisrs/browse_thread/thread/98177e2770659b31
#
#  Edited on Tuesday, 24 April 2012  
#  
########################### Instructions #######################################
#
# MP3 Mass Generator - Generate many mp3 files at once (like magic) :D
#
# go to the Cards/Facts Browser, select the cards to get the mp3 file generated,
# and go to the menu "Action" > "GoogleTTS MP3 Mass Generator"
#
# really easy ;)
#
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
automaticAnswers = False                         # disable the automatic recite
#automaticAnswers = TTS_tags_only                 # recite only [GTTS::] tags in the Answers as it appears
#automaticAnswers = TTS_if_no_tag_read_whole      # always recite the whole, but if there is a [GTTS::], it will only read the tags


#
# Keys to get the fields pronounced, case sensitive
# uncomment and change in a way that works for you,
# you can add as many as you want
# examples:
#TTS_read_field['Field Name'] =  Qt.Key_F9
#TTS_read_field['Front'] =  Qt.Key_F5
#TTS_read_field['Back'] = Qt.Key_F6
#TTS_read_field['Reading'] =  Qt.Key_F7
#TTS_read_field['Text'] = Qt.Key_F8
#all the available keys are in http://doc.trolltech.com/qtjambi-4.4/html/com/trolltech/qt/core/Qt.Key.html

# quote (encode) special characters for mp3 file names:
# Windows users should have their mp3 files quoted (True), if you want to try, the system encoding should be the same as the language you are learning. and in the Table slanguage, the right charset should be set there. (it may not work, do this only if you know what you are doing. If you want it really want it, install Linux! :D
# Unix users don't need to quote (encode) special characters. so you can set it as False if you want.
# it will work alright sync with AnkiMobile, but it won't work with AnkiWeb
quote_mp3 = True	# spC3A9cial.mp3 E381AFE38184.mp3 E4BDA0E5A5BD.mp3
#quote_mp3 = False  # spécial.mp3 はい.mp3　你好.mp3


#subprocessing is enabled by default
# on MS Windows XP or older, there is a bug of cutting the ending of a speech occasionally, so you may want to desable it.
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
['cs', 'Czech',	'cp1250'], #or iso-8859-2
['da', 'Danish',	'cp1252'], #or iso-8859-1
['nl', 'Dutch',	'cp1252'], #or iso-8859-1
['en', 'English',	'cp1252'], #or iso-8859-1
['fi', 'Finnish',	'cp1252'], #or iso-8859-1
['fr', 'French',	'cp1252'], #or iso-8859-1
['de', 'German',	'cp1252'], #or iso-8859-1
['el', 'Greek',	'cp1253'], #or iso-8859-7
['ht', 'Haitian Creole',	'cp1252'], #or iso-8859-1
['hi', 'Hindi',	'cp1252'], #or iso-8859-1
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
['cy', 'Welsh',	'iso-8859-14']]


#Address to the TTS service
TTS_ADDRESS = 'http://translate.google.com/translate_tts'

######################### End of Settings ##################################
import os, subprocess, re, sys, urllib
from ankiqt import mw
from anki import sound
from anki.sound import playFromText
from anki.utils import stripHTML
from anki.facts import Fact
from subprocess import Popen, PIPE, STDOUT
from urllib import quote_plus
from ankiqt.ui import view,facteditor,utils
from anki.hooks import wrap
from PyQt4 import QtGui,QtCore
from PyQt4.QtGui import *
from PyQt4.QtSvg import *


language_generator = TTS_language
file_max_length = 255 #filename max length for Unix

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
	


###########  TTS_read to recite the tts on-the-fly

def TTS_read(text, language=TTS_language):
	text = re.sub("\[sound:.*?\]", "", stripHTML(text.replace("\n", "")).encode('utf-8'))
	address = TTS_ADDRESS+'?tl='+language+'&q='+ quote_plus(text)
	#utils.showInfo(address)
	if subprocess.mswindows:
		param = ['mplayer.exe', '-ao', 'win32', '-slave', '-user-agent', "'Mozilla/5.0'", address]
		if subprocessing:
			subprocess.Popen(param, startupinfo=si, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
		else:
			subprocess.Popen(param, startupinfo=si, stdin=PIPE, stdout=PIPE, stderr=STDOUT).communicate()
	else:
		param = ['mplayer', '-slave', '-user-agent', "'Mozilla/5.0'", address]
		if subprocessing:
			subprocess.Popen(param, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
		else:
			subprocess.Popen(param, stdin=PIPE, stdout=PIPE, stderr=STDOUT).communicate()


###################  TTS_record to generate MP3 files



def TTS_record(text, language=TTS_language):
	text = re.sub("\[sound:.*?\]", "", stripHTML(text.replace("\n", "")).encode('utf-8'))
	address = TTS_ADDRESS+'?tl='+language+'&q='+ quote_plus(text)
	if quote_mp3: #re.sub removes \/:*?"<>|[]. from the file name
		file = quote_plus(re.sub('[\\\/\:\*\?"<>|\[\]\.]*', "",text)).replace("%", "")+'.mp3'
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




############################ MP3 File Generator


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
	GoogleTTS.setToolTip(_("GoogleTTS :: MP3 File Generator"))
	GoogleTTS.setShortcut(_("Ctrl+g"))
	GoogleTTS.setFocusPolicy(Qt.NoFocus)
	#GoogleTTS.setEnabled(False)
	self.iconsBox.addWidget(GoogleTTS)
	GoogleTTS.setStyle(self.plastiqueStyle)


facteditor.FactEditor.setupFields = wrap(facteditor.FactEditor.setupFields, GTTS_Fact_edit_setupFields,"after")
GTTS_Fact_edit_setupFields(mw.editor)




#################### TTS in Tool's menu

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


####################  MP3 Mass Generator


srcField = -1
dstField = -1
generate_sound_tags = True


class GTTS_mp3_mass_generator_Dialog(object):
	def setupUi(self, Dialog):
		Dialog.setObjectName("Dialog")
		Dialog.resize(400, 300)
		Dialog.setWindowTitle("GoogleTTS :: MP3 Mass Generator")

		buttonBox = QDialogButtonBox(Dialog);
		buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32));
		buttonBox.setOrientation(QtCore.Qt.Horizontal);
		buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok|QtGui.QDialogButtonBox.Cancel);
		verticalLayoutWidget = QtGui.QWidget(Dialog);
		verticalLayoutWidget.setGeometry(QtCore.QRect(20, 70, 357, 171));
		verticalLayout = QtGui.QVBoxLayout(verticalLayoutWidget);
		verticalLayout.setContentsMargins(0, 0, 0, 0);
		label_2 = QtGui.QLabel(verticalLayoutWidget);
		label_2.setText("GoogleTTS will generate MP3 files to all selected facts.");

		verticalLayout.addWidget(label_2);

		self.factkeys = mw.deck.allFields()


		formLayoutWidget = QtGui.QWidget(Dialog)
		formLayoutWidget.setGeometry(QtCore.QRect(20, 60, 329, 118));
		formLayout = QtGui.QFormLayout(formLayoutWidget);
		#formLayout.setFieldGrowthPolicy(QFormLayout::AllNonFixedFieldsGrow);
		formLayout.setContentsMargins(0, 0, 0, 0);



		languageLabel = QtGui.QLabel(formLayoutWidget)
		languageLabel.setText("Language")
		formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, languageLabel)
		self.languageComboBox = QtGui.QComboBox(formLayoutWidget)
		self.languageComboBox.addItems([d[1] for d in slanguages])
		self.languageComboBox.setCurrentIndex(get_language_id(TTS_language))
		formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.languageComboBox)


		sourceFieldLabel = QtGui.QLabel(formLayoutWidget)
		sourceFieldLabel.setText("Source Field")
		formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, sourceFieldLabel)
		self.sourceFieldComboBox = QtGui.QComboBox(formLayoutWidget)
		self.sourceFieldComboBox.addItems([d for d in self.factkeys])
		self.sourceFieldComboBox.setCurrentIndex(srcField)
		formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.sourceFieldComboBox)


		destinationFieldLabel = QtGui.QLabel(formLayoutWidget)
		destinationFieldLabel.setText("Destination Field")
		formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, destinationFieldLabel)
		self.destinationFieldComboBox = QtGui.QComboBox(formLayoutWidget)
		self.destinationFieldComboBox.addItems([d for d in self.factkeys])
		self.destinationFieldComboBox.setCurrentIndex(dstField)
		formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.destinationFieldComboBox)


		self.checkBox = QtGui.QCheckBox(Dialog)
		self.checkBox.setText("Generate sound file path within the [sound:] tag.")
		if generate_sound_tags:
			self.checkBox.setChecked(True)

		label = QtGui.QLabel(verticalLayoutWidget);
		label.setText("It will overwrite anything in the Destination Field. Make sure to select the right field. It may take a while.");
		label.setWordWrap(True);

		verticalLayout.addWidget(formLayoutWidget);
		verticalLayout.addWidget(self.checkBox);
		verticalLayout.addWidget(label);

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

def generate_audio_files(factIds, language, srcField_name, dstField_name, generate_sound_tags):
	mw.deck.startProgress(max=len(factIds))
	for c, id in enumerate(factIds):
		mw.deck.updateProgress(label="Generating MP3...", value=c)
		fact = mw.deck.s.query(Fact).get(id)
		try:
			if generate_sound_tags:
				fact[dstField_name] = '[sound:'+ TTS_record(fact[srcField_name], language) +']'
			else:
				fact[dstField_name] = TTS_record(fact[srcField_name], language)
		except:
			pass
	try:
		mw.deck.refreshSession()
	except:
		# old style
		mw.deck.refresh()
	mw.deck.updateCardQACacheFromIds(factIds, type="facts")
	mw.deck.finishProgress()

def setupMenu(editor):
	a = QAction("GoogleTTS MP3 Mass Generator", editor)
	a.setIcon(QtGui.QIcon(":/icons/speaker.png"))
	editor.connect(a, SIGNAL("triggered()"), lambda e=editor: onGenerate(e))
	editor.dialog.menuActions.addSeparator()
	editor.dialog.menuActions.addAction(a)

def onGenerate(editor):
	global TTS_language, dstField, srcField, generate_sound_tags
	n = "Generate MP3 files"
	d = QDialog()
	form = GTTS_mp3_mass_generator_Dialog()
	form.setupUi(d)
	if d.exec_():		
		TTS_language = slanguages[form.languageComboBox.currentIndex()][0]
		srcField = form.sourceFieldComboBox.currentIndex()
		dstField = form.destinationFieldComboBox.currentIndex()
		generate_sound_tags = form.checkBox.isChecked()
		if srcField != -1 and dstField != -1 :
			editor.parent.setProgressParent(editor)
			editor.deck.setUndoStart(n)
			generate_audio_files(editor.selectedFacts(), TTS_language, form.factkeys[srcField], form.factkeys[dstField], generate_sound_tags)
			editor.deck.setUndoEnd(n)
			editor.parent.setProgressParent(None)
			editor.updateSearch()
		else:
			utils.showInfo("You should select the Source and Destination Field!")

from anki.hooks import addHook
addHook("editor.setupMenus", setupMenu)


######################################### Keys and Redisplay

## Check pressed key
def newKeyPressEvent(evt):
	pkey = evt.key()
	if (mw.state == 'showAnswer' or mw.state == 'showQuestion'):
		if (pkey == TTS_KEY_Q):
			playTTSFromText(mw.currentCard.question)  #read the GTTS tags
		elif (pkey == TTS_KEY_Q_ALL):
			if re.findall("\[GTTS:(.*?):(.*?)\]", mw.currentCard.question, re.M|re.I):
				playTTSFromText(mw.currentCard.question) #read the GTTS tags
			else:
				TTS_read(mw.currentCard.question,TTS_language) #read the the whole field
		elif (mw.state=='showAnswer' and pkey == TTS_KEY_A):
			playTTSFromText(mw.currentCard.answer) #read the GTTS tags
		elif (mw.state=='showAnswer' and pkey == TTS_KEY_A_ALL):
			if re.findall("\[GTTS:(.*?):(.*?)\]", mw.currentCard.answer, re.M|re.I):
				playTTSFromText(mw.currentCard.answer) #read the GTTS tags
			else:
				TTS_read(mw.currentCard.answer,TTS_language)  #read the the whole field
		else:
			for key in TTS_read_field:
				if TTS_read_field[key] == pkey:

					TTS_read(mw.currentCard.fact.get(key, 0),TTS_language)
					break
	evt.accept()
	return oldEventHandler(evt)


def GTTSredisplay(self):
	if mw.state == 'showQuestion' or mw.state == 'showAnswer':
		if mw.state == 'showQuestion':
			toread = mw.currentCard.question
			automatic = automaticQuestions
		else:
			toread = mw.currentCard.answer
			automatic = automaticAnswers
		if not sound.hasSound(toread):
			if automatic == TTS_tags_only:
				playTTSFromText(toread)
			if automatic == TTS_if_no_tag_read_whole:
				if re.findall("\[GTTS:(.*?):(.*?)\]", toread, re.M|re.I):
					playTTSFromText(toread)
				else:
					TTS_read(toread,TTS_language)

oldEventHandler = mw.keyPressEvent
mw.keyPressEvent = newKeyPressEvent


view.View.redisplay = wrap(view.View.redisplay, GTTSredisplay,"after")



mw.registerPlugin("Google TTS", 0)



