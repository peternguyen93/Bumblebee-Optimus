#!/usr/bin/python

"""
    Bumblebee Optimus

    Help to run program with nvidia card easily 
"""

__version__ = 'Peter Nguyen'
__author__  = 'v0.4.1 released'

import os
import sys
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
import re
import subprocess

##Define
database_link='/etc/bumblebee/bumblebee_database'
icon_link='/usr/share/icons/optimus.png'
autostart_link='~/.config/autostart/bumblebee-optimus.desktop'

#Function 
basename = lambda file_name: file_name[file_name.rindex('/')+1:file_name.index('.')] 
#load data from database
def check_primus():#increate performance of nvidia card
	if os.path.exists('/usr/bin/primusrun'):
		return 'primusrun'
	else:
		return 'optirun'

def load_data(): #load data from data
	black_list = ['','@','#']
	list_data=[]
	f_open=open(os.path.expanduser(database_link),'r')
	for line in f_open.read().split('\n'):
		try:
			if line[0] not in black_list:
				list_data.append(line)
		except IndexError:
			pass
	f_open.close()
	return list_data

#change exec line to run with optirun
#fix Edit_file
def Edit_File(file_name):
	app = file_name
	optimus_app = file_name+'.optimus'
	#__run__ = check_primus()
	if os.path.exists (app):
		os.system('cp '+app+' '+app+'.save')
		os.system('cp '+app+' '+optimus_app)    
    
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

def update_database(value,data):
	data[1] = value #default line mode
	fw = fopen(database_link,'w')
	for line in data:
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
		aboutAction = menu.addAction('About')
		exitAction = menu.addAction('Exit')
		
		self.icon.setContextMenu(menu)
		self.icon.show()
		self.icon.setVisible(True)
		self.setWindowIcon(QIcon(icon_link))
		
		self.list_data=[basename(app) for app in load_data() if app != 'nvidia-settings']
		    
		self.lv = QListWidget()
		for item in self.list_data:
			self.lv.addItem(item)
	      
		self.remove = QPushButton('Remove Program',self)
		self.add = QPushButton('Add Program',self)
		self.test_graphic = QPushButton('Test Card',self)
		self.Exit = QPushButton('Exit',self)
		self.radiobutton1 = QRadioButton('Enable Nvidia Mode')
		self.radiobutton2 = QRadioButton('Enable OnBoard Mode')
		#self.radiobutton3 = QRadioButton('Enable Auto Mode')
		
		f_open = open(database_link,'r')
		self.check = ''
		for line in f_open.read().split('\n'):
			try:
				_re = re.search(r'@(\w+)',line)
				self.check = _re.group(1)
			except AttributeError:
				pass
		f_open.close()
	    
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
		mode.addStretch(1)
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
	    
	def closeEvent(self, event):
		self.hide()
		event.ignore()

	def activate(self,reason):
		if reason==3:
			self.show()
	
	def Test_Card(self):
		if os.path.exists('/usr/bin/glxspheres'):
			glx_test = 'glxspheres'
		elif os.path.exists('/usr/bin/glxgears'):
			glx_test = 'glxgears'
		else:
			QMessageBox.question(self,'Error','<h1> Check Your Mesa Package To Use This Function </h1>',QMessageBox.Ok)
			system.exit(1)

		if self.check == 'True':
			os.system('optirun '+glx_test)
		else:
			os.system(glx_test)
	
	def add_program(self):
		fname = str(QFileDialog.getOpenFileName(self, 'Add Program','/usr/share/applications/'))
		if fname:
			app_name = basename(fname) #basename
			self.list_data.append(app_name)
			#update ListView
			self.lv.addItem(app_name)
			#write new item to database
			f_write=open(os.path.expanduser(database_link),'a')
			f_write.write(fname+'\n')
			f_write.close()
		  
			Edit_File(fname)
			os.system('cp %s.optimus %s' % (fname,fname))

	def getItem(self,item):
			self.item_choice=item.text()
	#fix path app_name
	def remove_program(self):
		if(self.item_choice):
			self.list_data.remove(self.item_choice)
			
			self.lv.clear()
			for item in self.list_data:
				self.lv.addItem(item)
			#sync database
			d = [app for app in load_data() if app != 'nvidia-settings']
			for i in range(len(d)):
				if basename(d[i]) == self.item_choice:
					diff = d[i]
					break
			d.remove(diff)
			d.append('nvidia-settings')
			d.append('@True')
			d.append('#Database')
			d.reverse()
			write_change = open (os.path.expanduser(database_link),'w')
			for item in d:
				write_change.write(item+'\n')
			write_change.close()
			
			os.remove(diff)
			os.system('mv '+diff+'.save'+' '+diff)
			os.remove(diff+'.optimus')
		else:
			QMessageBox.question(self,'Alert','Error ! No Item Was Choosen',QMessageBox.Ok)
	#fix path
	def Change_Nvidia_Mode(self):
		self.add.setEnabled(True)
		self.remove.setEnabled(True)
		  
		self.check = 'True'
		#load data from database
		d = [app for app in load_data() if app != 'nvidia-settings']
		update_database('@True',d.append('nvidia-settings'))
		for app in d:
			os.system('cp '+app+'.optimus '+app)
	#fix path
	def Change_Intel_Mode(self):
		self.add.setEnabled(False)
		self.remove.setEnabled(False)
		
		self.check = 'False'
		#load data from database
		d = [app for app in load_data() if app != 'nvidia-settings']
		update_database('@False',d.append('nvidia-settings'))
		for app in d:
			os.system('cp '+app+'.save '+app)

	def enable_auto_start(self):
		if not(os.path.exists(os.path.expanduser(autostart_link))):
			os.system('cp /usr/share/applications/bumblebee-optimus.desktop ~/.config/autostart/')
			QMessageBox.question(self,'Alert','Auto Start is enabled',QMessageBox.Ok)
		else:
			QMessageBox.question(self,'Alert','Auto Start has been enabled',QMessageBox.Ok)
	
	def disable_auto_start(self):
		if os.path.exists(os.path.expanduser(autostart_link)):
			os.remove(autostart_link)
			QMessageBox.question(self,'Alert','Auto Start is disabled',QMessageBox.Ok)
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
		f_open.write('#Database\n@False\n')
		f_open.close()
	main()