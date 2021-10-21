from app import app
from prometheus_client import generate_latest
from .service.wsnmp import WSNMP

from flask import request
import json
import logging
from .metrics.wmetricsnmp import WMetricSNMP
from .util.wlist import WList

control_metric = WList()

def processMetrics(metric_snmp,values):
    #logging.debug(values)
    for key in values.keys():
        logging.debug("Key: "+key)
        if (metric_snmp.getValue(key) is None):
            metric_snmp.addMetric(key)
            metric_snmp.updateValue(key,values[key])
        else:
            metric_snmp.updateValue(key,values[key])

def check_parameter(oid,oidmethod):
    if oid is None:
        return False
    if oidmethod is None:
        return False
        
    return True

@app.route('/api/v1/json',methods=['GET'])
@app.route('/json',methods=['GET'])
def getsession():
    app.logger.debug('accesso generate json')
    oid = request.args.get('oid')
    oidmethod = request.args.get('oidmethod')
    if (check_parameter(oid,oidmethod)):
        logging.debug("metrics getting")
        query = WSNMP()
        values = query.check(oid,oidmethod)
        logging.debug(values)
        return json.dumps(values), 200
    
    return json.dumps({"status":"Requiere ingresar un OID Method + OID"}), 404

@app.route('/api/v1/metrics',methods=['GET'])
@app.route('/metrics',methods=['GET'])
def metricssession():
    app.logger.debug('accesso metrics')
    oid = request.args.get('oid')
    oidmethod = request.args.get('oidmethod')
    if (check_parameter(oid,oidmethod)):
        logging.debug("metrics prometheus getting")
        query = WSNMP()
        metric = None
        values = query.check(oid,oidmethod)
        if (control_metric.exists(oid)):
            metric = control_metric.getItem(oid)
            processMetrics(metric, values)
            control_metric.updateItem(metric.getName(),metric)
        else:
            metric = WMetricSNMP(oid)
            processMetrics(metric, values)
            control_metric.addItem(metric.getName(),metric)
        
        
        return generate_latest(metric.getRegistry())
    
    return json.dumps({"status":"Requiere ingresar un OID Method + OID"}), 404