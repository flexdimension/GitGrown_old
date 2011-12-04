#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import sys
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import QDeclarativeView
from PythonModel import PythonModel
 
# Create Qt application and the QDeclarative view
app = QApplication(sys.argv)
view = QDeclarativeView()


items = [['aaa','111'],['bbb','222'],['ccc','333']]
roles = ['name','num']
model = PythonModel(items, roles)

# Create an URL to the QML file
url = QUrl('view.qml')
# Set the QML file and show
view.rootContext().setContextProperty("model2", model)

view.setSource(url)
view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
view.show()
# Enter Qt main loop
sys.exit(app.exec_())
