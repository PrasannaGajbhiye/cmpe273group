#!/usr/bin/env python
import datetime,time,os,commands, subprocess,logging,urllib2, thread
from flask import Flask, jsonify, render_template, request

from datetime import timedelta
from flask import make_response, current_app
from functools import update_wrapper



"""
@Author: Michael Dong
@Date: Nov 26, 2015
@ScriptName:Linux Realtime Monitor


To use this script, flask must be installed on the machine. 
To begin with a bare Linux, do the following:
1. install pip:
$ wget https://bootstrap.pypa.io/get-pip.py 
$ sudo python get-pip.py

2. install flask:
$ sudo pip install flask

3. make sysinfo.py executable:
$ chmod a+x sysinfo.py

4. run the script:
$ ./sysinfo.py &

5.if you want to know the public IP for this machine:
$ curl -s ipecho.net/plain

6.if you want to know the internal IP for this machine:
$ hostname -I

"""

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator





app = Flask(__name__,static_url_path='/static')

def getCPUusage():
    # old method using top command
    idleCPU = commands.getoutput("top -b -n 2 -d0.01 | grep Cpu | tail -n 1 | awk -F\",\" '{print $4}' | cut -f 1 -d '.'")
    # cpuUsed = 100-int(idleCPU)
    
    #new method using mpstat command
    # cpuUsed = commands.getoutput("mpstat | grep all |awk '{print $4}'")
    #unit: Percent(integer part only)
    return 100-int(idleCPU)
    
def getMemoryUsed():
    usedMemory = commands.getoutput("free -m | grep Mem | awk '{print $3}'")
    #unit: MB
    return usedMemory

def getMemoryFree():
    memoryFree = commands.getoutput("free -m | grep Mem | awk '{print $4}'")
    #unit: MB
    return memoryFree
    
def getTotalMemory():
    totalMemory = commands.getoutput("free -m | grep Mem | awk '{print $2}'")
    #unit: MB
    return totalMemory
  
last_logged = [0,0]  
  
#get HTTP request per second  
def getHTTPQPS():
    newRequestNo = int(commands.getoutput("wc -l ./access.log | awk '{print $1}'"))
    if last_logged[0] == 0:
        last_logged[0] = time.time()
        last_logged[1] = newRequestNo   
    current_time = time.time()
    
    
    HTTPQPS = (newRequestNo - last_logged[1]) / (current_time - last_logged[0])
    last_logged[0] = current_time
    last_logged[1] = newRequestNo
    if HTTPQPS < 0:
        HTTPQPS = 0 
    return HTTPQPS
    
#get TCP request per second 
def getTCPQPS():
    #to do
    TCPQPS = 0
    return TCPQPS
    
def getDiskReads():
    diskReads = commands.getoutput("iostat -d -k | tail -n +4 | awk 'BEGIN { read=0 }{ read=read+$3  } END {print read}'")
    return diskReads
    
def getDiskWrites():
    diskWrites = commands.getoutput("iostat -d -k | tail -n +4 | awk 'BEGIN { write=0 }{ write=write+$4  } END {print write}'")
    return diskWrites

networkInTotalAtTime = [0, 0]
networkOutTotalAtTime = [0, 0]

def getNetworkInTotal():
    networkIn = 0
    
    #unit KB
    newNetworkInTotal = commands.getoutput("cat /proc/net/dev | tail -n +3 |cut -d':' -f2|awk 'BEGIN{totalIn=0} {totalIn=totalIn+$1} END{print totalIn/1024}'")
    if networkInTotalAtTime[1] == 0:
        networkInTotalAtTime[1] = int(float(newNetworkInTotal))
        networkInTotalAtTime[0] = time.time()
    else:
        currentTime = time.time()
        networkIn = (int(float(newNetworkInTotal)) - networkInTotalAtTime[1])/(currentTime - networkInTotalAtTime[0])
        networkInTotalAtTime[0] = currentTime
        networkInTotalAtTime[1] = int(float(newNetworkInTotal))
        
    return networkIn
    
def getNetworkOutTotal():
    networkOut = 0
    
    #unit KB
    newNetworkOutTotal = commands.getoutput("cat /proc/net/dev | tail -n +3 |cut -d':' -f2|awk 'BEGIN{totalOut=0} {totalOut=totalOut+$9} END{print totalOut/1024}'")
    if networkOutTotalAtTime[1] == 0:
        networkOutTotalAtTime[1] = int(float(newNetworkOutTotal))
        networkOutTotalAtTime[0] = time.time()
    else:
        currentTime = time.time()
        networkOut = (int(float(newNetworkOutTotal)) - networkOutTotalAtTime[1])/(currentTime - networkOutTotalAtTime[0])
        networkOutTotalAtTime[0] = currentTime
        networkOutTotalAtTime[1] = int(float(newNetworkOutTotal))
    
    return networkOut


@app.route('/cpu', methods=['GET','OPTIONS'])
@crossdomain(origin='*')
def getCPU():
    cpu = getCPUusage()
    return jsonify({"Datapoints":[{"Maximum":cpu}]})
    
