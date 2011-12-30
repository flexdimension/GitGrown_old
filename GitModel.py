'''
Created on 2011/12/04

@author: unseon_pro
'''

from git import *
from PyListModel import PyListModel
from DictListModel import DictListModel

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
        self.offsetDict, self.maxOffsetDict = self.getOffsetDict()
        
        rslt = []
        

        
        for ic in self.commitsList:
            item = {'hexsha': ic.hexsha,
                    'authored_date': ic.authored_date,
                    'offset': self.offsetDict[ic],
                    'maxOffset': self.maxOffsetDict[ic],
                    'summary': ic.summary,
                    'idx_parent0': '',
                    'idx_parent1': '',
                    'merge': str(len(ic.parents) == 2)
                    }
            
            cnt = 0
            for p in ic.parents:
                item['idx_parent'+str(cnt)] = self.commitsList.index(p)
                cnt += 1
                
            rslt.append(item)
        
        #rslt = sorted(rslt, key = lambda x : x['authored_date'])
        
        
        #for i in rslt : print i
        
        return DictListModel(rslt)
        
        
    def getOffsetDict(self):
        offsetDict = dict()
        maxOffsetDict = dict()
        graphDecorator = dict()
        mergeList = [(self.repo.commit(), None)]
        offset = 0
        
        #create merged commit head list
        while len(mergeList) > 0:
            commit, childCommit = mergeList.pop(0)
            ic = commit
            while True:
                if len(ic.parents) == 0:
                    break
                if ic.parents[0] in offsetDict.keys() :
                    break
                if len(ic.parents) == 2 :
                    print 'push : ', ic.parents[1].hexsha, self.commitsList.index(ic.parents[1])
                    mergeList.append((ic.parents[1], ic))
                ic = ic.parents[0]
                
            endCommit = ic
            maxOffset = self.getMaxOffset(childCommit, endCommit, maxOffsetDict)
            #print 'maxOffset = ', maxOffset
            maxOffset += 1
            #update all iter_commit as maxOffset
            if childCommit is None:
                beginIndex = 0
            else :
                beginIndex = self.commitsList.index(childCommit)
                
            endIndex = self.commitsList.index(endCommit)
            for icc in self.commitsList[beginIndex:endIndex+1]:
                maxOffsetDict[icc] = maxOffset
            #update all iter_parent as offset
            ic = commit
            while True:
                offsetDict[ic] = maxOffset
                if ic == endCommit:
                    break;
                ic = ic.parents[0]
                
        #for i in self.commitsList: print i.hexsha, offsetDict[i]
        
        
        
        return offsetDict, maxOffsetDict
                

    def getMaxOffset(self, begin, end, maxOffsetDict):
        #if maxOffsetDict is not initialized, return offset 0
        maxOffset = -1
        if begin is None:
            beginIndex = 0
        else :
            beginIndex = self.commitsList.index(begin)
        for ic in self.commitsList[beginIndex:]:
            if ic in maxOffsetDict.keys():
                maxOffset = max(maxOffsetDict[ic], maxOffset)
            
            if ic == end:
                break
            
        return maxOffset       
        
            
if __name__ == '__main__' :
    gm = GitModel()
    gm.connect("/Users/unseon_pro/myworks/gitx")
    bg = gm.getBranchGraphs()