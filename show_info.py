#!/usr/bin/python
# -*- coding: utf-8 *-*

import os
import subprocess
import json

class LbShowInfo :
	def showInfo (self,socat) :
		output = subprocess.check_output('echo "show info" | socat stdio %s'%(socat), shell=True) 
		Gresult = []
		result = {}
		for row in output.split('\n'):
			if ': ' in row:
				key = row.split(': ')[0]
				value = row.split(': ')[1]
				result[key.strip(' .')] = value.strip()
		Gresult.append(result)
		return json.dumps(Gresult, indent=4, sort_keys=True)


if __name__ == '__main__':
 	LbShowInfo()