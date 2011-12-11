from PySide.QtCore import QAbstractListModel, QModelIndex, Signal, Slot


class PyListModel(QAbstractListModel):
    selectionChanged = Signal(int)
    
    def __init__(self, items = None, roles = None, parent = None):
        QAbstractListModel.__init__(self, parent)
        if items is None or roles is None :
            return
        
        self.setData(items, roles)
        self.selectedValue = None
        self.selectedKey = None
        
    def setData(self, items, roles):
        self.items = items
        cnt = 0
        self.roleDict = dict()
        for r in roles :
            self.roleDict[cnt] = r
            cnt += 1
            
        self.setRoleNames(self.roleDict)

    def rowCount(self, parent=QModelIndex()):
        if self.items is None :
            return 0
        return len(self.items)

    def data(self, index, role=0):
        #print "data is called"
        #print len(self.items)
        #print index.row()
        #print role
        if self.items is None or self.roleDict is None :
            return None
        if len(self.roleDict) == 1 :
            return self.items[index.row()]
        if role < len(self.roleDict):
            return self.items[index.row()][role]
        return None
    
    def roleToNum(self, key):
        for r in self.roleDict.items() :
            print r
            if r[1] == key :
                return r[0]
        
        return -1

    @Slot(str, str)
    def onSelected(self, key, value):
        self.selectedKey = key
        if self.selectedValue == value :
            return

        self.selectedValue = value
        roleNum = self.roleToNum(key)
        
        print key + " " + value + " selected"
            
        cnt = 0
        for i in self.items :
            print i
            if i[roleNum] == self.selectedValue :
                self.selectedIndex = cnt
                
                print "selected index = " + str(cnt)
                self.selectionChanged.emit(cnt)

                return  cnt
            else :
                cnt += 1