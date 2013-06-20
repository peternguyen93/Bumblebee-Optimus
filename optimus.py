#!/usr/bin/python

# Copyright (c) 2012- PeterNguyen <https://github.com/peternguyen93>
#
# Optimus Laucher is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Optimus Laucher.  If not, see <http://www.gnu.org/licenses/>.

__author__ = 'Peter Nguyen'
__version__  = 'v0.8 beta 1'

import os
import sys
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
import re
from subprocess import call
import logging
import sqlite3

#Setup Logging File
logPath = os.path.expanduser('~/.local/log/')
if not os.path.exists(logPath):
	os.mkdir(logPath)
FORMAT = "[+] %(asctime)-15s %(message)s"
logging.basicConfig(filename = logPath+'optimus_laucher.log',level = logging.DEBUG,format=FORMAT)

database = os.path.expanduser('~/.local/share/bumblebee/optimus_DataBase.db')
icon = '/usr/share/icons/optimus.png'

# return '' if it's not contains filename
# /home/file.py return 
# /home/ return ''

class AppInfo:
	'''
		@Appinfo structure
		appname
		applink
		appicon
	'''
	appname = ''
	applink = ''
	appicon = ''
	      
	def __init__(self,app_tuple = None):
		if not app_tuple:
			#do nothing, overload constructor
			pass
		elif type(app_tuple) is tuple and len(app_tuple) == 3:
			self.appname = app_tuple[0]
			self.applink = app_tuple[1]
			self.appicon = app_tuple[2]
	
	def toTuple(self):
		return (self.appname,self.applink,self.appicon)
	
	def isFull(self):
		if self.appname and self.applink and self.appicon:
			return True
		else:
			return False

class OptimusDatabase:
	"""
		@OptimusDatabase
		opening a connection to database
		allow method connection to database 
	"""
	__conn = None #private object
	messageError = '' #error code return
	def __init__(self):
		self.__conn = sqlite3.connect(database) #connect to database
		
	def insert_Appinfo(self,appinfo):
		isDone = False #code return
		c = self.__conn.cursor() #get current cursor in database
		if isinstance(appinfo,AppInfo):
			try:
				c.execute('INSERT INTO apps_info VALUES(?,?,?)',appinfo.toTuple())
				self.__conn.commit() #commit change
				isDone = True
			except sqlite3.DatabaseError as err:
				self.messageError = 'Message : %s' % (err.message)
		else:
			self.messageError = 'Message : Wrong type data'
		return isDone
		
	def delete_Appinfo(self,appname):
		isDone = False #code return
		c = self.__conn.cursor()#get current cursor in database
		try:
			c.execute('DELETE FROM apps_info WHERE appname=:app',{'app':appname})
			self.__conn.commit() #commit change
			isDone = True
		except sqlite3.DatabaseError as err:
			self.messageError = 'Message : %s' % (err.message)
		return isDone
	
	def get_Appinfo(self):
		result = [] #get result from database
		c = self.__conn.cursor()
		try:
			fetch = c.execute('SELECT * FROM apps_info')
			for line in fetch:
				result.append(AppInfo(line))
		except sqlite3.DatabaseError as err:
			self.messageError = 'Message : %s' % (err.message)
		return result
	
	def update_Status(self,status):
		isDone = False
		c = self.__conn.cursor() #get current cursor in database
		if type(status) is int:
			if status in [0,1]: #status has value must be 0 or 1
				try:
					c.execute('UPDATE status SET nvidia_status=%d' % status)
					self.__conn.commit() #commit change
					isDone = True
				except sqlite3.DatabaseError as err:
					self.messageError = 'Message : %s' % (err.message)
			else:
				self.messageError = 'Message : status value must be zero or one'
		else:
			self.messageError = 'Message : Wrong type data'
		return isDone
	 
	def get_Statusinfo(self):
		status = -1
		c = self.__conn.cursor()
		try:
			c.execute('SELECT nvidia_status FROM status LIMIT 1')
			status = c.fetchone()[0]
		except sqlite3.DatabaseError as err:
			self.messageError = 'Message : %s' % (err.message)
		return status
	
	def close_Database(self):
		self.__conn.close()

