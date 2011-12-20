'''
Created on 2011/12/07

@author: unseon_pro
'''

from PySide.QtCore import *
from PySide.QtGui import QMainWindow, QVBoxLayout, QColor

from PySide.QtDeclarative import QDeclarativeView
from PyListModel import PyListModel
from DictListModel import DictListModel
from GitModel import GitModel

class GitPysideFrame(QMainWindow):
    '''
    classdocs
    '''

    @Slot(int)
    def onSelectedPathChanged(self, index) :
        print "onSelectedPathChanged is called"
        filePath = self.fileListModel.selectedValue
        obj = self.gm.getFileList()[index]
        
        if obj['type'] == 'blob' :
            self.fileViewModel = self.gm.getBlamedModel('HEAD', filePath)
            self.commitListModel = self.gm.getCommitListModel(filePath)
        elif obj['type'] ==  'tree':
            self.fileViewModel = None
            self.commitListModel = self.gm.getCommitListModel(filePath, 'dir')
        else :
            pass #error!!!!!
            
        rootContect = self.view.rootContext()
        rootContect.setContextProperty('fileViewModel', self.fileViewModel)
        rootContect.setContextProperty('commitListModel', self.commitListModel)
        self.commitListModel.selectionChanged.connect(self.onSelectedCommitChanged)
        self.commitListView.setProperty('currentIndex', 0)
        
        if obj['type'] == 'blob' :
            print "currentCommit is " + self.commitListModel.items[0][0]
            self.blameView.setProperty('currentCommit', self.commitListModel.items[0][0])

    @Slot(int)
    def onSelectedCommitChanged(self, index):
        print "onSelectedCommitChanged is called"
        sha = self.commitListModel.selectedValue
        filePath = self.fileListModel.selectedValue
        fileIndex = self.fileListModel.selectedIndex
        obj = self.gm.getFileList()[fileIndex]
        if obj['type'] == 'blob' :
            self.fileViewModel = self.gm.getBlamedModel(sha, filePath)
            rootContect = self.view.rootContext()
            rootContect.setContextProperty('fileViewModel', self.fileViewModel)
            self.blameView.setProperty('currentCommit', sha)
            print "blame model is changed"
        
        

    def __init__(self, parent = None) :
        '''
        Constructor
        '''
        super(GitPysideFrame, self).__init__(parent)
        
        layout = QVBoxLayout()
        
        self.view = QDeclarativeView(self)

        layout.addWidget(self.view)
        self.setLayout(layout)
        
        self.gm = GitModel()
        #self.gm.connect('/Users/unseon_pro/myworks/RoughSketchpad')
        self.gm.connect('.')
        
        self.configModel = self.gm.getConfigModel()
        
        self.fileListModel = self.gm.getFileListModel()
        self.fileListModel.selectionChanged.connect(self.onSelectedPathChanged)
        
        self.fileViewModel = None
        self.commitListModel = self.gm.getCommitListModel('', 'tree')
        self.commitListModel.selectionChanged.connect(self.onSelectedCommitChanged)
        
        self.branchGraphModel = self.gm.getBranchGraphs()
        
        # Create an URL to the QML file
        url = QUrl('view.qml')
        # Set the QML file and show
        
        rootContect = self.view.rootContext()
        #rootContect.setContextProperty('rootFrame', self)
        rootContect.setContextProperty('config', self.configModel)
        rootContect.setContextProperty('fileListModel', self.fileListModel)
        rootContect.setContextProperty('fileViewModel', self.fileViewModel)
        rootContect.setContextProperty('commitListModel', self.commitListModel)
        rootContect.setContextProperty('branchGraphModel', self.branchGraphModel)
        #self.view.setResizeMode(QDeclarativeView.SizeRootObjectToView)

        
        self.view.setSource(url)
        
        root = self.view.rootObject()

        self.fileBrowser = root.findChild(QObject, "fileBrowser")
        self.blameView = root.findChild(QObject, "blameView")
        self.commitListView = root.findChild(QObject, "commitListView")
        
        self.selectedPath = '.'
        self.selectedCommit = None

        