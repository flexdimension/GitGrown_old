#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import sys
from PySide.QtCore import *
from PySide.QtGui import QApplication

from GitPysideFrame import GitPysideFrame
 
# Create Qt application and the QDeclarative view
app = QApplication(sys.argv)
view = GitPysideFrame()
view.resize(800, 600)


view.show()


# Enter Qt main loop
sys.exit(app.exec_())
