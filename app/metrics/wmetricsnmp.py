from prometheus_client import Gauge
from prometheus_client import CollectorRegistry

import logging

class WMetricSNMP(object):
    
    def __init__(self,oid):
        super()
        self.name=oid
        self.contents={}
        self.registry = CollectorRegistry()
    
    def getName(self):
        return self.name
    
    def getRegistry(self):
        return self.registry
    
    def addMetric(self,name):
        try:
            logging.debug("Desde addmetric")
            self.contents[name]=Gauge(name, 'values',registry=self.registry)
        except Exception as e:
            logging.debug("Parametro de key incorrecto {}".format(e))
            raise Exception("Error al insertar una key invalida.")
        
    def updateValue(self,name,value):
        logging.debug("Desde updatevalue")
        if (self.getValue(name) is None):
            return False
        
        metric = self.getValue(name)
        logging.debug(value)
        metric.set(value)
        #metric.labels(snmp='oid').set(value)
       
        return True
    
    def getValue(self,name):
        try:
            logging.debug("Desde getvalue")
            if (self.contents[name]):
                return self.contents[name]
        except KeyError:
            return None
        except Exception as e:
            logging.debug(e.errno)
            raise Exception("Error al recuperar objeto de memoria") 
        
