#!/usr/bin/python

"""
    Bumblebee Optimus

    Help to run program with nvidia card easily 
    
"""

__version__ = 'Peter Nguyen'
__author__  = 'v0.2 alpha'

import os
import sys
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
import string

##Define
database_link='/etc/bumblebee_database'
icon_link='/usr/share/icons/optimus.png'
autostart_link='~/.config/autostart/bumblebee-optimus.desktop'
__linkdefault__ = '/usr/share/applications/'
setting_file = '/etc/bumblebee_optimus_setting'

def load_data():
    list_data=[]
    f_open=open(os.path.expanduser(database_link),'r')
    for line in f_open.read().split('\n'):
	  try:
	    if line[0] != '#' and line !='':
	      list_data.append(line)
	  except IndexError:
	      pass
    f_open.close()
    return list_data

def Edit_File(App_name):
  app = __linkdefault__+App_name+'.desktop'
  optimus_app = __linkdefault__+App_name+'.desktop.optimus'
  if os.path.exists (app):
    os.system('cp '+app+' '+app+'.save')
    os.system('cp '+app+' '+optimus_app)    
    
    f_open = open (app,'r')
    data = f_open.read().split('\n')
    num=0
    for line in range(len(data)):
      if data[line].split('=')[0].replace(' ','') == 'Exec':
	num=line
    f_open.close()
    
    f_open = open (optimus_app,'w')
    if (App_name == 'nvidia-settings'):
	data[num] = 'Exec = optirun '+App_name+' -c :8'
    else:
	data[num] = 'Exec = optirun '+App_name+' %U' 
    for line in data:
      f_open.write(line+'\n')
    f_open.close()    

class Optimus(QWidget): 
    def __init__(self, *args):
	super(Optimus,self,*args).__init__()
	
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
        
        self.list_data=load_data()
        
        self.lv = QListWidget()
        for item in self.list_data:
	  self.lv.addItem(item)
	  
        self.remove = QPushButton('Remove Program',self)
        self.add = QPushButton('Add Program',self)
        self.Exit = QPushButton('Exit',self)
        self.radiobutton1 = QRadioButton('Enable Nvidia Mode')
        self.radiobutton2 = QRadioButton('Disable Nvidia Mode')
        
        f_open = open(setting_file,'r')
        data=f_open.read().split('\n')[0]
        f_open.close()
        
        if(data == 'False'):
	    self.add.setEnabled(False)
	    self.remove.setEnabled(False)
	    self.lv.setVisible(False)
	    self.radiobutton1.setChecked(False)
	    self.radiobutton2.setChecked(True)
	else:
	    self.lv.setVisible(True)
	    self.add.setEnabled(True)
	    self.remove.setEnabled(True)
	    self.radiobutton1.setChecked(True)
	    self.radiobutton2.setChecked(False)
        
        #layout settings
        mode = QHBoxLayout()
        mode.addStretch(1)
        mode.addWidget(self.radiobutton1)
        mode.addWidget(self.radiobutton2)
        
        button_layout=QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.add)
        button_layout.addWidget(self.remove)
        button_layout.addWidget(self.Exit)
        
        view_layout = QVBoxLayout()
        view_layout.addWidget(QLabel('Bumblebee Option: ',self))
        view_layout.addLayout(mode)
        view_layout.addWidget(self.lv)
        view_layout.addLayout(button_layout)
        self.setLayout(view_layout)
        
        self.lv.setVisible(True)
        #action
        self.item_choice=''
        #
        
        self.radiobutton1.clicked.connect(self.Change_Nvidia_Mode)
        self.radiobutton2.clicked.connect(self.Change_Intel_Mode)
        
        self.lv.itemActivated.connect(self.getItem)
        self.add.clicked.connect(self.add_program)
        self.remove.clicked.connect(self.remove_program)
        
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
    
    def add_program(self):
	 fname = QFileDialog.getOpenFileName(self, 'Add Program',__linkdefault__)
	 if str(fname) != '':
	      app_name = str(fname).split('.')[0]
	      app_name = app_name.split('/')[4]
	      self.list_data.append(app_name)
	      #update ListView
	      self.lv.addItem(app_name)
	      #write new item to database
	      f_write=open(os.path.expanduser(database_link),'a')
	      f_write.write(app_name+'\n')
	      f_write.close()
	 
	      Edit_File(app_name)
	      os.system('cp '+__linkdefault__+app_name+'.desktop.optimus'+' '+__linkdefault__+app_name+'.desktop')

    def getItem(self,item):
	      self.item_choice=item.text()
	      
    def remove_program(self):
	      if(self.item_choice != ''):
		  self.list_data.remove(self.item_choice)
		  
		  self.lv.clear()
		  for item in self.list_data:
		      self.lv.addItem(item)
		  #update database
		  write_change = open (os.path.expanduser(database_link),'w')
		  
		  for item in self.list_data:
		      write_change.write(item+'\n')
		      
		  write_change.close()
		  
		  os.remove(__linkdefault__+self.item_choice+'.desktop')
		  os.system('mv '+__linkdefault__+str(self.item_choice)+'.desktop.save'+' '+__linkdefault__+str(self.item_choice)+'.desktop')
		  os.remove(__linkdefault__+self.item_choice+'.desktop.optimus')
	      else:
		   QMessageBox.question(self,'Alert','Error ! No Item Was Choosen',QMessageBox.Ok)

    def Change_Nvidia_Mode(self):
	      self.add.setEnabled(True)
	      self.remove.setEnabled(True)
	      f_open = open(setting_file,'w')
	      f_open.write('True\n')
	      f_open.close()
	      for app in self.list_data:
		  os.system('cp '+__linkdefault__+app+'.desktop.optimus'+' '+__linkdefault__+app+'.desktop')

    def Change_Intel_Mode(self):
	      self.add.setEnabled(False)
	      self.remove.setEnabled(False)
	      f_open = open(setting_file,'w')
	      f_open.write('False\n')
	      f_open.close()
	      for app in self.list_data:
		  os.system('cp '+__linkdefault__+app+'.desktop.save'+' '+__linkdefault__+app+'.desktop')

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
    w.setWindowTitle('Bumblebee Optimus')
    w.show() 
    sys.exit(app.exec_()) 

if __name__ == "__main__":
    if not os.path.exists (database_link):
	f_open = open(database_link,'w')
	f_open.write('#Database')
	f_open.close()
    if not os.path.exists (setting_file):
	f_open = open(setting_file,'w')
	f_open.write('False')
	f_open.close()
    main()