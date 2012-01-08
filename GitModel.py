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
        
            
if __name__ == '__main__' :
    gm = GitModel()
    gm.connect("/Users/unseon_pro/myworks/gitx")
    bg = gm.getBranchGraphs()