import boto3,datetime,time
import json
from flask import Flask, jsonify, Response
from boto3.session import Session
from influxdb import InfluxDBClient

app = Flask(__name__)

sessionPSG = Session(aws_access_key_id='xxxxxxxxxx',
	                    aws_secret_access_key='xxxxxxxxxxxx',
	                    region_name='xxxx')

sessionML = Session(aws_access_key_id='xxxxxxxxxxx',
                aws_secret_access_key='xxxxxxxxxxxxxxx',
                region_name='xxxxxxx')

sessionMD = Session(aws_access_key_id='xxxxxxxxxxx',
                aws_secret_access_key='xxxxxxxxxxxxxxx',
                region_name='xxxxxx')

sessionVX = Session(aws_access_key_id='xxxxxxxxxxxxx',
                aws_secret_access_key='xxxxxxxxxxxxxxxxx',
                region_name='xxxxxx')

instancePSG ='xxxxxxx'
instanceML = 'xxxxxxx'
instanceMD ='xxxxxx'
instanceVX='xxxxxxxx'


clientPSG=sessionPSG.client('cloudwatch')
clientML=sessionML.client('cloudwatch')
clientMD=sessionMD.client('cloudwatch')
clientVX=sessionVX.client('cloudwatch')

startTime = datetime.datetime.utcnow()-datetime.timedelta(seconds=600)
endTime = datetime.datetime.utcnow()
host='ec2-52-33-84-233.us-west-2.compute.amazonaws.com'
port=8086
user='root'
password='root'
dbname='AWS_MonitorDB'

