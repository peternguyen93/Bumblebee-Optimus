#!/usr/bin/python

"""
    Bumblebee Optimus

    Help to run program with nvidia card easily
 
    Change Log:
	---> Change GUI
	---> Add program button
	---> Remove program button
	---> Add system tray
	---> Add Auto Start
	---> Fix Bug
	---> Fix Enable AutoStart
    Change Log v0.1:
	---> Update GUI
	---> Update ,Fix Add / Remove Button
	--->Fix Bug

    Author: PeterNguyen
    Version : 0.1
"""

import os
import sys
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 

##Define
database_link='~/.config/bumblebee_database'
icon_link='/usr/share/icons/optimus.png'
autostart_link='~/.config/autostart/bumblebee-optimus.desktop'

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

class Optimus(QWidget): 
    def __init__(self, *args): 
        QWidget.__init__(self, *args)  
        
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

        remove = QPushButton('Remove Program',self)
        add = QPushButton('Add Program',self)
        Exit = QPushButton('Exit',self)
        # layout
        button_layout=QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(add)
        button_layout.addWidget(remove)
        button_layout.addWidget(Exit)
        
        view_layout = QVBoxLayout()
        view_layout.addWidget(self.lv)
        view_layout.addLayout(button_layout)
        self.setLayout(view_layout)
        #action
        self.item_choice=''
        #
        self.lv.doubleClicked.connect(self.run_program)
        self.lv.itemActivated.connect(self.getItem)
        add.clicked.connect(self.add_program)
        remove.clicked.connect(self.remove_program)
        
        self.icon.activated.connect(self.activate)
        Exit.clicked.connect(QCoreApplication.instance().quit)
    
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
                
    def run_program(self,item):
	if str(item.data().toString()) == 'nvidia-settings':
	      prefix=' -c :8 &'
	else:
	      prefix=' &'
	os.system('optirun '+str(item.data().toString())+prefix) #call bumblebee
    
    def add_program(self):
	text, ok = QInputDialog.getText(self, 'Add Program','Enter New Program:')
	if(os.path.exists('/usr/bin/'+str(text)) and self.list_data.count(str(text)) == 0):
	      self.list_data.append(str(text))
	      #update ListView
	      self.lv.addItem(str(text))
	      #write new item to database
	      f_write=open(os.path.expanduser(database_link),'a')
	      f_write.write(str(text)+'\n')
	      f_write.close()
	else:
	      if ok:
		  QMessageBox.question(self,'Alert','Program isn\'t installed',QMessageBox.Ok)

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
	      else:
		   QMessageBox.question(self,'Alert','Error ! No Item Was Choosen',QMessageBox.Ok)

    def enable_auto_start(self):
	    if not(os.path.exists(os.path.expanduser(autostart_link))):
		os.system('cp /usr/share/applications/bumblebee-optimus.desktop ~/.config/autostart/')
		QMessageBox.question(self,'Alert','Auto Start is enabled',QMessageBox.Ok)
	    else:
		QMessageBox.question(self,'Alert','Auto Start has been enabled',QMessageBox.Ok)
    
    def disable_auto_start(self):
	    if os.path.exists(os.path.expanduser(autostart_link)):
		os.system('rm '+autostart_link)
		QMessageBox.question(self,'Alert','Auto Start is disabled',QMessageBox.Ok)
	    else:
		QMessageBox.question(self,'Alert','Auto Start has been disabled',QMessageBox.Ok)
   
    def about_form(self):
	    data='<h3>Bumblebee Optimus</h3><br /><b>Author:</b><i>Peter Nguyen</i><br /><b>Version: 0.1</b>'
	    QMessageBox.question(self,'About',data,QMessageBox.Ok)

def main():
    
    app = QApplication(sys.argv) 
    w = Optimus() 
    w.setWindowTitle('Bumblebee Optimus')
    w.show() 
    sys.exit(app.exec_()) 

if __name__ == "__main__":
    #First Run
    if not (os.path.exists(os.path.expanduser('~/.config/bumblebee_database'))):
	   f_new = open(os.path.expanduser('~/.config/bumblebee_database'),'a')
	   f_new.write('# Bumblebee Database \n')
	   f_new.write('nvidia-settings\n')
	   if os.path.exists ('/usr/bin/vlc'):
	      f_new.write('vlc\n')
	   elif os.path.exists ('/usr/bin/firefox'):
	      f_new.write('firefox\n')
	   elif os.path.exists ('/usr/bin/chromium'):
	      f_new.write('chromium')
	   elif os.path.exists('/usr/bin/chromium-browser'): #for Fedora
	      f_new.write('chromium-browser')
	   elif os.path.exists('/usr/bin/totem'):
	      f_new.write('totem')
	   elif os.path.exists('/usr/bin/smplayer'):
	      f_new.write('smplayer')
	   f_new.close()
    main()