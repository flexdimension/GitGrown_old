'''
Created on 2011/12/04

@author: unseon_pro
'''

from git import Git, Repo
from PyListModel import PyListModel
from DictListModel import DictListModel
from GraphDecorator import GraphDecorator
from PySide.QtCore import QObject, Slot, Signal

from subprocess import Popen

import time

class GitModel(QObject) :

    statusRefreshed = Signal(str)

    def __init__(self):
        super(GitModel, self).__init__(None)
        self.configs = dict();
        self.repo = None
        
    def connect(self, path):
        self.repo = Repo(path)
        assert self.repo.bare == False
        
        self.git = Git(path)
        self.git.init()
        
    def run(self, cmd):
        print "run " + str(cmd)
        process = Popen(cmd)
        process.wait()
        print "returncode is " + str(process.returncode)
        return process.returncode
       
    def refreshStatus(self):
        self.status = self.git.status()    
        self.indexModel = self.getIndexModel()
        
        self.statusRefreshed.emit(self.status)
        
    def stageFile(self, path):
        return self.run(['git', 'add', path])
        
    def unstageFile(self, path):
        return self.run(['git', 'reset', 'HEAD', path])

    def executeCommit(self, msg):
        if msg is None or len(msg) == 0:
            print 'Message is empty'
            return -1

        rslt = self.run(['git', 'commit', '-m', msg])

        return rslt
    
    def undoRecentCommit(self):
        rslt = self.run(['git', 'reset', '--soft', 'HEAD^'])        
        return rslt

    def getIndexStatus(self):
        fileIndex = dict()
        
        MODIFIED = '#\tmodified:   '
        RENAMED = '#\trenamed:    '
        NEW_FILE = '#\tnew file:   '
        COMMITTED = '# Changes to be committed:'
        CHANGED = '# Changed but not updated:'
        UNTRACKED = '# Untracked files:'
        UNTRACKED_INTENT = '#    '
        

        self.isIdxClear = True
        lines = self.status.splitlines()
        type = ''
        for l in lines:
            print l
            
            #index
            if l == COMMITTED :
                type = 'I'
                self.isIdxClear = False
                
            #working directory
            elif l == CHANGED :
                type = 'W'

            if l.startswith(MODIFIED) :
                path = l[len(MODIFIED):]
                
                if type == 'I':
                    fileIndex[path] = 'M'
                elif type == 'W':
                    if path in fileIndex.keys():
                        fileIndex[path] += 'C'
                    else:
                        fileIndex[path] = 'C'
                continue
            
            if l.startswith(RENAMED) :
                path = l[len(RENAMED):].split(' ')[2]               
                fileIndex[path] = 'R'
            
            if l.startswith(NEW_FILE) :
                path = l[len(NEW_FILE):]                
                fileIndex[path] = 'N'                
                
            if l == UNTRACKED :
                type = 'U'
            
                idx = lines.index(l) + 3
                
                for ul in lines[idx:] :
                    if ul.startswith('#'):
                        path = ul.split('\t')[1]
                        #fileList.append({'type': type, 'path': path})
                        fileIndex[path] = 'U'
                break

        fileList = [] 
        
        #untracked or new files are appended later
        for path in fileIndex.keys() :
            if fileIndex[path] != 'U' and fileIndex[path] != 'N':
                fileList.append({'type': fileIndex[path], 'path': path})
        for path in fileIndex.keys() :
            if fileIndex[path] == 'U' or fileIndex[path] == 'N':
                fileList.append({'type': fileIndex[path], 'path': path})
               
        for i in fileList: print i
            
        return fileList
    
    def isIndexClear(self):
        return self.isIdxClear        
    
    def getIndexModel(self):
        return DictListModel(self.getIndexStatus())
        
    def getConfigs(self):
        rslt = dict()
        
        configs = self.repo.config_reader()
        
        for section in configs.sections():
            for option in configs.options(section):
                val = configs.get(section, option)
                val_typed = configs.get_value(section, option)
                rslt[section+"."+option] = val
        
        return rslt
    
    def getConfigItems(self):
        return sorted(self.getConfigs().items())
    
    def getConfigRoles(self):
        return ['section', 'value']
    
    def getConfigModel(self):
        return PyListModel(self.getConfigItems(), self.getConfigRoles())
    
    def getFileList(self):
        tree = self.repo.head.commit.tree
        rslt = []
        
        info = dict()
        info['name'] = "<" + tree.abspath.split('/')[-1] + ">"
        info['path'] = tree.path
        info['type'] = tree.type
        rslt.append(info)
        
        print "tree traverse"
        for obj in tree.traverse() :
            #not yet submodule is not carried
            if obj.type == 'submodule' :
                continue
            info = dict()
            info['name'] = obj.name
            info['path'] = obj.path
            #if isinstance(obj, Tree) :
            #    info['type'] = "dir"
            #else :
            #    info['type'] = "file"
                
            info['type'] = obj.type
            rslt.append(info)
        rslt = sorted(rslt, key = lambda t:t['path'])
        
        return rslt
    
    def getCommitInfo(self, hexsha = ''):
        return self.convertToDict(self.repo.commit())
    
    def getFileListModel(self):
        return DictListModel(self.getFileList())
    
    def getBlamed(self, path, commit):
        data = self.repo.git.blame(commit, path)
        
        rslt = []
        
        for line in data.splitlines() :
            print 'line = ', line
            commit, rest = line.split(' (', 1)
            info = rest.split(') ', 1)
            infos = info[0].split(' ', 4)
            infos[4] = int(infos[4])
            
            code = info[1]
            
            rslt.append([commit] + infos + [code])
        '''
        for i in rslt :
            i[0] = i[0].hexsha
            i[1] = str(i[1][0])
        '''    
        return rslt
        
    def getBlamedRoles(self):
        return ['commit', 'user', 'data', 'time', 'permission', 'num', 'code']

    def getBlamedModel(self, path, commit = 'HEAD'):
        return PyListModel(self.getBlamed(path, commit), self.getBlamedRoles())

    def getCommitList(self, path, type = 'blob'):
        rslt = []
        
        if path == '' : #get all commit list if path is top
            for c in self.repo.iter_commits('HEAD', max_count = 100) :
                rslt.append([c.hexsha, c.author.name, \
                    time.asctime(time.gmtime(c.authored_date))])
            return rslt
        
        for c in self.repo.iter_commits('HEAD', max_count = 100) :
            for k in c.stats.files.keys() :
                #print "path:" + b.path
                if k == path or (type == 'tree' and path in k) :
                    rslt.append([c.hexsha, c.author.name, \
                        time.asctime(time.gmtime(c.authored_date))])
                    break
        #print rslt
        return rslt
    
    def getCommitRoles(self):
        return ['hexsha', 'author_name', 'authored_date']
    
    def getCommitListModel(self, path, type = 'blob'):
        return PyListModel(self.getCommitList(path, type), self.getCommitRoles())

    def convertToDict(self, commit):
        '''
        convert a commit to a dict item with keys
        
        Params:
            commit
            
        Return:
            a dict with keys
                hexsha
                authored_date
                summary
        '''
        item = {'hexsha': commit.hexsha,
                'authored_date': commit.authored_date,
                'summary': commit.summary,
                'isMerged': False,
                'mergeInto': None,
                'mergeFrom': None,
                'offset': 0,
                }
        
        isMerged = commit.summary[:5] == 'Merge'
        if isMerged :
            '''
            parse summary to get mergeFrom and mergeInto
            '''
            parts = commit.summary.split('\'')
            item['mergeFrom'] = parts[1]
            
            if len(parts) == 2 :
                item['mergeInto'] = 'master'
            else:
                item['mergeInto'] = parts[2][6:]
        
        return item
        
    def getFlowModelWithBranches(self, branches):
        
        headCommits = map(lambda x: self.repo.commit(x), branches)

        #Get traversedList and convert it to commitInfos
        traversedList = self.getBranchGraphs3(branches)
        commitInfos = map(lambda x:self.convertToDict(x), traversedList)

        self.traversedList = []
        
        for i in range(len(headCommits)):
            print "flow:", branches[i]
            cf = self.getCommitFlow(headCommits[i])
                 
            for ic in cf:
                idx = traversedList.index(ic)
                commitInfos[idx]['offset'] = i + 1
                
        commitInfos.reverse()
        
        return DictListModel(commitInfos)

    def getCommitFlow(self, commit):
        currentFlow = []

        while True :
            currentFlow.append(commit)
            self.traversedList.append(commit)
            parents = commit.parents
            
            if len(parents) == 0:
                #print "branch3:", commit, "- commit terminated"
                break
            elif len(parents) == 1:
                p0 = parents[0]
                if p0 in self.traversedList:
                    #print "branch3:", commit, "- return to branch"
                    break
                else:
                    #print "branch3:", commit, "- forward to parents"
                    commit = p0
                    continue
            else: #len(parents) == 2
                p0 = parents[0]
                p1 = parents[1]
                if p0 in self.traversedList:
                    commit = p1
                    continue
                else:
                    commit = p0
                    continue
                
        #for i in currentFlow:
            #print "getCommitFlow", i.hexsha
                
        return currentFlow                


    
    def getBranchGraphs3(self, branches):
        #heads = self.repo.heads
        #masterCommit = heads.master.commit
        
        self.traversedList = []
        
        for b in branches:
            headCommit = self.repo.commit(b)
            self.traverseCommit(headCommit)

        #self.traversedList.reverse()
                
        return self.traversedList
       
    def traverseCommit(self, commit):
        if commit in self.traversedList:
            return
        
        currentFlow = []

        while True :
            currentFlow.append(commit)
            parents = commit.parents
            
            if len(parents) == 0:
                #print "branch3:", commit, "- commit terminated"
                break
            else:
                p0 = parents[0]
                if p0 in self.traversedList:
                    #print "branch3:", commit, "- return to branch"
                    break
                else:
                    #print "branch3:", commit, "- forward to parents"
                    commit = p0
                    continue
                
        currentFlow.reverse()                
        for commit in currentFlow:
            if len(commit.parents) == 2:
                self.traverseCommit(commit.parents[1])            
            self.traversedList.append(commit)
            
            
if __name__ == '__main__' :
    gm = GitModel()
    #gm.connect("/Users/unseon_pro/myworks/FlowsSample")
    #bg = gm.getBranchGraphs3()
    #for i in bg :
    #    print "traversed", i.hexsha
    
    #gm.connect('.')
    #rslt = gm.getIndexStatus()
    #for i in rslt: print i