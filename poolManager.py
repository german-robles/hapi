#!/usr/bin/python
# -*- coding: utf-8 *-*

try:
	import os
	import subprocess
	import yaml
	import sys
except ImportError:
	print 'To run this script you must install missing modules'

class LbPoolManager :
	def getPoolConfig(self, vertical):
		imHere = os.path.dirname(os.path.abspath(__file__))
		with open("%s/hapi.conf" % (imHere), 'r') as ymlfile:
			config = yaml.load(ymlfile)
		backend = (config['%s'% (vertical)])
		return backend

	def nodeShutDown(self, backend, action, server, ui_id, socat):	
		for i in backend :
			try:
				subprocess.Popen(['echo "%s server %s/%s%s" | socat stdio %s'% (action, i, server, ui_id, socat)], shell=True)
			except OSError:
				print ('Can not perform action!')
	def getServerConfig(self):
		imHere = os.path.dirname(os.path.abspath(__file__))
		with open("%s/hapi.conf" % (imHere), 'r') as ymlfile:
			config = yaml.load(ymlfile)
		server = (config['server'])
		sslkey = (config['sslkey'])
		sslcrt = (config['sslcrt'])
		accesslog = (config['accesslog'])
		logfile = (config['logfile'])
		user = (config['user'])
		password = (config['password'])
		socat = (config['socat'])
		bind = (config['bind'])
		port = (config['port'])
		debug = (config['debug'])
		return server, sslkey, sslcrt, accesslog, logfile, user, password, socat, bind, port, debug

if __name__ == '__main__':
	LbPoolManager()