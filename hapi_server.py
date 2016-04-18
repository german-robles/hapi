#!/usr/bin/python
# -*- coding: utf-8 *-*
import json
import os
from flask import Flask, url_for, jsonify
from flask.ext.httpauth import HTTPBasicAuth
from flask import make_response
from show_info import LbShowInfo
from poolManager import LbPoolManager
from nodeStatus import LbNodesInfo
import yaml
import logging
from logging.handlers import RotatingFileHandler
from flask import request
import ssl
from flask import escape


app = Flask(__name__)
poolManager = LbPoolManager()
(server, sslkey, sslcrt, accesslog, logfile, user, password, socat, bind, port, debug) = poolManager.getServerConfig()
nodesInfo = LbNodesInfo()
showInfo = LbShowInfo()
jResult = (showInfo.showInfo(socat))

auth = HTTPBasicAuth()
imHere = os.path.dirname(os.path.abspath(__file__))

@auth.get_password
def get_password(username):
	if username == user:
		return password
	return None

@auth.error_handler
def unauthorized():
	rip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
	app.logger.error('Unauthorized user trying to connect from ip: %s'%(rip))
	resp = make_response(jsonify({'error': 'Unauthorized access'}), 401)
	resp.headers['server'] = 'T101-CS'
	return resp

@app.route('/', methods=['GET'])
@auth.login_required
def api_root():

	# app.logger.warning('A warning occurred (%d apples)', 42)
	# app.logger.error('An error occurred')
	# app.logger.info('')
	greeting = '''
		                   ____                  
		                _.' :  `._               
		            .-.'`.  ;   .'`.-.           
		   __      / : ___\ ;  /___ ; \      __  
		 ,'_ ""--.:__;".-.";: :".-.":__;.--"" _`,
		 :' `.t""--.. '<@.`;_  ',@>` ..--""j.' `;
		      `:-.._J '-.-'L__ `-- ' L_..-;'     
		        "-.__ ;  .-"  "-.  : __.-"       
		            L ' /.------.\ ' J           
		             "-.   "--"   .-"            
		            __.l"-:_JL_;-";.__           
		         .-j/'.;  ;""""  / .'\"-.        
		       .' /:`. "-.:     .-" .';  `.      
		    .-"  / ;  "-. "-..-" .-"  :    "-.   
		 .+"-.  : :      "-.__.-"      ;-._   \  
		 ; \  `.; ;                    : : "+. ; 
		 :  ;   ; ;                    : ;  : \: 
		 ;  :   ; :                    ;:   ;  : 
		: \  ;  :  ;    Welcome, may   : ;  /  :: 
		;  ; :   ; :    the source    ;   :   ;: 
		:  :  ;  :  ;   be with U!    : :  ;  : ; 
		;\    :   ; :                ; ;     ; ; 
		: `."-;   :  ;              :  ;    /  ; 
		 ;    -:   ; :              ;  : .-"   : 
		 :\     \  :  ;            : \.-"      : 
		  ;`.    \  ; :            ;.'_..--  / ; 
		  :  "-.  "-:  ;          :/."      .'  :
		   \         \ :          ;/  __        :
		    \       .-`.\        /t-""  ":-+.   :
		     `.  .-"    `l    __/ /`. :  ; ; \  ;
		       \   .-" .-"-.-"  .' .'j \  /   ;/ 
		        \ / .-"   /.     .'.' ;_:'    ;  
		         :-""-.`./-.'     /    `.___.'   
		               \ `t  ._  /            
		                "-.t-._:'             

	Welcome to HApi for HAproxy, you can configure this app in the conf file. Refer to README for further information'''+'\n'
	greeting = make_response(greeting)
	greeting.headers['server'] = 'T101-CS'
	return greeting

@app.route('/loadBalancer/status', methods=['GET'])
@auth.login_required
def api_lb_show_info():
	jResult = (showInfo.showInfo(socat))	
	jResult = make_response(jResult)
	jResult.headers['server'] = 'T101-CS'
	return jResult	

@app.route('/loadBalancer/nodes/<status>', methods=['GET'])
@auth.login_required
def api_lb_show_nodes_status(status):

	if status == 'up':
		nodeStatus = (nodesInfo.getNodesStatus(server,socat,status='UP'))
		result = make_response(nodeStatus)
		result.headers['server'] = 'T101-CS'
		return result
	elif status == 'down':
		nodeStatus = (nodesInfo.getNodesStatus(server,socat,status='DOWN'))
		result = make_response(nodeStatus)
		result.headers['server'] = 'T101-CS'
		return result
	elif status == 'maint':
		nodeStatus = (nodesInfo.getNodesStatus(server,socat,status='MAINT'))
		result = make_response(nodeStatus)
		result.headers['server'] = 'T101-CS'	
		return result
	else:
		nstatusEx = make_response('Can not perform action %s not recognized'% escape(status) + '\n')
		nstatusEx.headers['server'] = 'T101-CS'
		return nstatusEx			

@app.route('/loadBalancer/poolManager/<vertical>/<action>/<int:ui_id>', methods=['POST'])
@auth.login_required
def api_lb_pool_manager(vertical, action, ui_id):
	try:
		backend = poolManager.getPoolConfig(vertical)
	except:
		pmEx = make_response('Can not found config, unable to perform requested action')
		pmEx.headers['server'] = 'T101-CS'
		return pmEx
	if action == 'enable' or action == 'disable':
		pass
	else:
		actionEx = make_response('Can not perform action %s not recognized'% escape(action) + '\n')
		actionEx.headers['server'] = 'T101-CS'
		return actionEx	       
	poolManager.nodeShutDown(backend, action, server, ui_id, socat)		
	pmResp = make_response(jsonify({'backend': '%s'%(backend), 'node' : '%s'%(ui_id), 'action' : '%s'%(action)}), 200)  
	pmResp.headers['server'] = 'T101-CS'
	return pmResp
ssl_context=('', '')
if __name__ == '__main__':
	#log.setLevel(logging.ERROR)		
	handler = RotatingFileHandler(logfile, maxBytes=10000, backupCount=1)
	handler.setLevel(logging.DEBUG)
	app.logger.addHandler(handler)
	logger = logging.getLogger('werkzeug')
	handler = logging.FileHandler(accesslog)
	logger.addHandler(handler)	
	app.logger.addHandler(handler)

	app.run(host=bind, port=port, debug=debug, ssl_context=(sslcrt, sslkey, ssl.PROTOCOL_TLSv1))