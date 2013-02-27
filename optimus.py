#!/usr/bin/python

"""
    Bumblebee Optimus

    Help to run program with nvidia card easily 
"""

__author__ = 'Peter Nguyen'
__version__  = 'v0.6.1 released'

import os
import sys
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
import re
from subprocess import call

database_link='/etc/bumblebee/bumblebee_database'
icon_link='/usr/share/icons/optimus.png'
autostart_link='~/.config/autostart/bumblebee-optimus.desktop'
#Function 
basename = lambda file_name: file_name[file_name.rindex('/')+1:file_name.index('.')] 
#load data from database
class optimus_function:
	def load_data(self): #load data from data
		black_list = ['@','#']
		list_data=[]
		option = ''
		f_open=open(database_link,'r')
		for line in f_open.read().split('\n'):
			if(line != ''):
				if(line[0] not in black_list):
					list_data.append(line)
				elif(line[0]=='@'):
					option = line
		f_open.close()
		return (option[1:],list_data)
	#change exec line to run with optirun
	#fix Edit_file
	def edit_file(self,file_name):
		app = file_name
		optimus_app = file_name+'.optimus'
		#__run__ = check_primus()
		if os.path.exists (app):
			call(['cp',app,app+'.save'])
			call(['cp',app,optimus_app])
	    
		f_open = open (app,'r')
		data = f_open.read().split('\n')
		num = []
		for line in range(len(data)):
			if re.search(r'Exec',data[line].split('=')[0].replace(' ','')):
				num.append(line)
		f_open.close()
    
		f_open = open (optimus_app,'w')
		if (basename(file_name) == 'nvidia-settings'):
			_exec_ = 'Exec=optirun '+basename(file_name)+' -c :8'
		else:
			_exec_ = 'Exec=optirun '+basename(file_name)+' %U'
		for i in num:
			data[i] = _exec_
		for line in data:
			f_open.write(line+'\n')
		f_open.close()

	def update_database(self,value,data):
		outfile = []
		if(value != None):
			outfile.append(value)
		outfile.extend(data)
		outfile.append('#nvidia-settings')
		fw = open(database_link,'w')
		for line in outfile:
			fw.write(line+'\n')
		fw.close()

