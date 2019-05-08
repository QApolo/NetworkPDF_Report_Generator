#!/usr/bin/env python
import httplib
import sys
import time
from datetime import datetime
import json

httpdata = {
    "web": "url",
    "timeload": 0,
    "rec_bytes": 0,
    "speed_download": 0,
    "status": "down"
}
def getResourceName(resource):
    index = -1
    name = ""
    while resource[index] != '/' and abs(index) <= len(resource):
        name = name + str(resource[index])
        index = index -1 
    if len(name) < 5:
        name = "elif"
    return name[::-1]

def check_webserver(address, port, resource):
    #create connection
    name = getResourceName(resource)
    print(getResourceName(resource))
    httpdata['web'] = address
    if not resource.startswith('/'):
        resource = '/' + resource
    try:
        conn = httplib.HTTPConnection(address, port)
        print('HTTP connection created successfully')
        #make    request
    	t1 = time.time()
        req = conn.request('GET', resource)
        
    	t2 = time.time()
    	print("time %.20f seconds" %(t2 - t1))
        httpdata['timeload'] = t2 - t1
        print('request for %s successful' % resource)
        # get response
        response = conn.getresponse()
        f = open(name, "w")
        size = len(response.read())
        print("size %d" %size)
        httpdata['rec_bytes'] = size

        httpdata['speed_download'] = size * 8 / (t2-t1)
        f.write( response.read())
        f.close()

        print('response status: %s' % response.status)
        print("status %s" %(response.reason))
        httpdata['status'] = response.reason
    except sock.error as e:
        print ("HTTP connection failed: %s' % e")
        return False
    finally:
        conn.close()
        jsondata = json.dumps(httpdata)
        w = open("information.json", "w")
        w.write(jsondata)
    	print ('HTTP connection closed successfully')
    	if response.status in [200, 301]:
        		return True
	else:
    		return False
check_webserver("localhost", 80, "/")