class OptimusIOConnection:
	'''
		@OptimusIOConnection
		- Provide method to read/write application.desktop
	'''
	def checkPrimus(self):
		#check if system has primusrun which is installed
		if os.path.exists('/usr/bin/primusrun'):
			return True
		else:
			return False
	
	def parse_File_Object_To_AppInfo(self,file_name):
		appinfo = AppInfo()
		if file_name != '':
			fread = open(file_name,'r')
			data = fread.read()
			appinfo.applink = file_name
			d = re.findall(r'Name=(.+?)\n',data)
			if len(d) > 0 :
				appinfo.appname = d[0]
			d = re.findall(r'Icon=(.+?)\n',data)
			if len(d) > 0:
				appinfo.appicon = d[0]
		return appinfo
	
	#fix Edit_file
	def EditFile(self,appinfo):
		#edit applications to run optirun
		optimus_app = appinfo.applink + '.optimus'
		#__run__ = check_primus()
		if os.path.exists (appinfo.applink):
			call(['cp',appinfo.applink,appinfo.applink + '.save'])
			call(['cp',appinfo.applink,optimus_app])
		#find line contains Exec=
		fread = open (appinfo.applink,'r')
		data = fread.read().split('\n')
		num = []
		for line in range(len(data)):
			if re.search(r'Exec',data[line].split('=')[0].replace(' ','')):
				num.append(line)
		fread.close()
		#replace old Exec command 
		fwrite = open (optimus_app,'w')
		name = self.getFilename(appinfo.applink)
		if name == 'nvidia-settings':
			execute = 'Exec=optirun nvidia-settings -c :8'
		else:
			execute = 'Exec=optirun '+name+' %U' 
		for i in num:
			data[i] = execute
		#write new data to file
		for line in data:
			fwrite.write(line+'\n')
		fwrite.close()
	
	def getFilename(self,filename):
		basename = os.path.basename(filename)
		name = ''
		if basename.index('.'):
			name = basename.split('.')[0]
		else:
			name = basename
		return name
	     
