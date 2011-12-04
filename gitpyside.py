'''
Created on 2011/12/04

@author: unseon_pro
'''

from git import *

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
            
if __name__ == '__main__' :
    gm = GitModel()
    gm.connect("/Users/unseon_pro/myworks/RoughSketchpad")
    configs = gm.getConfigs()
    print configs.items()
    #for item in sorted(configs) :
    #    print item + "=" + configs[item]