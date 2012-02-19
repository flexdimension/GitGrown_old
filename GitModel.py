'''
Created on 2011/12/04

@author: unseon_pro
'''

from git import *
from PyListModel import PyListModel
from DictListModel import DictListModel
from GraphDecorator import GraphDecorator

import time

class GitModel() :
    def __init__(self):
        self.configs = dict();
        self.repo = None
        
    def connect(self, path):
        self.repo = Repo(path)
        assert self.repo.bare == False
        
        
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
    
    def getCommitInfo(self, hexsha):
        return None
    
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
    
    def getBranchInfos(self):
        bi = []
        for b in self.repo.heads :
            name = b.name
            for c in self.repo.iter_commits(name) :
                date = c.authored_date
                sha = c.hexsha
                parents = []
                for p in c.parents :
                    parents.append(p.hexsha)
                bi.append([name, date, sha, parents])
                
        return bi
    
    #return DictListModel
    # 
    def getBranchGraphs(self):
        """ return DictListModel of commits for constructing branch graph
        
        keys on a commit dict:
        hexsha
        authored_date 
        /parents
        /branches
        offset
        /name_rev
        /heads
        merge
        """

        self.commitsList = list(self.repo.iter_commits())
        #self.commitsList = sorted(self.commitsList, 
        #                          key = lambda x : x.authored_date,
        #                          reverse = True)
                
        #calculate offset for representing a graph
        self.graphDecorator = self.getGraphDecorator()
        
        rslt = []
        

        
        for ic in self.commitsList:
            item = {'hexsha': ic.hexsha,
                    'authored_date': ic.authored_date,
                    'offset': self.graphDecorator[ic].getCommitOffset(),
                    'maxOffset': self.graphDecorator[ic].getMaxOffset(),
                    'decor': str(self.graphDecorator[ic]),
                    'summary': ic.summary,
                    'idx_parent0': '',
                    'idx_parent1': '',
                    'merge': str(len(ic.parents) == 2)
                    }
            
            cnt = 0
            for p in ic.parents:
                item['idx_parent'+str(cnt)] = self.commitsList.index(p)
                cnt += 1
            
            print ic.hexsha, self.graphDecorator[ic]
                
            rslt.append(item)
        
        #rslt = sorted(rslt, key = lambda x : x['authored_date'])
        
        
        #for i in rslt : print i
        
        return DictListModel(rslt)
            
    def getGraphDecorator(self):
        '''
        return dict of decorator for presenting commits
        '''
        self.graphDecorator = dict()
        #tuple of merge list is composed from commit and its child
        mergeList = [(self.repo.commit(), None)]        
        #create merged commit head list
        while len(mergeList) > 0:
            subFirstCommit, mergeCommit = mergeList.pop(0)
            ic = subFirstCommit
            while True:
                #finish when end of commit
                if len(ic.parents) == 0:
                    subLastCommit = ic
                    branchCommit = None
                    break
                #finish when accessing a commit which have been already met
                if ic.parents[0] in self.graphDecorator.keys() and \
                   self.graphDecorator[ic.parents[0]].getCommitOffset() > -1:
                    subLastCommit = ic
                    branchCommit = ic.parents[0]
                    print 'subLastCommit=', ic.hexsha
                    print 'branchCommit=', branchCommit.hexsha
                    break
                
                #push merged commit when parents are two
                if len(ic.parents) == 2 :
                    #print 'push : ', ic.parents[1].hexsha, self.commitsList.index(ic.parents[1])
                    mergeList.append((ic.parents[1], ic))
                ic = ic.parents[0]
                

            if subFirstCommit in self.graphDecorator.keys() and \
               self.graphDecorator[subFirstCommit].getCommitOffset() >= 0:
                offsetSFC = self.graphDecorator[subFirstCommit].getCommitOffset()
                self.graphDecorator[mergeCommit].assignForwardMergeAt(offsetSFC)
                continue
                
            maxOffset = self.getMaxOffset(mergeCommit, branchCommit, self.graphDecorator)
            #print 'maxOffset = ', maxOffset
            maxOffset += 1
            #update all iter_commit as maxOffset
            if mergeCommit is not None:
                if mergeCommit not in self.graphDecorator.keys():
                    self.graphDecorator[mergeCommit] = GraphDecorator()
                if self.graphDecorator[mergeCommit].lastDecor() == GraphDecorator.BRANCH:
                    maxOffset -= 1
                    self.graphDecorator[mergeCommit].assignMergeBranchAt(maxOffset)
                else:
                    self.graphDecorator[mergeCommit].assignMergeAt(maxOffset)
                idxMergeCommit = self.commitsList.index(mergeCommit)
            else:
                idxMergeCommit = -1
            
            
            if branchCommit is not None:
                if branchCommit not in self.graphDecorator.keys():
                    self.graphDecorator[branchCommit] = GraphDecorator()
                self.graphDecorator[branchCommit].assignBranchAt(maxOffset)
                idxBranchCommit = self.commitsList.index(branchCommit)
            else:
                idxBranchCommit = None

                
            for icc in self.commitsList[idxMergeCommit + 1:idxBranchCommit]:
                if icc not in self.graphDecorator.keys():
                    self.graphDecorator[icc] = GraphDecorator()
                self.graphDecorator[icc].assignForwardAt(maxOffset)
                #print 'f', self.graphDecorator[icc]
                
            
                
            #update all iter_parent as offset
            ic = subFirstCommit
            while True:
                self.graphDecorator[ic].assignCommitAt(maxOffset)
                if ic == subLastCommit:
                    break;
                ic = ic.parents[0]
                
                
                
        for i in self.commitsList: print i.hexsha, self.graphDecorator[i]
        
        
        
        return self.graphDecorator
                

    def getMaxOffset(self, begin, end, graphDecorator):
        #if maxOffsetDict is not initialized, return offset 0
        maxOffset = -1
        if begin is None:
            beginIndex = 0
        else :
            beginIndex = self.commitsList.index(begin)
            
        if end is None:
            endIndex = None
        else :
            endIndex = self.commitsList.index(end) + 1
            
        for ic in self.commitsList[beginIndex:endIndex]:
            if ic in graphDecorator.keys():
                maxOffset = max(graphDecorator[ic].getMaxOffset(), maxOffset)
            
        return maxOffset
    
    def traverse(self):
        rslt = []
        
        
        
        
        return rslt 
    
    def traverseBranch(self, commit, level, parentCommit):
        assert(commit is not None)
        
        cm = commit
        
        branches = []
        branchCommits = []

        while True:
            branchCommits.append(cm)
            #self.decoList[cm] = GraphDecorator()
            
            
            if len(cm.parents) == 0 or cm.parents[0] in self.traversedList:
                break;
            if len(cm.parents) == 2:
                branches.append(cm)
            cm = cm.parents[0]
        
        if parentCommit is None:
            idx = 0
        else:                
            idx = self.traversedList.index(parentCommit) + 1
            if len(parentCommit.parents) is None:
                pass
            elif parentCommit.parents[0] != cm.parents[0]:
                #firstBranchedCommit = self.traversedList.index(branchCommits[-1])
                #pFirstBranchedCommit = self.traversedList.index(branchCommits[-1].parents[0])                
                level = level + 1
        
        #merge    
        self.traversedList = self.traversedList[:idx] + \
                        branchCommits + \
                        self.traversedList[idx:]



        
        for cm in branchCommits:
            self.levelList[cm] = level

        for c in branches:
            self.traverseBranch(c.parents[1], level+1, c)

                
    def printTraverse(self):
        self.traversedList = []
        self.levelList = dict()
        self.decoList = dict()
        
        self.traverseBranch(self.repo.commit('master'), 0, None)
        
        for i in self.traversedList:
            print ' ' * self.levelList[i] + 'O' + '\t' + i.hexsha + ' ' + i.summary[:20]
                
        
    
    def getBranchGraphs2(self):
        
        heads = self.repo.heads
        
        #headCommitList a list of a tuble (head commit and its child)
        #headCommitList = map(lambda x:(self.repo.commit(x), None), heads)
        headCommitList = [(heads.master.commit, None)]
        
        rslt = []
        
        while len(headCommitList) > 0:
            stream = []
            commit, childCommit = headCommitList.pop()
            print commit, "is poped : ", len(headCommitList) 
            
            ic = commit
            #if ic is already exist insert list and quit
            while True:
                if ic in rslt:
                    if childCommit is not None:
                        idxInsert = rslt.index(childCommit) + 1
                    else:
                        idxInsert = 0
                    rslt = rslt[0:idxInsert] + stream + rslt[idxInsert:]
                    break
                else:
                    stream.append(ic)
                    
                    parents = ic.parents
                    if len(parents) == 0:
                        break
                    else:
                        if len(parents) > 1:
                            headCommitList.append((parents[1], ic))
                            print parents[1], "is appended", len(headCommitList) 
                        ic = ic.parents[0]
        return rslt

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
        
                        
    def getCommitListModelFromBranch(self, branchName):
        '''
        get list of commits come from branchName
        
        Params
        branchName : str
        
        Return
        DictListModel (list of dict)
            keys:
                hexsha
                authored_date
                summary
        '''
        commitList = []
        headCommit = self.repo.commit(branchName)
        commitList.append(self.convertToDict(headCommit))

        ic = headCommit
        while True:
            if len(ic.parents) is 0:
                break
            ic = ic.parents[0]
            commitList.append(self.convertToDict(ic))
        
        return DictListModel(commitList)
    
    def getFlowModel(self):
        flowList = self.getBranchGraphs3()
        commitInfos = map(lambda x:self.convertToDict(x), flowList)
        return DictListModel(commitInfos)
    
    def getFlowModelWithBranches(self, branches):
        
        headCommits = map(lambda x: self.repo.commit(x), branches)

        traversedList = self.getBranchGraphs3()
        commitInfos = map(lambda x:self.convertToDict(x), traversedList)


        self.traversedList = []
        
        for i in range(len(headCommits)):
            print "flow:", branches[i]
            cf = self.getCommitFlow(headCommits[i])
                 
            for ic in cf:
                idx = traversedList.index(ic)
                if commitInfos[idx]['offset'] == 0:
                    commitInfos[idx]['offset'] = i + 1
        
        return DictListModel(commitInfos)

    def getCommitFlow(self, commit):
        currentFlow = []

        while True :
            currentFlow.append(commit)
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
                
        for i in currentFlow:
            print "getCommitFlow", i.hexsha
                
        return currentFlow                


    
    def getBranchGraphs3(self):
        heads = self.repo.heads
        masterCommit = heads.master.commit
        
        self.traversedList = []
        
        self.traverseCommit(masterCommit)

        self.traversedList.reverse()
                
        return self.traversedList
       
    def traverseCommit(self, commit):
        
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
    gm.connect("/Users/unseon_pro/myworks/FlowsSample")
    bg = gm.getBranchGraphs3()
    for i in bg :
        print "traversed", i.hexsha