@app.route('/memory', methods=['GET','OPTIONS'])
@crossdomain(origin='*')
def getMemory():
    memory = getMemoryUsed()
    return jsonify({"Datapoints":[{"Maximum":memory}]})
    
@app.route('/HTTPQPS', methods=['GET','OPTIONS'])
@crossdomain(origin='*')
def getQPS():
    httpqps = getHTTPQPS()
    return jsonify({"Datapoints":[{"Maximum":httpqps}]})
    
@app.route('/diskreads', methods=['GET','OPTIONS'])
@crossdomain(origin='*')
def getReads():
    reads = getDiskReads()
    return jsonify({"Datapoints":[{"Maximum":reads}]})
    
@app.route('/diskwrites', methods=['GET','OPTIONS'])
@crossdomain(origin='*')
def getWrites():
    writes = getDiskWrites()
    return jsonify({"Datapoints":[{"Maximum":writes}]})
    
@app.route('/networkin', methods=['GET','OPTIONS'])
@crossdomain(origin='*')
def getNetworkIn():
    networkin = getNetworkInTotal()
    return jsonify({"Datapoints":[{"Maximum":networkin}]})
    
@app.route('/networkout', methods=['GET','OPTIONS'])
@crossdomain(origin='*')
def getNetworkOut():
    networkout = getNetworkOutTotal()
    return jsonify({"Datapoints":[{"Maximum":networkout}]})
    





    
    
cpuSpikePIDs = []
@app.route('/startcpuspike', methods=['GET'])
def startcpuspike():

    currentCPU = getCPUusage()
    if float(currentCPU) <= 80.0:
        proc = subprocess.Popen("for i in 1; do while : ; do : ; done & done", shell=True)
        cpuSpikePIDs.append(proc.pid+1)
    return jsonify({"pid":cpuSpikePIDs, "currentCPU":currentCPU})

@app.route('/stopcpuspike', methods=['GET'])
def stopcpuspike():
    ret = 1
    currentCPU = getCPUusage()
    if float(currentCPU) > 50.0:
        if cpuSpikePIDs:
            for pid in cpuSpikePIDs:
                os.system('kill -9 ' +str(pid))
    return jsonify({"ret":ret, "currentCPU":currentCPU})


@app.route('/startmemoryspike', methods=['GET'])
def startmemoryspike():
    currentMemory = getMemoryUsed()
    freeMemory = getMemoryFree()
    diskSize = str(round(int(freeMemory) * 0.6))
    os.system("mkdir -p /media/ramdisk; mount -t tmpfs -o size=%sM tmpfs /media/ramdisk/; cat /dev/zero > /media/ramdisk/large"%diskSize)
    return jsonify({"currentMemory":currentMemory+diskSize})
    

@app.route('/stopmemoryspike', methods=['GET'])
def stopmemoryspike():
    currentMemory = getMemoryUsed()
    freeMemory = getMemoryFree()
    os.system("umount /dev/shm; rm -rf /media/ramdisk/*;")
    return jsonify({"currentMemory":currentMemory})
    
@app.route('/startnetworkoutspike',methods=['GET'])
def startnetworkoutspike():
    networkout = getNetworkOutTotal()
    os.system("nc -l 5555 < ./testzerofile2M.dat")
    return jsonify({"networkout":networkout})
    
# @app.route('/startnetworkinspike',methods=['GET'])
# def startnetworkinspike():
#     networkin = getNetworkInTotal()
#     os.system("nc -l 5555 < ./testzerofile2M.dat")
#     return jsonify({"networkin":networkin})


@app.route('/requesttest', methods=['GET'])
def requesttest():
    return jsonify({"1":1})



# @app.route('/startrequestspike', methods=['GET'])
# def startrequestspike():
#     for i in xrange(5):
#         # thread.start_new_thread(urllib2.urlopen("http://localhost:5000/requesttest"), None)
#         urllib2.urlopen("http://localhost:5000/requesttest")
#     return 1
    

@app.route('/realtime_monitor/', methods=['GET'])
def getUsage():
    cpuUsage = getCPUusage()
    usedMemory = getMemoryUsed()
    totalMemory = getTotalMemory()
    diskReads = getDiskReads()
    diskWrites = getDiskWrites()
    networkInTotal = getNetworkInTotal()
    networkOutTotal = getNetworkOutTotal()
    HTTPQPS = getHTTPQPS()
    usage = {"cpuUsage":cpuUsage, "usedMemory":usedMemory,"totalMemory":totalMemory, "diskReads":diskReads ,"diskWrites":diskWrites, "HTTPQPS":HTTPQPS, "networkInTotal":networkInTotal, "networkOutTotal":networkOutTotal }
    return jsonify(usage)








@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)


@app.route('/')
def getIndex():
    return render_template('sysinfo.html')





if __name__ == '__main__':
    #log HTTP requests into access.log file
    logger = logging.getLogger('werkzeug')
    handler = logging.FileHandler('access.log')
    logger.addHandler(handler)

    # Add the handler to Flask's logger for cases
    #  where Werkzeug isn't used as the underlying WSGI server.
    app.logger.addHandler(handler)
    
    
    app.run(debug=True, host='0.0.0.0')
    