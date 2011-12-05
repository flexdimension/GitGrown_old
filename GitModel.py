'''
Created on 2011/12/04

@author: unseon_pro
'''

from git import *
from PythonModel import PythonModel

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
    
    def getFileList(self):
        tree = self.repo.head.commit.tree
        rslt = []
        for obj in tree.traverse() :
            info = dict()
            info['name'] = obj.name
            info['path'] = obj.path
            if isinstance(obj, Tree) :
                info['type'] = "dir"
            else :
                info['type'] = "file"
            rslt.append(info)
        rslt = sorted(rslt, key = lambda t:t['path'])
        
        return rslt
    
    def getBlamedModel(self, path):
        data = self.repo.git.blame("HEAD", path)
        
        rslt = []
        
        for line in data.splitlines() :
            commit, rest = line.split(' (')
            print rest
            info = rest.split(') ')
            print info
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
        
            
if __name__ == '__main__' :
    gm = GitModel()
    gm.connect("/Users/unseon_pro/myworks/RoughSketchpad")
    configs = gm.getConfigs()
    print configs.items()
    #for item in sorted(configs) :
    #    print item + "=" + configs[item]