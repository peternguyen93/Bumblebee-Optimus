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
	
    Author: PeterNguyen
    Version : testing 3
"""

import os
import sys
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 

class Optimus(QWidget): 
    def __init__(self, *args): 
        QWidget.__init__(self, *args) 

        # load program     
        self.list_data=[]
        f_open=open(os.path.expanduser('~/.config/bumblebee_database'),'r')
        for line in f_open.read().split('\n'):
	  try:
	    if line[0] != '#' and line !='':
	      self.list_data.append(line)
	  except IndexError:
	      pass
        f_open.close()
        
        self.icon=QSystemTrayIcon(QIcon('/usr/share/icons/optimus.png'),self)
        self.icon.isSystemTrayAvailable()
        
        menu = QMenu()
        setting_menu = menu.addMenu('Setting')
        enable_autostart = setting_menu.addAction('Enable Auto Start')
        disable_autostart = setting_menu.addAction('Disable Auto Start')
        aboutAction = menu.addAction('About')
	exitAction = menu.addAction('Exit')
	
	self.icon.setContextMenu(menu)
        self.icon.show()
        self.icon.setVisible(True)
        self.setWindowIcon(QIcon('/usr/share/icons/optimus.png'))
        
        #widget
        lm = ListModel(self.list_data, self)
        self.lv = QListView()
        self.lv.setModel(lm)

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
        self.lv.doubleClicked.connect(self.run_program) #
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
	os.system('optirun '+str(item.data().toString())+' &') #call bumblebee
    
    def add_program(self):
	text, ok = QInputDialog.getText(self, 'Add Program','Enter New Program:')
	if(os.path.exists('/usr/bin/'+str(text)) and self.list_data.count(str(text)) == 0):
	      self.list_data.append(str(text))
	      #update ListView
	      lm=ListModel(self.list_data,self)
	      self.lv.setModel(lm)
	      
	      #write new item to database
	      f_write=open(os.path.expanduser('~/.config/bumblebee_database'),'a')
	      f_write.write(str(text)+'\n')
	      f_write.close()
	      
	      if ok:
		  QMessageBox.question(self,'Alert','Program was added',QMessageBox.Ok)
	else:
	      if ok:
		  QMessageBox.question(self,'Alert','Program isn\'t installed',QMessageBox.Ok)

    def remove_program(self):
	text, ok = QInputDialog.getText(self, 'Remove Program','Enter Program:')
	
	if self.list_data.count(str(text)) == 1:
	      self.list_data.remove(str(text))
	      #update ListView
	      lm=ListModel(self.list_data,self)
	      self.lv.setModel(lm)
	      
	      #write database
	      f_write=open(os.path.expanduser('~/.config/bumblebee_database'),'w')
	      for line in self.list_data:
		f_write.write(line+'\n')
	      f_write.close()
	      
	      if ok:
		  QMessageBox.question(self,'Alert','Program was removed',QMessageBox.Ok)
	else:
	      if ok:
		  QMessageBox.question(self,'Alert','Error ......',QMessageBox.Ok)

    def enable_auto_start(self):
	    if not(os.path.exists('~/.config/autostart/bumblebee-optimus.desktop')):
		os.system('cp /usr/share/applications/bumblebee-optimus.desktop ~/.config/autostart/')
		QMessageBox.question(self,'Alert','Auto Start is enabled',QMessageBox.Ok)
	    else:
		QMessageBox.question(self,'Alert','Auto Start has been enabled',QMessageBox.Ok)
    
    def disable_auto_start(self):
	    if os.path.exists('~/.config/autostart/bumblebee-optimus.desktop'):
		os.system('rm ~/.config/autostart/bumblebee-optimus.desktop')
		QMessageBox.question(self,'Alert','Auto Start is disabled',QMessageBox.Ok)
	    else:
		QMessageBox.question(self,'Alert','Auto Start has been disabled',QMessageBox.Ok)
   
    def about_form(self):
	    data='<h3>Bumblebee Optimus</h3><br /><b>Author:</b><i>Peter Nguyen</i><br /><b>Version: testing</b>'
	    QMessageBox.question(self,'About',data,QMessageBox.Ok)

class ListModel(QAbstractListModel): 
    def __init__(self, datain, parent=None, *args): 
        QAbstractListModel.__init__(self, parent, *args) 
        self.list_data = datain
 
    def rowCount(self, parent=QModelIndex()): 
        return len(self.list_data) 
 
    def data(self, index, role): 
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(self.list_data[index.row()])
        else: 
            return QVariant()

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
	   f_new.write('nvidia-settings -c :8 \n')
	   f_new.close()
    main()