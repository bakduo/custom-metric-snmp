import subprocess

from ..config.config import CONFIG_APP

#Neccesary for import dinaymc instance
from .device.ciscoisr import Cisr

import logging

class FDevice(object):

    def __init__(self):
        self.name="factory"

    @staticmethod
    def getInstance(name):
        targetclass = name.capitalize()
        return globals()[targetclass]()


class WSNMP(object):
    def __init__(self):
        self.community = CONFIG_APP["app"]["community"]
        self.device = CONFIG_APP["app"]["device"]
        self.mips = CONFIG_APP["app"]["mips"]
        self.port = CONFIG_APP["app"]["port"]
        self.version = CONFIG_APP["app"]["version"]
        self.oid = ""
        self.hosts = CONFIG_APP["app"]["hosts"].split(",")
        self.module = CONFIG_APP["app"]["module"]
        self.oidmethod = ""

    def check(self,oid,oidmethod):
        try:
            self.oid = oid
            self.oidmethod = oidmethod
            cmd = "/usr/bin/snmpwalk -v{} -c{} -m {} {}:{} {}".format(self.version,self.community,self.mips,self.device,self.port,self.oid)
            #Minimal mockup
            #cmd = "cat ./fixit/snmp.txt"
            check = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
            stdout, stderr = check.communicate()
            module = FDevice.getInstance(self.module)
            salida = {}
            for item in self.hosts:
                logging.debug(item)
                label = module.transform_label(item,self.oid)
                value = module.transform(stdout,self.oidmethod,item)
                logging.debug(value)
                if (value):
                    salida[label]=value
                    
                   
            return salida
        except Exception as e:
            raise Exception("Exception al realizar check")


