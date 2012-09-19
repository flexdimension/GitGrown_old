from PySide.QtCore import QAbstractListModel, QModelIndex, Slot, Signal


class DictListModel(QAbstractListModel):

    selectionChanged = Signal(int)
    
    def __init__(self, dictList = None, parent = None):
        QAbstractListModel.__init__(self, parent)
        
        self.items = None        
        self.selectedValue = None
        self.selectedKey = None
        self.selectedIndex = None

        if dictList is None or len(dictList) == 0:
            return

        self.setData(dictList)
        
        
    def setData(self, dictList):
        self.items = dictList
        self.roles = dict()
        cnt = 0
        for k in self.items[0].keys() :
            self.roles[cnt] = k
            cnt += 1
            
        self.setRoleNames(self.roles)

    def rowCount(self, parent=QModelIndex()):
        if self.items is None :
            return 0
        return len(self.items)

    def data(self, index, role=0):
        if self.items is None :
            return None
        if role < len(self.roles):
            key = self.roles[role]
            return self.items[index.row()][key]
        return None
    
    def findIndex(self, key, value, exactMatch = True):
        cnt = 0
        for i in self.items :
            print i
            if i[key] == value : #exact match
                return  cnt
            elif exactMatch is False and value in i[key]:
                return cnt
            else :
                cnt += 1
        return -1
    
    def find(self, key, value, exactMatch = True):
        idx = self.findIndex(key, value, exactMatch)
        return self.items[idx]
        
    
    @Slot(str, str)
    def onSelected(self, key, value):
        self.selectedKey = key
        if self.selectedValue == value :
            return

        self.selectedValue = value
        
        print key + " " + value + " selected"
        
        idx = self.findIndex(key, value)
        if idx == -1 :
            return
 
        self.selectedIndex = idx
        print "selected index = " + str(idx)
        self.selectionChanged.emit(idx)

            
    