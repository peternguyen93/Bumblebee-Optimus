#!/usr/bin/python

"""
    Bumblebee Optimus

    Help to run program with nvidia card easily
 
    Change Log:
	-> Chang GUI
	---> Add program button
	---> Remove program button
	
    Author: PeterNguyen
    Version : test 2
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
        #widget
        lm = ListModel(self.list_data, self)
        self.lv = QListView()
        self.lv.setModel(lm)

        remove = QPushButton("Remove Program",self)
        add = QPushButton("Add Program",self)
        # layout
        layout = QVBoxLayout()
        layout.addWidget(self.lv) 
        self.setLayout(layout)
        #layout
        button_layout=QVBoxLayout()
        layout.addWidget(add)
        layout.addWidget(remove)
        self.setLayout(button_layout)
        #action
        self.lv.doubleClicked.connect(self.run_program) #
        add.clicked.connect(self.add_program)
        remove.clicked.connect(self.remove_program)
   
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
		  QMessageBox.question(self,'Alert','Program was added',QMessageBox.Yes)
	else:
	      if ok:
		  QMessageBox.question(self,'Alert','Program isn\'t installed',QMessageBox.Yes)

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
		  QMessageBox.question(self,'Alert','Program was removed',QMessageBox.Yes)
	else:
	      if ok:
		  QMessageBox.question(self,'Alert','Error ......',QMessageBox.Yes)

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