import boto3,datetime,time
import json
from flask import Flask, jsonify, Response
from boto3.session import Session
from influxdb import InfluxDBClient

app = Flask(__name__)

sessionPSG = Session(aws_access_key_id='xxxxxxxx',
	                    aws_secret_access_key='xxxxxxxx',
	                    region_name='xxxxxx')

sessionML = Session(aws_access_key_id='xxxxxxx',
                aws_secret_access_key='xxxxxxxxx',
                region_name='xxxxxxx')

sessionMD = Session(aws_access_key_id='xxxxxxxxxxx',
                aws_secret_access_key='xxxxxxxxxxxxxx',
                region_name='xxxxx')

sessionVX = Session(aws_access_key_id='xxxxxxx',
                aws_secret_access_key='xxxxxxxxxx',
                region_name='xxxxx')

instancePSG ='xxxxx'
instanceML = 'xxxx'
instanceMD ='xxxxx'
instanceVX='xxxxx'


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
def get_networkOut():
	# Instance: PSG, Metric: CPUUtilization
	responsePSG_NetworkOut = clientPSG.get_metric_statistics(
				 Namespace='AWS/EC2',
		                MetricName='NetworkOut',
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
		
	if len(responsePSG_NetworkOut)>0:
		if len(responsePSG_NetworkOut['Datapoints'])>0:
			json_body=[
        			{
            				"measurement": "networkOut",
            				"tags": {
                				"Instance-ID": instancePSG
           		 		},
            				"time": responsePSG_NetworkOut['Datapoints'][0]['Timestamp'],
            				"fields": {
                				"Instance-ID": instancePSG,
                				"Minimum":responsePSG_NetworkOut['Datapoints'][0]['Minimum'],
                				"Unit":responsePSG_NetworkOut['Datapoints'][0]['Unit'],
                				"Sum":responsePSG_NetworkOut['Datapoints'][0]['Sum'],
                				"SampleCount":responsePSG_NetworkOut['Datapoints'][0]['SampleCount'],
                				"Average":responsePSG_NetworkOut['Datapoints'][0]['Average'],
                				"Maximum":responsePSG_NetworkOut['Datapoints'][0]['Maximum']
            				}
        			}
    			]

			client.write_points(json_body)
		else:
			print("Datapoints is null.",instancePSG)
	else:
		print("Result is null.",instancePSG)


	responseML_NetworkOut = clientML.get_metric_statistics(
				 Namespace='AWS/EC2',
		                MetricName='NetworkOut',
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
		
	if len(responseML_NetworkOut)>0:
		if len(responseML_NetworkOut['Datapoints'])>0:
			json_body=[
        			{
            				"measurement": "networkOut",
            				"tags": {
                				"Instance-ID": instanceML
           		 		},
            				"time": responseML_NetworkOut['Datapoints'][0]['Timestamp'],
            				"fields": {
                				"Instance-ID": instanceML,
                				"Minimum":responseML_NetworkOut['Datapoints'][0]['Minimum'],
                				"Unit":responseML_NetworkOut['Datapoints'][0]['Unit'],
                				"Sum":responseML_NetworkOut['Datapoints'][0]['Sum'],
                				"SampleCount":responseML_NetworkOut['Datapoints'][0]['SampleCount'],
                				"Average":responseML_NetworkOut['Datapoints'][0]['Average'],
                				"Maximum":responseML_NetworkOut['Datapoints'][0]['Maximum']
            				}
        			}
    			]

			client.write_points(json_body)
		else:
			print("Datapoints is null.",instanceML)
	else:
		print("Result is null.",instanceML)

	# responseMD_NetworkOut = clientMD.get_metric_statistics(
	# 			 Namespace='AWS/EC2',
	# 	                MetricName='NetworkOut',
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
	# print(responseMD_NetworkOut)
		
	# if len(responseMD_NetworkOut)>0:
	# 	if len(responseMD_NetworkOut['Datapoints'])>0:
	# 		json_body=[
 #        			{
 #            				"measurement": "networkOut",
 #            				"tags": {
 #                				"Instance-ID": instanceMD
 #           		 		},
 #            				"time": responseMD_NetworkOut['Datapoints'][0]['Timestamp'],
 #            				"fields": {
 #                				"Instance-ID": instanceMD,
 #                				"Minimum":responseMD_NetworkOut['Datapoints'][0]['Minimum'],
 #                				"Unit":responseMD_NetworkOut['Datapoints'][0]['Unit'],
 #                				"Sum":responseMD_NetworkOut['Datapoints'][0]['Sum'],
 #                				"SampleCount":responseMD_NetworkOut['Datapoints'][0]['SampleCount'],
 #                				"Average":responseMD_NetworkOut['Datapoints'][0]['Average'],
 #                				"Maximum":responseMD_NetworkOut['Datapoints'][0]['Maximum']
 #            				}
 #        			}
 #    			]

	# 		client.write_points(json_body)
	# 	else:
	# 		print("Datapoints is null.",instanceMD)
	# else:
	# 	print("Result is null.",instanceMD)

	responseVX_NetworkOut = clientVX.get_metric_statistics(
				 Namespace='AWS/EC2',
		                MetricName='NetworkOut',
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
	print(responseVX_NetworkOut)
		
	if len(responseVX_NetworkOut)>0:
		if len(responseVX_NetworkOut['Datapoints'])>0:
			json_body=[
        			{
            				"measurement": "networkOut",
            				"tags": {
                				"Instance-ID": instanceVX
           		 		},
            				"time": responseVX_NetworkOut['Datapoints'][0]['Timestamp'],
            				"fields": {
                				"Instance-ID": instanceVX,
                				"Minimum":responseVX_NetworkOut['Datapoints'][0]['Minimum'],
                				"Unit":responseVX_NetworkOut['Datapoints'][0]['Unit'],
                				"Sum":responseVX_NetworkOut['Datapoints'][0]['Sum'],
                				"SampleCount":responseVX_NetworkOut['Datapoints'][0]['SampleCount'],
                				"Average":responseVX_NetworkOut['Datapoints'][0]['Average'],
                				"Maximum":responseVX_NetworkOut['Datapoints'][0]['Maximum']
            				}
        			}
    			]

			client.write_points(json_body)
		else:
			print("Datapoints is null.",instanceVX)
	else:
		print("Result is null.",instanceVX)

if __name__ == '__main__':
    get_networkOut()