class Optimus(QWidget): 
	def __init__(self, *args):
		super(Optimus,self,*args).__init__()
		self.item_choice=''
		self.SetupGui()
	    
	def SetupGui(self):
		self.icon=QSystemTrayIcon(QIcon(icon_link),self)
		self.icon.isSystemTrayAvailable()
		
		menu = QMenu()
		setting_menu = menu.addMenu('Settings')
		enable_autostart = setting_menu.addAction('Enable Auto Start')
		disable_autostart = setting_menu.addAction('Disable Auto Start')
		nvidia_mode = menu.addAction('Nvidia Mode')
		onboard_mode = menu.addAction('Onboard Mode')
		aboutAction = menu.addAction('About')
		exitAction = menu.addAction('Exit')
		
		self.icon.setContextMenu(menu)
		self.icon.show()
		self.icon.setVisible(True)
		self.setWindowIcon(QIcon(icon_link))
		
		db = optimus_function().load_data()
		self.list_data = db[1]
		self.lv = QListWidget()
		if(self.list_data):
			for item in self.list_data:
				self.lv.addItem(basename(item))
	      
		self.remove = QPushButton('Remove Program',self)
		self.add = QPushButton('Add Program',self)
		self.test_graphic = QPushButton('Test Video Card',self)
		self.Exit = QPushButton('Exit',self)
		self.radiobutton1 = QRadioButton('Nvidia Mode')
		self.radiobutton2 = QRadioButton('OnBoard Mode')
		#self.radiobutton3 = QRadioButton('Enable Auto Mode')
		
		self.check = db[0]
	    
		if(self.check == 'False'):
			self.add.setEnabled(False)
			self.remove.setEnabled(False)
			self.lv.setVisible(False)
			self.radiobutton1.setChecked(False)
			self.radiobutton2.setChecked(True)
			#self.radiobutton3.setChecked(False)
		elif (self.check == 'True'):
			self.lv.setVisible(True)
			self.add.setEnabled(True)
			self.remove.setEnabled(True)
			self.radiobutton1.setChecked(True)
			self.radiobutton2.setChecked(False)
			#self.radiobutton3.setChecked(False)
		#else:
			#self.radiobutton3.setChecked(True)
		#layout settings
		mode = QHBoxLayout()
		mode.addWidget(self.radiobutton1)
		mode.addWidget(self.radiobutton2)
		#mode.addWidget(self.radiobutton3)
		
		button_layout=QHBoxLayout()
		button_layout.addStretch(1)
		button_layout.addWidget(self.add)
		button_layout.addWidget(self.remove)
		button_layout.addWidget(self.Exit)
		
		view_layout = QVBoxLayout()
		view_layout.addWidget(QLabel('Bumblebee Option: ',self))
		view_layout.addLayout(mode)
		view_layout.addWidget(self.lv)
		view_layout.addWidget(self.test_graphic)
		view_layout.addLayout(button_layout)
		self.setLayout(view_layout)
		
		self.lv.setVisible(True)
		#action
		
		self.radiobutton1.clicked.connect(self.Change_Nvidia_Mode)
		self.radiobutton2.clicked.connect(self.Change_Intel_Mode)
		#self.radiobutton3.clicked.connect(self.Auto_Mode)
			
		self.lv.itemActivated.connect(self.getItem)
		self.add.clicked.connect(self.add_program)
		self.remove.clicked.connect(self.remove_program)
		self.test_graphic.clicked.connect(self.Test_Card)
			
		self.icon.activated.connect(self.activate)
		self.Exit.clicked.connect(QCoreApplication.instance().quit)
	    
		exitAction.triggered.connect(qApp.quit)
		aboutAction.triggered.connect(self.about_form)
		enable_autostart.triggered.connect(self.enable_auto_start)
		disable_autostart.triggered.connect(self.disable_auto_start)
		nvidia_mode.triggered.connect(self.Change_Nvidia_Mode)
		onboard_mode.triggered.connect(self.Change_Intel_Mode)
	    
	def closeEvent(self, event):
		self.hide()
		event.ignore()

	def activate(self,reason):
		if reason==3:
			self.show()

	def getItem(self,item):
			self.item_choice=item.text()
	
	def Test_Card(self):
		if os.path.exists('/usr/bin/glxspheres'):
			glx_test = 'glxspheres'
		elif os.path.exists('/usr/bin/glxgears'):
			glx_test = 'glxgears'
		else:
			QMessageBox.question(self,'Error','<h1> Check Your Mesa Package To Use This Function </h1>',QMessageBox.Ok)
			system.exit(1)
		if self.check == 'True':
			call(['optirun',glx_test])
		else:
			call([glx_test])
	
	#fix path
	def Change_Nvidia_Mode(self):
		self.add.setEnabled(True)
		self.remove.setEnabled(True)
		  
		self.check = 'True'
		#load data from database
		for app in self.list_data:
			call(['cp',app+'.optimus',app])
		optimus_function().update_database('@True',self.list_data)
		self.radiobutton1.setChecked(True)
		self.radiobutton2.setChecked(False)
	#fix path
	def Change_Intel_Mode(self):
		self.add.setEnabled(False)
		self.remove.setEnabled(False)
		
		self.check = 'False'
		#load data from database
		for app in self.list_data:
			call(['cp',app+'.save',app])
		optimus_function().update_database('@False',self.list_data)
		self.radiobutton1.setChecked(False)
		self.radiobutton2.setChecked(True)
	
	def add_program(self):
		fname = str(QFileDialog.getOpenFileName(self, 'Add Program','/usr/share/applications/'))
		if (fname):
			if (os.path.exists(fname)):
				app_name = basename(fname) #basename
				self.list_data.append(fname)
				#update ListView
				self.lv.addItem(app_name)
				#write new item to database
				optimus_function().update_database('@True',self.list_data)
				optimus_function().edit_file(fname)
				os.system('cp %s.optimus %s' % (fname,fname))
			else:
				QMessageBox.question(self,'Alert','Error ! App doesn\'t exists',QMessageBox.Ok)

	#fix path app_name
	def remove_program(self):
		if(self.item_choice):
			for i in xrange(len(self.list_data)):
				if basename(self.list_data[i]) == self.item_choice:
					diff = self.list_data[i]
					self.list_data.remove(self.list_data[i])
					break
			#update ListWidget
			self.lv.clear()
			for app in self.list_data:
				self.lv.addItem(basename(app))
			optimus_function().update_database('@True',self.list_data)
			if(os.path.exists(diff+'.save') and os.path.exists(diff+'.optimus')):
				os.remove(diff)
				call(['mv',diff+'.save',diff])
				os.remove(diff+'.optimus')
		else:
			QMessageBox.question(self,'Alert','Error ! No Item Was Choosen',QMessageBox.Ok)
	#other function
	def enable_auto_start(self):
		if not(os.path.exists(os.path.expanduser(autostart_link))):
			os.system('cp /usr/share/applications/bumblebee-optimus.desktop ~/.config/autostart/')
			QMessageBox.question(self,'Alert','Auto Start was enabled',QMessageBox.Ok)
		else:
			QMessageBox.question(self,'Alert','Auto Start has been enabled',QMessageBox.Ok)
	
	def disable_auto_start(self):
		if os.path.exists(os.path.expanduser(autostart_link)):
			os.remove(autostart_link)
			QMessageBox.question(self,'Alert','Auto Start was disabled',QMessageBox.Ok)
		else:
			QMessageBox.question(self,'Alert','Auto Start has been disabled',QMessageBox.Ok)
      
	def about_form(self):
		data='<h3>Bumblebee Optimus</h3><br /><b>Author:</b><i>'+__author__+'</i><br /><b>Version: '+__version__+'</b>'
		QMessageBox.question(self,'About',data,QMessageBox.Ok)

def main():
	app = QApplication(sys.argv) 
	w = Optimus() 
	w.setWindowTitle('Bumblebee Optimus Laucher')
	w.show() 
	sys.exit(app.exec_()) 

if __name__ == "__main__":
	if not os.path.exists (database_link):
		f_open = open(database_link,'a')
		f_open.write('#Database\n@False\n#nvidia-settings\n')
		f_open.close()
	main()