Export metrics custom by prometheus and python app
===============================

# ROADMAP
- [x] acceso por medio de snmp
- [x] obtener metricas por medio de snmp
- [x] generar metrics prometheus
- [x] generar modulo para dispotivos. Se inicia con separar por ahora solo para cisco
- [x] generar bypass para metricas respecto a los servicios.
- [x] adecuar grafana y/o centreon para esto.
- [x] generar imagen de docker. Así se puede usar como una api de servicio.
- [x] refactor

# Problematica

No siempre telegraf, u otra herramienta de extracción de metricas nos puede funcionar acorde a los resultados esperados por medio de snmp. Cuando falla la devolución en formato **table**. Por lo tanto opte por realizar un servicio para converir la salida en lo que necesito.

# Generar dependencias

```
pipenv lock -r > deploy-requirements.txt

```

# Build

Genera una imagen de docker 
```
make clean && make build

```

se puede pasar la config correspondiente en formato json:
```
docker --rm -v config.json:...app.json -p x:5000 nombre-service:version

```

En caso de pasar a kubernetes o Swarm simplemente agregan los datos correspondientes a secrets de json y demas configuración relacionada al deploy de servicio.

# Ejemplo configuracion:
config.json
```
{
    "app":{
        "device":"servidor",
        "port":puerto,
        "community":"public",
        "mips":"foldermips",
        "hosts":"1.1.1.1,2.2.2.2,4.4.4.4.etc...",
        "version":"version",
        "module":"modulo"
    }
}
```
Que me permite exportar?
```

NAT-MIB::natAddrBindInTranslates.0.ipv4."ip1" = Counter64: n
NAT-MIB::natAddrBindInTranslates.0.ipv4."ip2" = Counter64: n
NAT-MIB::natAddrBindInTranslates.0.ipv4."ip3" = Counter64: n
NAT-MIB::natAddrBindInTranslates.0.ipv4."ip3" = Counter64: n
...

```

Como metodología inicial se podria extender de clase DeviceNetwork y Mib. De forma tal de implementar cualquier device y OID como modulo y expotar las metricas en formato de prometheus.

