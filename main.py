#!/usr/bin/python
# -*- coding: utf-8 -*-
 
import sys
from PySide.QtCore import *
from PySide.QtGui import QApplication

from GitGrownFrame import GitGrownFrame
 
# Create Qt application and the QDeclarative view
app = QApplication(sys.argv)
view = GitGrownFrame()
view.resize(1000, 800)


view.show()


# Enter Qt main loop
sys.exit(app.exec_())
