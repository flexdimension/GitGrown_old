'''
Created on 2011/12/07

@author: unseon_pro
'''

from PySide.QtCore import *
from PySide.QtGui import QMainWindow, QVBoxLayout, QColor

from PySide.QtDeclarative import QDeclarativeView
from PythonModel import PythonModel
from DictListModel import DictListModel
from GitModel import GitModel

class GitPysideFrame(QMainWindow):
    '''
    classdocs
    '''


    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(GitPysideFrame, self).__init__(parent)
        
        layout = QVBoxLayout()
        
        self.view = QDeclarativeView(self)

        layout.addWidget(self.view)
        self.setLayout(layout)
        
        self.gm = GitModel()
        self.gm.connect('/Users/unseon_pro/myworks/RoughSketchpad')
        
        self.configModel = self.gm.getConfigModel()
        
        self.fileListModel = self.gm.getFileListModel()
        
        filePath = 'src/com/criticalmass/roughsketchpad/app/RsCanvas.py'
        self.fileViewModel = self.gm.getBlamedModel(filePath)
        self.commitListModel = self.gm.getCommitListModel(filePath)
        
        # Create an URL to the QML file
        url = QUrl('view.qml')
        # Set the QML file and show
        self.view.rootContext().setContextProperty('config', self.configModel)
        self.view.rootContext().setContextProperty('fileListModel', self.fileListModel)
        self.view.rootContext().setContextProperty('fileViewModel', self.fileViewModel)
        self.view.rootContext().setContextProperty('commitListModel', self.commitListModel)
        self.view.setResizeMode(QDeclarativeView.SizeRootObjectToView)

        
        self.view.setSource(url)
        
        root = self.view.rootObject()

        self.fileBrowser = root.findChild(QObject, "fileBrowser")
        self.blameView = root.findChild(QObject, "blameView")
        self.commitListView = root.findChild(QObject, "commitListView")

        