client = InfluxDBClient(host, port, user, password, dbname)
def get_networkIn():
	# Instance: PSG, Metric: CPUUtilization
	responsePSG_NetworkIn = clientPSG.get_metric_statistics(
				 Namespace='AWS/EC2',
		                MetricName='NetworkIn',
		                Dimensions=[
		                        {
		                                'Name':'InstanceId',
		                                'Value':instancePSG
		                        },
		                ],
		                StartTime=startTime,
		                EndTime=endTime,
		                Period=300,
		                Statistics=[
		                        'Average','Maximum','SampleCount','Sum','Minimum'
		                ],
		                Unit='Bytes'
		            )
	# print(responseML_CPUUtilization)
		
	if len(responsePSG_NetworkIn)>0:
		if len(responsePSG_NetworkIn['Datapoints'])>0:
			json_body=[
        			{
            				"measurement": "networkIn",
            				"tags": {
                				"Instance-ID": instancePSG
           		 		},
            				"time": responsePSG_NetworkIn['Datapoints'][0]['Timestamp'],
            				"fields": {
                				"Instance-ID": instancePSG,
                				"Minimum":responsePSG_NetworkIn['Datapoints'][0]['Minimum'],
                				"Unit":responsePSG_NetworkIn['Datapoints'][0]['Unit'],
                				"Sum":responsePSG_NetworkIn['Datapoints'][0]['Sum'],
                				"SampleCount":responsePSG_NetworkIn['Datapoints'][0]['SampleCount'],
                				"Average":responsePSG_NetworkIn['Datapoints'][0]['Average'],
                				"Maximum":responsePSG_NetworkIn['Datapoints'][0]['Maximum']
            				}
        			}
    			]

			client.write_points(json_body)
		else:
			print("Datapoints is null.",instancePSG)
	else:
		print("Result is null.",instancePSG)


	responseML_NetworkIn = clientML.get_metric_statistics(
				 Namespace='AWS/EC2',
		                MetricName='NetworkIn',
		                Dimensions=[
		                        {
		                                'Name':'InstanceId',
		                                'Value':instanceML
		                        },
		                ],
		                StartTime=startTime,
		                EndTime=endTime,
		                Period=300,
		                Statistics=[
		                        'Average','Maximum','SampleCount','Sum','Minimum'
		                ],
		                Unit='Bytes'
		            )
	# print(responseML_CPUUtilization)
		
	if len(responseML_NetworkIn)>0:
		if len(responseML_NetworkIn['Datapoints'])>0:
			json_body=[
        			{
            				"measurement": "networkIn",
            				"tags": {
                				"Instance-ID": instanceML
           		 		},
            				"time": responseML_NetworkIn['Datapoints'][0]['Timestamp'],
            				"fields": {
                				"Instance-ID": instanceML,
                				"Minimum":responseML_NetworkIn['Datapoints'][0]['Minimum'],
                				"Unit":responseML_NetworkIn['Datapoints'][0]['Unit'],
                				"Sum":responseML_NetworkIn['Datapoints'][0]['Sum'],
                				"SampleCount":responseML_NetworkIn['Datapoints'][0]['SampleCount'],
                				"Average":responseML_NetworkIn['Datapoints'][0]['Average'],
                				"Maximum":responseML_NetworkIn['Datapoints'][0]['Maximum']
            				}
        			}
    			]

			client.write_points(json_body)
		else:
			print("Datapoints is null.",instanceML)
	else:
		print("Result is null.",instanceML)

	# responseMD_NetworkIn = clientMD.get_metric_statistics(
	# 			 Namespace='AWS/EC2',
	# 	                MetricName='NetworkIn',
	# 	                Dimensions=[
	# 	                        {
	# 	                                'Name':'InstanceId',
	# 	                                'Value':instanceMD
	# 	                        },
	# 	                ],
	# 	                StartTime=startTime,
	# 	                EndTime=endTime,
	# 	                Period=300,
	# 	                Statistics=[
	# 	                        'Average','Maximum','SampleCount','Sum','Minimum'
	# 	                ],
	# 	                Unit='Bytes'
	# 	            )
	# print(responseMD_NetworkIn)
		
	# if len(responseMD_NetworkIn)>0:
	# 	if len(responseMD_NetworkIn['Datapoints'])>0:
	# 		json_body=[
 #        			{
 #            				"measurement": "networkIn",
 #            				"tags": {
 #                				"Instance-ID": instanceMD
 #           		 		},
 #            				"time": responseMD_NetworkIn['Datapoints'][0]['Timestamp'],
 #            				"fields": {
 #                				"Instance-ID": instanceMD,
 #                				"Minimum":responseMD_NetworkIn['Datapoints'][0]['Minimum'],
 #                				"Unit":responseMD_NetworkIn['Datapoints'][0]['Unit'],
 #                				"Sum":responseMD_NetworkIn['Datapoints'][0]['Sum'],
 #                				"SampleCount":responseMD_NetworkIn['Datapoints'][0]['SampleCount'],
 #                				"Average":responseMD_NetworkIn['Datapoints'][0]['Average'],
 #                				"Maximum":responseMD_NetworkIn['Datapoints'][0]['Maximum']
 #            				}
 #        			}
 #    			]

	# 		client.write_points(json_body)
	# 	else:
	# 		print("Datapoints is null.",instanceMD)
	# else:
	# 	print("Result is null.",instanceMD)

	responseVX_NetworkIn = clientVX.get_metric_statistics(
				 Namespace='AWS/EC2',
		                MetricName='NetworkIn',
		                Dimensions=[
		                        {
		                                'Name':'InstanceId',
		                                'Value':instanceVX
		                        },
		                ],
		                StartTime=startTime,
		                EndTime=endTime,
		                Period=300,
		                Statistics=[
		                        'Average','Maximum','SampleCount','Sum','Minimum'
		                ],
		                Unit='Bytes'
		            )
	print(responseVX_NetworkIn)
		
	if len(responseVX_NetworkIn)>0:
		if len(responseVX_NetworkIn['Datapoints'])>0:
			json_body=[
        			{
            				"measurement": "networkIn",
            				"tags": {
                				"Instance-ID": instanceVX
           		 		},
            				"time": responseVX_NetworkIn['Datapoints'][0]['Timestamp'],
            				"fields": {
                				"Instance-ID": instanceVX,
                				"Minimum":responseVX_NetworkIn['Datapoints'][0]['Minimum'],
                				"Unit":responseVX_NetworkIn['Datapoints'][0]['Unit'],
                				"Sum":responseVX_NetworkIn['Datapoints'][0]['Sum'],
                				"SampleCount":responseVX_NetworkIn['Datapoints'][0]['SampleCount'],
                				"Average":responseVX_NetworkIn['Datapoints'][0]['Average'],
                				"Maximum":responseVX_NetworkIn['Datapoints'][0]['Maximum']
            				}
        			}
    			]

			client.write_points(json_body)
		else:
			print("Datapoints is null.",instanceVX)
	else:
		print("Result is null.",instanceVX)

if __name__ == '__main__':
    get_networkIn()
