import logging

class WList(object):
    
    def __init__(self):
        super()
        self._contents = {}
        
    def deleteItem(self,name):
        if (self.exists(name)):
            del self._contents[name]
            return True
        return False
            
    def updateItem(self,name,value):
        if (self.exists(name) is False):
            return False
        self._contents[name] = value
            
    def addItem(self,name,value):
        if (self.exists(name) is False):
            self._contents[name] = value
            logging.debug("Item: {} values: {}".format(name,self._contents[name]))
            return True
        return False
    
    def getItem(self,name):
        if (self.exists(name) is False):
            return False
        return self._getValue(name)
    
    def exists(self,name):
        if (self._getValue(name) is None):
            return False
        return True
            
    def _getValue(self,name):
        try:
            if (self._contents[name]):
                return self._contents[name]
        except KeyError:
            return None
        except Exception as e:
            logging.debug(e.errno)
            raise Exception("Error al recuperar objeto de memoria") 