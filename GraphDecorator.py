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
    COMMIT = '*'

    def __init__(self):
        '''
        Constructor
        '''
        self.decor = []
        
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
    
    def getMaxBranchOffset(self):
        for i in range(len(self.decor)-1, -1, -1):
            d = self.decor[i]
            if  d != GraphDecorator.MERGE and d != GraphDecorator.BLANK:
                return i
        return -1
    
    def getMaxMergeOffset(self):
        for i in range(len(self.decor)-1, -1, -1):
            d = self.decor[i]
            if  d != GraphDecorator.BRANCH and d != GraphDecorator.BLANK:
                return i
        return -1
        
    
    def assignMergeAt(self, offset):
        #handling overflow - extend the memory
        rest = len(self.decor) - offset
        if rest <= 0:
            self.decor.extend([GraphDecorator.BLANK] * (1 - rest))
        if self.decor[offset] == GraphDecorator.BRANCH:
            self.decor[offset] = GraphDecorator.BRANCH_MERGE
        else:
            self.decor[offset] = GraphDecorator.MERGE

    def assignBranchAt(self, offset):
        #handling overflow - extend the memory
        rest = len(self.decor) - offset
        if rest <= 0:
            self.decor.extend([GraphDecorator.BLANK] * (1 - rest))
        if self.decor[offset] == GraphDecorator.MERGE:
            self.decor[offset] = GraphDecorator.BRANCH_MERGE
        else:
            self.decor[offset] = GraphDecorator.BRANCH
        
    def __str__(self):
        return self.decor.__repr__()
        
if __name__ == '__main__':
    gd = GraphDecorator()
    print gd
    gd.addBranch()
    print gd
    gd.addMerge()
    print gd
    gd.assignMergeAt(5)
    print gd
    print gd.getMaxMergeOffset()
    print gd.getMaxBranchOffset()
    gd.assignBranchAt(5)
    print gd