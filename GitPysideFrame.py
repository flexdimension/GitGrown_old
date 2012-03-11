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
            
    @Slot()
    def refreshStatus(self):
        print 'refreshed!!'
        self.gm.refreshStatus()
        rootContext = self.view.rootContext()
        rootContext.setContextProperty('gitStatus', self.gm.status)
        rootContext.setContextProperty('indexModel', self.gm.indexModel)
        
    @Slot()
    def commit(self, msg):
        assert msg is not None and msg != ''
        
        print msg
        self.gm.executeCommit(msg)
        self.refreshStatus()
        
    @Slot()
    def stageFile(self, path):
        print 'GitPysideFrame: slot stage called: ' + path
        self.gm.stageFile(path)
        self.refreshStatus()
        
    @Slot()
    def unstageFile(self, path):
        print 'GitPysideFrame: slot unstage called'
        self.gm.unstageFile(path)
        self.refreshStatus()
        
    @Slot()
    def discard(self, path):
        print 'GitPysideFrame: slot discard called'
        self.refreshStatus()
    
        
        
        

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
        #self.gm.connect('/Users/unseon_pro/myworks/gitx')
        #self.gm.connect('/Users/unseon_pro/myworks/FlowsSample')
        
        self.configModel = self.gm.getConfigModel()
        
        self.fileListModel = self.gm.getFileListModel()
        self.fileListModel.selectionChanged.connect(self.onSelectedPathChanged)
        
        self.fileViewModel = None
        self.commitListModel = self.gm.getCommitListModel('', 'tree')
        
        #self.branchGraphModel = self.gm.getBranchGraphs()
        #self.commitListModel2 = self.gm.getCommitListModelFromBranch('master')
        
        
        self.flowModel = self.gm.getFlowModelWithBranches(
                                      ['master', 'development', 'feature_command'])
        
        # Create an URL to the QML file
        #url = QUrl('view.qml')
        #url = QUrl('BranchFlowView.qml')
        url = QUrl('MainView.qml')

        # Set the QML file and show
        
        rootContext = self.view.rootContext()
        
        #removed because of halt
        #rootContext.setContextProperty('rootFrame', self)
        rootContext.setContextProperty('config', self.configModel)
        rootContext.setContextProperty('fileListModel', self.fileListModel)
        rootContext.setContextProperty('fileViewModel', self.fileViewModel)
        rootContext.setContextProperty('commitListModel', self.commitListModel)
        rootContext.setContextProperty('flowModel', self.flowModel)
        rootContext.setContextProperty('gitModel', self.gm)
        
        self.refreshStatus()
        
        self.view.setSource(url)
        
        root = self.view.rootObject()
        
        self.refreshButton = root.findChild(QObject, "refreshButton")
        self.refreshButton.clicked.connect(self.refreshStatus)

        self.commitButton = root.findChild(QObject, "commitButton")
        self.commitButton.commitWithMessage.connect(self.commit)
        
        self.indexStatus = root.findChild(QObject, "indexStatus")
        self.indexStatus.stageFile.connect(self.stageFile)
        self.indexStatus.unstageFile.connect(self.unstageFile)

        #self.fileBrowser = root.findChild(QObject, "fileBrowser")
        #self.blameView = root.findChild(QObject, "blameView")
        #self.commitListView = root.findChild(QObject, "commitListView")
        
        self.selectedPath = '.'
        self.selectedCommit = None

        