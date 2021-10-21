from abc import abstractmethod
from abc import ABC
import logging

 
class DeviceNetwork(ABC):
 
    @abstractmethod
    def transform(self,stdout,module,item):
        pass
    @abstractmethod
    def transform_label(self,item,oid):
        pass
    
    
class Mib(ABC):

    @abstractmethod
    def execute(self):
        pass

class Natmib(Mib):

    def __init__(self):
        self.name="NAT_MIB"
        self.stdin = None
        self.ip = None

    def setData(self,p,ip):
        self.stdin = p
        self.ip = ip
    

    def execute(self):
        try:        
            metric_value = False        
            lines = str(self.stdin).split("\\n")
            for line in lines:
                #logging.debug("linea: {}".format(line))
                tmp_str = str(line).replace("\"","")
                if self.ip in tmp_str:
                    separate_value=tmp_str.split(":")
                    if (len(separate_value)>=3):
                        metric_value = separate_value[3].replace(" ","")
                        #logging.debug(metric_value)
                        
                    break
            
            return metric_value
        except Exception as e:
            logging.debug("Execption {}".format(e))
            return False

class FMib(object):

    @staticmethod
    def getInstance(module):
        targetclass = module.capitalize()
        return globals()[targetclass]()

class Cisr(DeviceNetwork):

    def __init__(self):
        self.enable = False
        self.strategy = None
        
    def normalize_str(self,name):
        tmp_str = str(name).lower().replace(".","_").replace("-", "_")
        return tmp_str

    def transform(self,stdout,module,item):
        self.strategy = FMib.getInstance(module)
        self.strategy.setData(stdout,item)
        return self.strategy.execute()
    
    def transform_label(self,item,oid):
        valuekey = ""
        if ("::" in oid):
            valuekey = oid.split("::")[1] + "_" + item
        else:
            valuekey = self.oid + "_" + item
        
        logging.debug("Normalize: {}".format(self.normalize_str(valuekey)))
        return self.normalize_str(valuekey)