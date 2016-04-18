# HApi
HApi, HA Proxy api to manage nodes. HApi is a Restful API that provides haproxy load balancer nodes management. The main goal of HApi is to simply get JSON objects to get stats,node availability info and manage them.

### Version
1.0.0

### Tech

HApi uses a number of open source projects to work properly:

* [Python Flask]
* [Python Flask-HTTPAuth]
* [Python YAML]

### Installation

You need Python 2.7 , Python Flask, Python GNUPG, Python YAML installed:

```sh
$ sudo pip install flask
$ sudo pip install Flask-HTTPAuth
$ sudo pip install pyyaml
```

### Config Example:

First of all you must have activated as admin level HAproxy statistics in the HAproxy configuration file:

```sh
stats socket /var/run/haproxy.stat level admin

```

#### Here is an HAproxy configuration example to balance between 2 lamp servers:

```sh
global
        log /dev/log   local0
        log 127.0.0.1   local1 notice
        maxconn 4096
        user haproxy
        group haproxy
        daemon
        stats socket /var/run/haproxy.stat user haproxy group haproxy level admin  # Stats socke location
defaults
        log     global
        mode    http
        option  httplog
        option  dontlognull
        retries 3
        option redispatch
        maxconn 2000
        contimeout     5000
        clitimeout     50000
        srvtimeout     50000

frontend http-frontend
    bind *:80
    reqadd X-Forwarded-Proto:\ http
    default_backend wwwbackend

backend wwwbackend
    balance roundrobin
    option httpclose
    option forwardfor
    cookie SRVNAME insert
    server lamp1 lamp1.lbserver:80 cookie S1 check
    server lamp2 lamp2.lbserver:80 cookie S2 check

``` 

#### Here is a HAPI configuration example example (HAPI code is running over '/opt/hapi' directory):

```yaml
socat: '/var/run/haproxy.stat'
server: 'lamp'
http-frontend:
-  'wwwbackend'
sslkey: '/opt/hapi/ssl/hapi.key'
sslcrt: '/opt/hapi/ssl/hapi.crt'
accesslog: '/opt/hapi/log/hapi_access.log'
logfile: '/opt/hapi/log/hapi.log'
user: 'yourUser'
password: 'yourPass'
bind: '0.0.0.0'
port: 6000
debug: True

```

### API Rest Usage:

Get HAproxy statistics (/loadBalancer/status)	 
```sh
curl -X GET https://hapiserver:6000/loadBalancer/status -k -uyourUser:yourPass
```
 Response example:
 ```json
[
    {
        "CurrConns": "1", 
        "Maxconn": "4096", 
        "Maxpipes": "0", 
        "Maxsock": "8206", 
        "Memmax_MB": "0", 
        "Name": "HAProxy", 
        "Nbproc": "1", 
        "Pid": "1651", 
        "PipesFree": "0", 
        "PipesUsed": "0", 
        "Process_num": "1", 
        "Release_date": "2013/06/17", 
        "Run_queue": "1", 
        "Tasks": "3", 
        "Ulimit-n": "8206", 
        "Uptime": "0d 0h18m44s", 
        "Uptime_sec": "1124", 
        "Version": "1.4.24", 
        "description": "", 
        "node": "vagrant-base-trusty-amd64"
    }
]

```
Get Node status (/loadBalancer/nodes/<status> (available input on status))
```sh
curl -X GET https://hapiserver:6000/loadBalancer/nodes/up -k -uyourUser:yourPass
```
Response example:
```json
[
    {
        "found": "True"
    }, 
    {
        "Nodes": [
            "wwwbackend: lamp1", 
            "wwwbackend: lamp2"
        ]
    }
]
```

Put over maintenance one backend node (for re-enable node use enable insted of disable on URI):
```sh
curl -X POST https://hapiserver:6000/loadBalancer/poolManager/http-frontend/disable/1 -k -uyourUser:yourPass
```
Response Example:
```json
{
  "action": "disable", 
  "backend": "['wwwbackend']", 
  "node": "1"
}
```

Please don't forget to put debug off on configuration file, once you setted up the service.

   [Python Flask]: <https://pypi.python.org/pypi/Flask>
   [Python Flask-HTTPAuth]: <https://pypi.python.org/pypi/Flask-HTTPAuth>
   [Python YAML]: <https://pypi.python.org/pypi/PyYAML>