class Optimus(QWidget): 
	'''
		@Optimus
		- Build User Interface using PyQt4
		- Provide methods to listen event and solve event
	'''
	def __init__(self, *args):
		super(Optimus,self,*args).__init__()#overwrite parent class
		self.item_choice = ''
		self.SetupGui()
	
	def LoadData(self):
		#load configuration of program from database
		database = OptimusDatabase()
		self.appinfo_Data = database.get_Appinfo()
		self.status = database.get_Statusinfo()
		if self.status < 0:
			logging.error(database.messageError)
			QMessageBox.question(self,'Error',database.messageError,QMessageBox.Ok)
			sys.exit(1)
		database.close_Database()
		#load listview item
		self.lv = QListWidget()
		if len(self.appinfo_Data): #if self.appinfo_Data not 0
			for item in self.appinfo_Data:
				self.lv.addItem(item.appname)
	
	def SetupGui(self):
		# Setup GUI 
		self.LoadData()
		self.icon = QSystemTrayIcon(QIcon(icon),self)
		self.icon.isSystemTrayAvailable()
		
		#menu in system tray
		menu = QMenu()
		self.nvidia_mode = menu.addAction('Nvidia Mode')
		self.onboard_mode = menu.addAction('Onboard Mode')
		self.aboutAction = menu.addAction('About')
		self.exitAction = menu.addAction('Exit')
		
		self.icon.setContextMenu(menu)
		self.icon.show()
		self.icon.setVisible(True)
		self.setWindowIcon(QIcon(icon))
		
		#function button
		self.remove = QPushButton('Remove Program',self)
		self.add = QPushButton('Add Program',self)
		self.test_graphic = QPushButton('Test Video Card',self)
		self.exit = QPushButton('Exit',self)
		self.radiobutton1 = QRadioButton('Nvidia Mode')
		self.radiobutton2 = QRadioButton('Onboard Mode')
		self.radiobutton3 = QRadioButton('Optirun')
		
		if not self.status:
			self.add.setEnabled(False)
			self.remove.setEnabled(False)
			self.lv.setVisible(False)
			self.radiobutton1.setChecked(False)
			self.radiobutton2.setChecked(True)
		elif self.status:
			self.lv.setVisible(True)
			self.add.setEnabled(True)
			self.remove.setEnabled(True)
			self.radiobutton1.setChecked(True)
			self.radiobutton2.setChecked(False)
		
		#layout settings
		groupbox1 = QGroupBox('Video Card Mode:')
		video_mode = QHBoxLayout()
		video_mode.addWidget(self.radiobutton1)
		video_mode.addWidget(self.radiobutton2)
		groupbox1.setLayout(video_mode)
		
		option_view = QHBoxLayout()
		option_view.addWidget(groupbox1)
		
		button_layout=QHBoxLayout()
		button_layout.addWidget(self.add)
		button_layout.addWidget(self.remove)
		button_layout.addWidget(self.exit)
		
		view_layout = QVBoxLayout()
		view_layout.addLayout(option_view)
		view_layout.addWidget(self.lv)
		view_layout.addWidget(self.test_graphic)
		view_layout.addLayout(button_layout)
		self.setLayout(view_layout)
		
		self.lv.setVisible(True)
		#set Event
		self.SetEvent()
	
	def SetEvent(self):
		#Set Event of widget 
		self.radiobutton1.clicked.connect(self.NvidiaMode)
		self.radiobutton2.clicked.connect(self.IntelMode)
		
		self.lv.itemActivated.connect(self.GetItemChoice)
		self.add.clicked.connect(self.AddProgram)
		self.remove.clicked.connect(self.RemoveProgram)
		self.test_graphic.clicked.connect(self.VideoCardTest)
			
		self.icon.activated.connect(self.Activate)
		self.exit.clicked.connect(self.QuitProgram)
	    
		self.exitAction.triggered.connect(self.QuitProgram)
		self.aboutAction.triggered.connect(self.About)
		self.nvidia_mode.triggered.connect(self.NvidiaMode)
		self.onboard_mode.triggered.connect(self.IntelMode)
	
	def VideoCardTest(self):
		#Video Test Method provides a function allow test performance of video card
		if os.path.exists('/usr/bin/glxspheres'):
			glx_test = 'glxspheres'
		elif os.path.exists('/usr/bin/glxgears'):
			glx_test = 'glxgears'
		else:
			QMessageBox.question(self,'Error','<h1> Check Your Mesa Package To Use This Function </h1>'
			    ,QMessageBox.Ok)
		if self.status:
			call(['optirun',glx_test])
		else:
			call([glx_test])
	
	#fix path
	def NvidiaMode(self): #This method allow program to change video mode of applications to nvidia 
		self.status = 1#set value
		#write data into database
		database = OptimusDatabase()
		if database.update_Status(self.status):
			self.add.setEnabled(True)
			self.remove.setEnabled(True) 
			
			#change app.applink call nvidia card
			if self.appinfo_Data:
				for app in self.appinfo_Data:
					call(['cp',app.applink+'.optimus',app.applink])
			
			self.radiobutton1.setChecked(True)
			self.radiobutton2.setChecked(False)
		else:
			logging.error(database.messageError)
			QMessageBox.question(self,'Error',database.messageError,QMessageBox.Ok)
			self.status = 0 #reset value
			self.radiobutton1.setChecked(False)
			self.radiobutton2.setChecked(True)
		database.close_Database()
		
	#fix path
	def IntelMode(self):
		self.status = 0#set value
		#write data into database
		database = OptimusDatabase()
		if database.update_Status(self.status):
			#IntelMode method allow to change NvidiaMode to IntelMode
			self.add.setEnabled(False)
			self.remove.setEnabled(False)
			
			#change app.applink call intel card
			if self.appinfo_Data:
				for app in self.appinfo_Data:
					call(['cp',app.applink+'.save',app.applink])
			self.radiobutton1.setChecked(False)
			self.radiobutton2.setChecked(True)
			
		else:
			logging.error(database.messageError)
			QMessageBox.question(self,'Error',database.messageError,QMessageBox.Ok)
			self.status = 1 #reset value
			self.radiobutton1.setChecked(True)
			self.radiobutton2.setChecked(False)
		database.close_Database()
	
	def AddProgram(self):
		#AddProgram, append an application to applications list
		#call FileDialog
		fname = str(QFileDialog.getOpenFileName(self, 'Add Program','/usr/share/applications/'))
		if fname:
			if os.path.exists(fname):
				optimusIO = OptimusIOConnection()
				database = OptimusDatabase()
				appinfo = optimusIO.parse_File_Object_To_AppInfo(fname)
				if appinfo.isFull:
					#write new item to database
					if database.insert_Appinfo(appinfo):
						self.appinfo_Data.append(appinfo)
						#update ListView
						self.lv.addItem(appinfo.appname)
						#edit file
						optimusIO.EditFile(appinfo)
						call(['cp',appinfo.applink+'.optimus',appinfo.applink])
					else:
						QMessageBox.question(self,'Error',database.messageError,QMessageBox.Ok)
						logging.error(database.messageError)
				else:
					msgErr = 'Error Value'
					QMessageBox.question(self,'Error',msgErr,QMessageBox.Ok)
					logging.error(msgErr)
				database.close_Database()
			else:
				QMessageBox.question(self,'Alert','Error ! App doesn\'t exists',QMessageBox.Ok)

	#fix path app_name
	def RemoveProgram(self):
		#RemoveProgram, remove an application to applications list
		if self.item_choice:
			for item in self.appinfo_Data:
				if(item.appname == self.item_choice):
					diff = item
					self.appinfo_Data.remove(item)
					break
			# remove app
			database = OptimusDatabase()
			if database.delete_Appinfo(diff.appname):
				self.lv.clear()
				for app in self.appinfo_Data:
					self.lv.addItem(app.appname)
				if(os.path.exists(diff.applink+'.save') and os.path.exists(diff.applink+'.optimus')):
					os.remove(diff.applink)
					call(['mv',diff.applink+'.save',diff.applink])
					os.remove(diff.applink+'.optimus') 
				else:
					msgerr = 'Message : Application doesn\'t exists'
					logging.error(msgerr)
					QMessageBox.question(self,'Error',msgerr,QMessageBox.Ok)
			else:
				logging.error(database.messageError)
				QMessageBox.question(self,'Error',database.messageError,QMessageBox.Ok)
				self.appinfo_Data.append(diff) #restore item when delete item is error
			database.close_Database()
		else:
			QMessageBox.question(self,'Alert','Error ! No Item Was Choosen',QMessageBox.Ok)

	def QuitProgram(self):
		sys.exit(1)
	
	def CloseEvent(self, event):
		#disable button close and hide in system tray
		self.hide()
		event.ignore()

	def Activate(self,reason):
		#active system tray
		if reason == 3:
			self.show()

	def GetItemChoice(self,item):
		#choice item in listview
		self.item_choice = item.text()

	def About(self):
		data = '<h3>Bumblebee Optimus</h3><br /><b>Author:</b><i>%s</i><br /><b>Version: %s</b>' % (__author__,__version__)
		QMessageBox.question(self,'About',data,QMessageBox.Ok)

def main():
	#main function run GUI
	app = QApplication(sys.argv) 
	w = Optimus() 
	w.setWindowTitle('Optimus Laucher')
	w.show() 
	sys.exit(app.exec_())

#run app
if __name__ == "__main__":
	main()
	#if program terminated -> update database