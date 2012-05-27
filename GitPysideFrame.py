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
        obj = self.gitModel.getFileList()[index]
        
        if obj['type'] == 'blob' :
            self.fileViewModel = self.gitModel.getBlamedModel('HEAD', filePath)
            self.commitListModel = self.gitModel.getCommitListModel(filePath)
        elif obj['type'] ==  'tree':
            self.fileViewModel = None
            self.commitListModel = self.gitModel.getCommitListModel(filePath, 'dir')
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
        obj = self.gitModel.getFileList()[fileIndex]
        if obj['type'] == 'blob' :
            self.fileViewModel = self.gitModel.getBlamedModel(sha, filePath)
            rootContect = self.view.rootContext()
            rootContect.setContextProperty('fileViewModel', self.fileViewModel)
            self.blameView.setProperty('currentCommit', sha)
            print "blame model is changed"
            
    @Slot()
    def refreshStatus(self):
        print 'refreshed!!'
        self.gitModel.refreshStatus()
        rootContext = self.view.rootContext()
        rootContext.setContextProperty('gitStatus', self.gitModel.status)
        rootContext.setContextProperty('indexModel', self.gitModel.indexModel)
        self.flowModel = self.gitModel.getFlowModelWithBranches(
                                      ['master',
                                       'development',
                                       'feature_command',
                                       'feature_ui'])
        rootContext.setContextProperty('flowModel', self.flowModel)
                
    @Slot()
    def commit(self, msg):
        assert msg is not None and msg != ''
        
        print "GitPysideFrame : " + msg
        self.gitModel.executeCommit(msg)
        self.refreshStatus()
        
    @Slot()
    def stageFile(self, path):
        print 'GitPysideFrame: slot stage called: ' + path
        self.gitModel.stageFile(path)
        self.refreshStatus()
        
    @Slot()
    def unstageFile(self, path):
        print 'GitPysideFrame: slot unstage called'
        self.gitModel.unstageFile(path)
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
        
        self.gitModel = GitModel()
        #self.gitModel.connect('/Users/unseon_pro/myworks/RoughSketchpad')
        self.gitModel.connect('.')
        #self.gitModel.connect('/Users/unseon_pro/myworks/gitx')
        #self.gitModel.connect('/Users/unseon_pro/myworks/FlowsSample')
        
        self.configModel = self.gitModel.getConfigModel()
        
        self.fileListModel = self.gitModel.getFileListModel()
        self.fileListModel.selectionChanged.connect(self.onSelectedPathChanged)
        
        self.fileViewModel = None
        self.commitListModel = self.gitModel.getCommitListModel('', 'tree')
        
        #self.branchGraphModel = self.gitModel.getBranchGraphs()
        #self.commitListModel2 = self.gitModel.getCommitListModelFromBranch('master')
        
        
        self.flowModel = self.gitModel.getFlowModelWithBranches(
                                      ['master',
                                       'development',
                                       'feature_command',
                                       'feature_ui'])
        
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
        rootContext.setContextProperty('gitModel', self.gitModel)
        
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

        