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
__version__  = 'v0.8 beta 2'

import os
import sys
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
import re
from subprocess import call
import logging
import json

#Setup Logging File
logPath = os.path.expanduser('~/.local/log/')
if not os.path.exists(logPath):
	os.mkdir(logPath)
FORMAT = "[+] %(asctime)-15s %(message)s" #errorlog format
logging.basicConfig(filename = logPath+'optimus_laucher.log',level = logging.DEBUG,format=FORMAT)

jsonfile = '/etc/bumblebee/optimus_Database.json'
icon = '/usr/share/icons/optimus.png'

class OptimusJsonData:
	'''
		@OptimusJsonData
		- Read/Write data in json structure
	'''
	__data = None
	errorMsg = ''
	errorCode = False
	
	def __checkObject(self,jsonObject):
		#check JsonObject data is match with {'status':/value/,'apps':[{app1},{apps2}]
		if type(jsonObject) <> dict or jsonObject.keys() <> ['status','apps']:
			self.errorCode = True
			self.errorMsg = '[!] Wrong type data'
		elif jsonObject['status'] not in [0,1]:
			self.errorCode = True
			self.errorMsg = '[!] Wrong type status data'
		elif type(jsonObject['apps']) <> list:
			self.errorCode = True
			self.errorMsg = '[!] Wrong type apps data'
		else:
			if jsonObject['apps']:
				for i in jsonObject['apps']:
					if type(i) <> dict or i.keys() <> ['appicon', 'applink', 'appname']:
						self.errorCode = True
						self.errorMsg = '[!] Wrong type apps item data'
						break
	
	def update_JsonData(self,jsonObject):
		#update JsonData when jsonObject had changed
		self.__checkObject(jsonObject)
		if not self.errorCode:
			json_read_file = open(jsonfile,'w')
			text = json.dumps(jsonObject)
			json_read_file.write(text)
			json_read_file.close()
			self.errorCode = False
		else:
			self.errorMsg = '[!] Update Data was failed'
		return self.errorCode #errorCode = False whe code is raise error
	
	def get_JsonData(self):
		#get all JsonData from Json file
		result = {}
		json_read_file = open(jsonfile,'r')
		fread = json_read_file.read()
		json_read_file.close()
		if fread:#if file is not null
			self.__data = json.loads(fread) #convert to object
			self.__checkObject(self.__data) #check object
			if not self.errorCode: #not error
				result = self.__data #get object
		else:
			self.errorCode = True
			self.errorMsg = 'Empty data file !'
		return result

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
		#parse file details to appinfo which is a dict type
		appinfo = {}
		if file_name != '':
			fread = open(file_name,'r')
			data = fread.read()
			appinfo['applink'] = file_name
			d = re.findall(r'Name=(.+?)\n',data)
			if len(d) > 0 :
				appinfo['appname'] = d[0]
			d = re.findall(r'Icon=(.+?)\n',data)
			if len(d) > 0:
				appinfo['appicon'] = d[0]
		return appinfo
	
	#fix Edit_file
	def EditFile(self,applink):
		#edit applications to run optirun
		optimus_app = applink + '.optimus'
		#__run__ = check_primus()
		if os.path.exists (applink):
			call(['cp',applink,applink + '.save'])
			call(['cp',applink,optimus_app])
		#find line contains Exec=
		fread = open (applink,'r')
		data = fread.read().split('\n')
		num = []
		for line in range(len(data)):
			if re.search(r'Exec',data[line].split('=')[0].replace(' ','')):
				num.append(line)
		fread.close()
		#replace old Exec command 
		fwrite = open (optimus_app,'w')
		name = self.getFilename(applink)
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
		#get basename of file
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
		database = OptimusJsonData()
		self.data = database.get_JsonData()
		if self.data['status'] < 0:
			logging.error("[!] Not load status nvidia card")
			QMessageBox.question(self,'Error',"[!] Not load status nvidia card",QMessageBox.Ok)
			sys.exit(1)
		#load listview item
		self.lv = QListWidget()
		if len(self.data['apps']): #if self.appinfo_Data not 0
			for item in self.data['apps']:
				self.lv.addItem(item['appname'])
	
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
		
		if not self.data['status']:
			self.add.setEnabled(False)
			self.remove.setEnabled(False)
			self.lv.setVisible(False)
			self.radiobutton1.setChecked(False)
			self.radiobutton2.setChecked(True)
		elif self.data['status']:
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
		if self.data['status']:
			call(['optirun',glx_test])
		else:
			call([glx_test])
	
	def NvidiaMode(self):
		#This method allow program to change video mode of applications to nvidia 
		self.data['status'] = 1#set value
		#write data into database
		database = OptimusJsonData()
		if not database.update_JsonData(self.data):
			self.add.setEnabled(True)
			self.remove.setEnabled(True) 
				
			#change app.applink call nvidia card
			if self.data['apps']:
				for app in self.data['apps']:
					call(['cp',app['applink']+'.optimus',app['applink']])
				
			self.radiobutton1.setChecked(True)
			self.radiobutton2.setChecked(False)
		else:
			logging.error(database.errorMsg)
			QMessageBox.question(self,'Error',database.errorMsg,QMessageBox.Ok)
			self.data['status'] = 0 #reset value
			self.radiobutton1.setChecked(False)
			self.radiobutton2.setChecked(True)
		
	def IntelMode(self):
		self.data['status'] = 0#set value
		#write data into database
		database = OptimusJsonData()
		if not database.update_JsonData(self.data):
			#IntelMode method allow to change NvidiaMode to IntelMode
			self.add.setEnabled(False)
			self.remove.setEnabled(False)
				
			#change app.applink call intel card
			if self.data['apps']:
				for app in self.data['apps']:
					call(['cp',app['applink']+'.save',app['applink']])
			self.radiobutton1.setChecked(False)
			self.radiobutton2.setChecked(True)
		else:
			logging.error(database.errorMsg)
			QMessageBox.question(self,'Error',database.errorMsg,QMessageBox.Ok)
			self.data['status'] = 1 #reset value
			self.radiobutton1.setChecked(True)
			self.radiobutton2.setChecked(False)
	
	def AddProgram(self):
		#AddProgram, append an application to applications list
		#call FileDialog
		fname = str(QFileDialog.getOpenFileName(self, 'Add Program','/usr/share/applications/'))
		if fname:
			if os.path.exists(fname):
				optimusIO = OptimusIOConnection()
				database = OptimusJsonData()
				appinfo = optimusIO.parse_File_Object_To_AppInfo(fname)
				if type(appinfo) is dict and len(appinfo) == 3:
					#write new item to database
					self.data['apps'].append(appinfo)
					if not database.update_JsonData(self.data):
						#update ListView
						self.lv.addItem(appinfo['appname'])
						#edit file
						optimusIO.EditFile(appinfo['applink'])
						call(['cp',appinfo['applink']+'.optimus',appinfo['applink']])
					else:
						self.data['apps'].remove(appinfo)
						QMessageBox.question(self,'Error',database.errorMsg,QMessageBox.Ok)
						logging.error(database.errorMsg)
				else:
					msgErr = 'Error Value'
					QMessageBox.question(self,'Error',msgErr,QMessageBox.Ok)
					logging.error(msgErr)
			else:
				QMessageBox.question(self,'Alert','Error ! App doesn\'t exists',QMessageBox.Ok)

	#fix path app_name
	def RemoveProgram(self):
		#RemoveProgram, remove an application to applications list
		if self.item_choice:
			for item in self.data['apps']:
				if(item['appname'] == self.item_choice):
					diff = item
					self.data['apps'].remove(item)
					break
			# remove app
			database = OptimusJsonData()
			if not database.update_JsonData(self.data):
				self.lv.clear()
				for app in self.data['apps']:
					self.lv.addItem(app['appname'])
				if(os.path.exists(diff['applink']+'.save') and os.path.exists(diff['applink']+'.optimus')):
					os.remove(diff['applink'])
					call(['mv',diff['applink']+'.save',diff['applink']])
					os.remove(diff['applink']+'.optimus') 
				else:
					msgerr = 'Message : Application doesn\'t exists'
					logging.error(msgerr)
					QMessageBox.question(self,'Error',msgerr,QMessageBox.Ok)
			else:
				logging.error(database.errorMsg)
				QMessageBox.question(self,'Error',database.errorMsg,QMessageBox.Ok)
				self.data['apps'].append(diff) #restore item when delete item is error

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
	if not os.path.exists(jsonfile):
		fwrite = open(jsonfile,'w')
		data = {'status':0,'apps':[]}
		text = json.dumps(data)
		fwrite.write(text)
		fwrite.close()
	main()