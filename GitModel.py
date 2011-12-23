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
        
        for obj in tree.traverse() :
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
    
    def getBranchGraphs(self):
        
        branchDict = dict()
        
        cnt = 0
        for b in self.repo.heads :
            branchDict[b.name] = cnt
            cnt += 1
        
            
        #mergeMap
        # [main branch name, [list of child branches (name, commit)]]    
        mergeMap = dict()            
        commits = dict()
        for c in self.repo.iter_commits() :
            name_rev = c.name_rev.split(' ')[1].split('/')[-1]
            print 'name_rev ' + c.name_rev
            branchName = name_rev.split('~')[0]
            offset = branchDict[branchName]
            #offset = 0
            
            #parents to string list
            l = lambda x, y : x + [y.hexsha]
            parents = reduce(l, c.parents, [])
        
            merge = None
            if len(parents) >= 1 and 'Merge branch' in c.summary:
                merge = str(c.summary).split("'")[1]
                if branchName in mergeMap.keys() :
                    mergeMap[branchName].append(merge)
                else :
                    mergeMap[branchName] = [merge]
                
                
            commits[c.hexsha] = [c.authored_date, parents, [], offset, name_rev, [], merge]
        
        for i in mergeMap.items() : print i
        
        #branch info
        for b in self.repo.heads :
            name = b.name
            commits[b.commit.hexsha][5].append(name)
            
            for c in self.repo.iter_commits(name) :
                commits[c.hexsha][2].append(name)

        #recalc offset : very very heavy
        for main in mergeMap.keys() :
            main_commit = self.repo.commit(main)
            for branch in mergeMap[main] :
                branch_commit = self.repo.commit(branch)
                for ic in branch_commit.iter_parents() :
                    if ic in main_commit.iter_parents() :
                        print ic.hexsha, commits[ic.hexsha][3], branchDict[main]
                        commits[ic.hexsha][3] = branchDict[main]
                        

                
        rslt = []
        
        for c in commits.keys() :
            d = dict()
            d['hexsha'] = c
            d['authored_date'] = commits[c][0]
            l = lambda x, y : x + ' ' + y
            d['parents'] = reduce(l, commits[c][1], '')[1:]
            d['branches'] = reduce(l, commits[c][2], '')[1:]
            d['offset'] = str(commits[c][3])
            d['name_rev'] = commits[c][4]
            d['heads'] = reduce(l, commits[c][5], '')[1:]
            merge = commits[c][6]
            d['merge'] = merge
            rslt.append(d)
            
        
        rslt = sorted(rslt, key = lambda x : x['authored_date'])

        #for r in rslt : print r
                        
        return DictListModel(rslt)
        
        
            
if __name__ == '__main__' :
    gm = GitModel()
    gm.connect("/Users/unseon_pro/myworks/RoughSketchpad")
    configs = gm.getConfigs()
    print configs.items()
    #for item in sorted(configs) :
    #    print item + "=" + configs[item]