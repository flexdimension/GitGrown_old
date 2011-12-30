'''
Created on 2011/12/29

@author: unseon_pro
'''

class GraphDecorator():
    '''
    classdocs
    '''


    MERGE = '\\'
    BRANCH = '/'
    FOWARD = '|'
    BRANCH_MERGE = '<'
    BLANK = ' '

    def __init__(self):
        '''
        Constructor
        '''
        self.decor = ''
        
    def lastDecor(self):
        if len(self.decor) == 0:
            return ''
        else :
            return self.decor[-1]
        
    def setLastDecor(self, decor):
        if len(self.decor) == 0:
            self.decor[0] = decor
        else :
            self.decor[-1] = decor
    
    def appendDecor(self, decor):
        self.decor.append(decor)

    def addMerge(self):
        if self.lastDecor() == GraphDecorator.BRANCH:
            self.setLastDecor(GraphDecorator.BRANCH_MERGE)
        else:
            self.appendDecor(GraphDecorator.MERGE)

    def addBranch(self):
        if self.lastDecor() == GraphDecorator.MERGE:
            self.setLastDecor(GraphDecorator.BRANCH_MERGE)
        else:
            self.appendDecor(GraphDecorator.BRANCH)
            
    def addFoward(self):
        self.appendDecor(GraphDecorator.FOWARD)
        
    def getMaxOffset(self):
        return len(self.decor) - 1