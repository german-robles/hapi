#!/usr/bin/python
# -*- coding: utf-8 *-*

import os
import subprocess
import json

class LbNodesInfo :
	def getNodesStatus (self, server, socat, status) :
		try:
			output = subprocess.check_output('echo "show stat" | socat stdio %s | grep %s[0-9] | grep %s'%(socat, server, status), shell=True)	
			Gresult = []
			state = {'found' : 'True'}
			Gresult.append(state)
			Nresult = []
			for row in output.split('\n'):
				if ',' in row:
					backend = row.split(',')[0]
					node = row.split(',')[1]
					Nresult.append(backend.strip()+': '+node)
			Nodes = {'Nodes': Nresult}
			Gresult.append(Nodes)
			nodeStatus = json.dumps(Gresult, indent=4, sort_keys=True)
			return nodeStatus
		except 	Exception:
			Gresult = []
			state = {'found' : 'False'}
			Gresult.append(state)
			code = json.dumps(Gresult, indent=4, sort_keys=True)
			return code
			

		
				
if __name__ == '__main__':
	LbNodesInfo()