from PySide.QtCore import QAbstractListModel, QModelIndex


class DictListModel(QAbstractListModel):
    def __init__(self, dictList = None, parent = None):
        QAbstractListModel.__init__(self, parent)
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