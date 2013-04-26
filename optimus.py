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
__version__  = 'v0.8 alpha 2'

import os
import sys
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
import re
from subprocess import call
import logging

#Setup Logging File
logPath = os.path.expanduser('~/.local/log/')
if not os.path.exists(logPath):
	os.mkdir(logPath)
logging.basicConfig(filename = logPath+'optimus_laucher.log',level = logging.DEBUG)

database='/etc/bumblebee/bumblebee_database'
icon='/usr/share/icons/optimus.png'

# return '' if it's not contains filename
# /home/file.py return 
# /home/ return ''
basename = lambda file_name: file_name[(file_name.rindex('/') + 1) if '/' in file_name else 0:
					file_name.index('.') if '.' in file_name else 0]

class optimus_function:
	'''
		Class optimus_function
		- Provide method to read/write data from database
	'''
	def checkPrimus(self):
		#check if system has primusrun which is installed
		if os.path.exists('/usr/bin/primusrun'):
			return True
		else:
			return False

	def load_data(self): #load data from data
		black_list = ['@','#','$']#if first char of line is @ or #, not load this line
		list_data = [] #application is stored here
		option = '' #option
		bumblebee_mode = '' #bumblebee_mode
		f_open = open(database,'r')
		for line in f_open.read().split('\n'):
			if line != '':
				if line[0] not in black_list:
					list_data.append(line)
				elif line[0] == '@':
					option = line[1:]
		f_open.close()
		return (option,list_data)
	      
	#fix Edit_file
	def edit_file(self,file_name):
		#edit applications to run optirun
		app = file_name
		optimus_app = file_name + '.optimus'
		#__run__ = check_primus()
		if os.path.exists (app):
			call(['cp',app,app + '.save'])
			call(['cp',app,optimus_app])
		#find line contains Exec=
		f_open = open (app,'r')
		data = f_open.read().split('\n')
		num = []
		for line in range(len(data)):
			if re.search(r'Exec',data[line].split('=')[0].replace(' ','')):
				num.append(line)
		f_open.close()
		#replace old Exec command 
		f_open = open (optimus_app,'w')
		if basename(file_name) == 'nvidia-settings':
			execute = 'Exec=optirun %s -c :8' % (basename(file_name))
		else:
			execute = 'Exec=optirun %s %U' % (basename(file_name))
		for i in num:
			data[i] = execute
		#write new data to file
		for line in data:
			f_open.write(line+'\n')
		f_open.close()
	
	def update_database(self,data,header):
		#Update database method
		outfile = []
		outfile.extend(header)
		outfile.extend(data)
		fw = open(database,'w')
		for line in outfile:
			fw.write(line+'\n')
		fw.close()

class Optimus(QWidget): 
	'''
		Class Optimus
		- Build User Interface using PyQt4
		- Provide methods to listen event and solve event
	'''
	def __init__(self, *args):
		super(Optimus,self,*args).__init__()#overwrite parent class
		self.item_choice = ''
		self.SetupGui()
	
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
		
		if self.check == 'False':
			self.add.setEnabled(False)
			self.remove.setEnabled(False)
			self.lv.setVisible(False)
			self.radiobutton1.setChecked(False)
			self.radiobutton2.setChecked(True)
		elif self.check == 'True':
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

	def LoadData(self):
		#load configuration of program from database
		db = optimus_function().load_data()
		if(db):#if db contains values
			self.check = db[0] #load video mode
			if self.check in ['True','False']:
				self.header = [] #header
				self.list_data = db[1] #list_data load applications
				self.header.append('@'+self.check)#load video mode
				self.header.append('#nvidia-settings')
			else:
				QMessageBox.question(self,'Error','Mode Value Not Found',QMessageBox.Ok)
				logging.error('Mode Value Not Found')
				sys.exit(1)

			self.lv = QListWidget()
			if self.list_data:
				for item in self.list_data:
					self.lv.addItem(basename(item))
			else:
				logging.warning('Empty List Program')
		else:
			QMessageBox.question(self,'Error','Database doesn\'t loaded',QMessageBox.Ok)
			logging.error('Database doesn\'t loaded')
			sys.exit(1)
	
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
	    
		self.exitAction.triggered.connect(self.CloseEvent)
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
		if self.check == 'True':
			call(['optirun',glx_test])
		else:
			call([glx_test])
	
	#fix path
	def NvidiaMode(self):
		#This method allow program to change video mode of applications to nvidia 
		self.add.setEnabled(True)
		self.remove.setEnabled(True)
		  
		self.check = 'True'#reset value
		#load data from database
		if self.list_data:
			for app in self.list_data:
				call(['cp',app+'.optimus',app])
		try:
			self.header[0] = '@'+self.check #reset value
		except IndexError:
			logging.error('Error When Mode Value Not Found')
			sys.exit(1)
		self.radiobutton1.setChecked(True)
		self.radiobutton2.setChecked(False)
		#write data into file
		optimus_function().update_database(self.list_data,self.header)
		
	#fix path
	def IntelMode(self):
		#IntelMode method allow to change NvidiaMode to IntelMode
		self.add.setEnabled(False)
		self.remove.setEnabled(False)
		
		self.check = 'False'#reset value
		#load data from database
		if self.list_data:
			for app in self.list_data:
				call(['cp',app+'.save',app])
		try:
			self.header[0] = '@'+self.check
		except IndexError:
			logging.error('Error When Mode Value Not Found')
			sys.exit(1)
		self.radiobutton1.setChecked(False)
		self.radiobutton2.setChecked(True)
		#write data into database
		optimus_function().update_database(self.list_data,self.header)
	
	def AddProgram(self):
		#AddProgram, append an application to applications list
		#call FileDialog
		fname = str(QFileDialog.getOpenFileName(self, 'Add Program','/usr/share/applications/'))
		if fname:
			if os.path.exists(fname):
				app_name = basename(fname) #get basename
				self.list_data.append(fname) #append fill fname to applications list
				#update ListView
				self.lv.addItem(app_name)
				#write new item to database
				optimus_function().edit_file(fname)
				optimus_function().update_database(self.list_data,self.header)
				call(['cp',fname+'.optimus',fname])
			else:
				QMessageBox.question(self,'Alert','Error ! App doesn\'t exists',QMessageBox.Ok)

	#fix path app_name
	def RemoveProgram(self):
		#RemoveProgram, remove an application to applications list
		if self.item_choice:
			for i in xrange(len(self.list_data)):
				if(basename(self.list_data[i]) == self.item_choice):
					diff = self.list_data[i]
					self.list_data.remove(self.list_data[i])
					break
			# remove app
			self.lv.clear()
			for app in self.list_data:
				self.lv.addItem(basename(app))
			optimus_function().update_database(self.list_data,self.header)
			if(os.path.exists(diff+'.save') and os.path.exists(diff+'.optimus')):
				os.remove(diff)
				call(['mv',diff+'.save',diff])
				os.remove(diff+'.optimus')
		else:
			QMessageBox.question(self,'Alert','Error ! No Item Was Choosen',QMessageBox.Ok)

	def QuitProgram(self):
		optimus_function().update_database(self.list_data,self.header)
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
		data = '<h3>Bumblebee Optimus</h3><br /><b>Author:</b><i>%s</i><br /><b>Version: %d</b>' % (__author__,__version__)
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
	if not os.path.exists (database):
		f_open = open(database,'w')
		f_open.write('@False\n#nvidia-settings\n')
		f_open.close()
	main()
	#if program terminated -> update database