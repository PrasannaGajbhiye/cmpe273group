import boto3,datetime,time
from flask import Flask, jsonify, render_template, request,send_from_directory
from boto3.session import Session


from datetime import timedelta
from flask import make_response, current_app
from functools import update_wrapper


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


accounts = {"PSG":{"aws_access_key_id":'xxxxxxxxxxxxxxx', "aws_secret_access_key":'xxxxxxxxxxxxxxxxx', "region_name":'xxxxxxxx', "instances":[{'xxxxxx':{"sysinfo_address": "http://xx.xx.xx.xxxx"}}]},\
            "MD":{"aws_access_key_id":'xxxxxxxxxxxxxxxx', "aws_secret_access_key":'xxxxxxxxxxxxxxxxx', "region_name":'xxxx', "instances":[{'xxxxxx':{"sysinfo_address": "http://xx.xx.xx.xxxx"}}]},\
            'ML':{"aws_access_key_id":'xxxxxxxxxxxxxxx',"aws_secret_access_key":'xxxxxxxxxxxxxxxxxx',"region_name":'xxxxx',"instances":[{'xxxxxx':{"sysinfo_address": "http://xx.xx.xx.xxxx"}}]}}


metrics = {"cpu":{ "metricName":"CPUUtilization", "statistics":"Maximum", "unit":"Percent"},\
            # "memory":{"metricName":"Memory", "statistics":"Maximum", "unit":"Percent"},\
            "diskRead":{"metricName":"DiskReadBytes", "statistics":"Maximum", "unit":"Bytes"},\
            "diskWrite":{"metricName":"DiskWriteBytes", "statistics":"Maximum", "unit":"Bytes"},\
            "networkIn":{"metricName":"NetworkIn", "statistics":"Maximum", "unit":"Bytes"},\
            "networkOut":{"metricName":"NetworkOut", "statistics":"Maximum", "unit":"Bytes"}\
            # "requests":{"metricName":"Request", "statistics":"Maximum", "unit":"Percent"}
        }

def getSessionClient(aws_access_key_id, aws_secret_access_key, region_name):
    session = Session(aws_access_key_id = aws_access_key_id, aws_secret_access_key = aws_secret_access_key, region_name = region_name)
    client = session.client('cloudwatch')
    return client

@app.route('/account/', methods=['POST'])
def postAccount():
    account_name = request.form['account_name']
    aws_access_key_id = request.form['aws_access_key_id']
    aws_secret_access_key = request.form['aws_secret_access_key']
    region_name = request.form['region_name']
    instance_id = request.form['instance_id']
    instance_sysinfo_address = request.form['instance_sysinfo_address']
    if account_name not in accounts:
        accounts[account_name] =  {"aws_access_key_id":aws_access_key_id, "aws_secret_access_key":aws_secret_access_key, "region_name":region_name, "instances":[{instance_id:{"sysinfo_address":instance_sysinfo_address}}]}   
    else:
        accounts[account_name]["aws_access_key_id"] = aws_access_key_id
        accounts[account_name]["aws_secret_access_key"] = aws_secret_access_key
        accounts[account_name]["region_name"] = region_name
        accounts[account_name]["instances"][instance_id] = {"instance_sysinfo_address":instance_sysinfo_address}
        

@app.route('/instance/', methods=['POST'])
def postInstance():
    account_name = request.form["account_name"]
    instance_id = request.form["instance_id"]
    instance_sysinfo_address = request.form['instance_sysinfo_address']
    if account_name in accounts:
        accounts[account_name]["instances"][instance_id] = {"instance_sysinfo_address":instance_sysinfo_address}
    else:
        pass
        

@app.route('/instance/<account_name>/<int:instance_no>/<metric_name>/<data_format>/', methods=['GET'])
def getUsage(account_name,instance_no,metric_name, data_format=""):
    if account_name not in accounts:
        return None
    if instance_no < 0 or instance_no >len(accounts[account_name])-1:
        return None
    if metric_name not in metrics:
        return None
	
    account = accounts[account_name]
    client = getSessionClient(account['aws_access_key_id'], account['aws_secret_access_key'], account['region_name'])
    # collective={}
    
    startTime = datetime.datetime.now()-datetime.timedelta(seconds=300)
    endTime = datetime.datetime.now()
	# Instance: PSG, Metric: CPUUtilization 
    response = client.get_metric_statistics(
	                Namespace='AWS/EC2',
	                MetricName=metrics[metric_name]['metricName'],
	                Dimensions=[
	                        {
	                                'Name':'InstanceId',
	                                'Value':account['instances'][instance_no].keys()[0]
	                        },
	                ],
	                StartTime=startTime,
	                EndTime=endTime,
	                Period=60,
	                Statistics=[
                        metrics[metric_name]['statistics']
	                        # 'Average','Maximum','SampleCount','Sum','Minimum'
	                ],
	                Unit=metrics[metric_name]['unit']
	            )
                
    instance_id = account['instances'][instance_no].keys()[0]

    if data_format == 'json':
        return jsonify(response)
    elif data_format == 'html':
        print metric_name
        return render_template('instance_monitor.html', account_name=account_name, response=response, instance_no=instance_no, metric=metric_name,instance_address=accounts[account_name]["instances"][instance_no][instance_id]["sysinfo_address"])



@app.route('/longperiod/instance/<account_name>/<int:instance_no>/<metric_name>/<int:period>/<interval>/', methods=['GET','OPTIONS'])
@crossdomain(origin='*')
def getLongPeriod(account_name,instance_no,metric_name,period, interval):
    if account_name not in accounts:
        return None
    if instance_no < 0 or instance_no >len(accounts[account_name])-1:
        return None
    if metric_name not in metrics:
        return None
	
    account = accounts[account_name]
    client = getSessionClient(account['aws_access_key_id'], account['aws_secret_access_key'], account['region_name'])
    # collective={}
    
    periodInSeconds = period * 60
    startTime = datetime.datetime.now()-datetime.timedelta(seconds=periodInSeconds)
    endTime = datetime.datetime.now()
	# Instance: PSG, Metric: CPUUtilization 
    response = client.get_metric_statistics(
	                Namespace='AWS/EC2',
	                MetricName=metrics[metric_name]['metricName'],
	                Dimensions=[
	                        {
	                                'Name':'InstanceId',
	                                'Value':account['instances'][instance_no].keys()[0]
	                        },
	                ],
	                StartTime=startTime,
	                EndTime=endTime,
                    Period=60,
                    # Period=periodInSeconds,
	                Statistics=[
                        metrics[metric_name]['statistics']
	                        # 'Average','Maximum','SampleCount','Sum','Minimum'
	                ],
	                Unit=metrics[metric_name]['unit']
	            )
                
    # instance_id = account['instances'][instance_no].keys()[0]

    # if data_format == 'json':
    return jsonify(response)    
    
    
    # return render_template('longperiod_monitor.html')




@app.route('/accounts/', methods=['GET'])
def getAccounts():
    if not accounts:
        return None
    return render_template('account_monitor.html', accounts=accounts)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)


@app.route('/')
def getIndex():
    return render_template('aws_monitor.html', accounts=accounts)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')