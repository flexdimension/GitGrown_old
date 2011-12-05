#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import QDeclarativeView
from PythonModel import PythonModel
from DictListModel import DictListModel
from GitModel import GitModel
 
# Create Qt application and the QDeclarative view
app = QApplication(sys.argv)
view = QDeclarativeView()


#items = [['aaa','111'],['bbb','222'],['ccc','333']]
#roles = ['name','num']
#model = PythonModel(items, roles)

gm = GitModel()
gm.connect('/Users/unseon_pro/myworks/RoughSketchpad')
model = PythonModel(gm.getConfigItems(), gm.getConfigRoles())
fileListModel = DictListModel(gm.getFileList())

filePath = 'src/com/criticalmass/roughsketchpad/app/RsCanvas.py'
fileViewModel = PythonModel(gm.getBlamedModel(filePath),\
                            gm.getBlamedRoles())
# Create an URL to the QML file
url = QUrl('view.qml')
# Set the QML file and show
view.rootContext().setContextProperty('model2', model)
view.rootContext().setContextProperty('fileListModel', fileListModel)
view.rootContext().setContextProperty('fileViewModel', fileViewModel)


view.setSource(url)
view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
view.show()
# Enter Qt main loop
sys.exit(app.exec_())
