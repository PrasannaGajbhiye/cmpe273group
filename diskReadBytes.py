import boto3,datetime,time
import json
from flask import Flask, jsonify, Response
from boto3.session import Session
from influxdb import InfluxDBClient

app = Flask(__name__)

sessionPSG = Session(aws_access_key_id='xxxxxxxx',
	                    aws_secret_access_key='xxxxxxx',
	                    region_name='xxxx')

sessionML = Session(aws_access_key_id='xxxxxxxxx',
                aws_secret_access_key='xxxxxxxxxx',
                region_name='xxxx')

sessionMD = Session(aws_access_key_id='xxxxxxxxxx',
                aws_secret_access_key='xxxxxxxxxxxx',
                region_name='xxxxx')

sessionVX = Session(aws_access_key_id='xxxxxxxxxxx',
                aws_secret_access_key='xxxxxxxxxxxxx',
                region_name='xxxxx')

instancePSG ='xxxxxx'
instanceML = 'xxxxxx'
instanceMD ='xxxxxxx'
instanceVX='xxxxxxx'


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
def get_diskReadBytes():
	# Instance: PSG, Metric: CPUUtilization
	responsePSG_DiskReadBytes = clientPSG.get_metric_statistics(
				 Namespace='AWS/EC2',
		                MetricName='DiskReadBytes',
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
		
	if len(responsePSG_DiskReadBytes)>0:
		if len(responsePSG_DiskReadBytes['Datapoints'])>0:
			json_body=[
        			{
            				"measurement": "diskReadBytes",
            				"tags": {
                				"Instance-ID": instancePSG
           		 		},
            				"time": responsePSG_DiskReadBytes['Datapoints'][0]['Timestamp'],
            				"fields": {
                				"Instance-ID": instancePSG,
                				"Minimum":responsePSG_DiskReadBytes['Datapoints'][0]['Minimum'],
                				"Unit":responsePSG_DiskReadBytes['Datapoints'][0]['Unit'],
                				"Sum":responsePSG_DiskReadBytes['Datapoints'][0]['Sum'],
                				"SampleCount":responsePSG_DiskReadBytes['Datapoints'][0]['SampleCount'],
                				"Average":responsePSG_DiskReadBytes['Datapoints'][0]['Average'],
                				"Maximum":responsePSG_DiskReadBytes['Datapoints'][0]['Maximum']
            				}
        			}
    			]

			client.write_points(json_body)
		else:
			print("Datapoints is null.",instancePSG)
	else:
		print("Result is null.",instancePSG)


	responseML_DiskReadBytes = clientML.get_metric_statistics(
				 Namespace='AWS/EC2',
		                MetricName='DiskReadBytes',
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
		
	if len(responseML_DiskReadBytes)>0:
		if len(responseML_DiskReadBytes['Datapoints'])>0:
			json_body=[
        			{
            				"measurement": "diskReadBytes",
            				"tags": {
                				"Instance-ID": instanceML
           		 		},
            				"time": responseML_DiskReadBytes['Datapoints'][0]['Timestamp'],
            				"fields": {
                				"Instance-ID": instanceML,
                				"Minimum":responseML_DiskReadBytes['Datapoints'][0]['Minimum'],
                				"Unit":responseML_DiskReadBytes['Datapoints'][0]['Unit'],
                				"Sum":responseML_DiskReadBytes['Datapoints'][0]['Sum'],
                				"SampleCount":responseML_DiskReadBytes['Datapoints'][0]['SampleCount'],
                				"Average":responseML_DiskReadBytes['Datapoints'][0]['Average'],
                				"Maximum":responseML_DiskReadBytes['Datapoints'][0]['Maximum']
            				}
        			}
    			]

			client.write_points(json_body)
		else:
			print("Datapoints is null.",instanceML)
	else:
		print("Result is null.",instanceML)

	# responseMD_DiskReadBytes = clientMD.get_metric_statistics(
	# 			 Namespace='AWS/EC2',
	# 	                MetricName='DiskReadBytes',
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
	# print(responseMD_DiskReadBytes)
		
	# if len(responseMD_DiskReadBytes)>0:
	# 	if len(responseMD_DiskReadBytes['Datapoints'])>0:
	# 		json_body=[
 #        			{
 #            				"measurement": "diskReadBytes",
 #            				"tags": {
 #                				"Instance-ID": instanceMD
 #           		 		},
 #            				"time": responseMD_DiskReadBytes['Datapoints'][0]['Timestamp'],
 #            				"fields": {
 #                				"Instance-ID": instanceMD,
 #                				"Minimum":responseMD_DiskReadBytes['Datapoints'][0]['Minimum'],
 #                				"Unit":responseMD_DiskReadBytes['Datapoints'][0]['Unit'],
 #                				"Sum":responseMD_DiskReadBytes['Datapoints'][0]['Sum'],
 #                				"SampleCount":responseMD_DiskReadBytes['Datapoints'][0]['SampleCount'],
 #                				"Average":responseMD_DiskReadBytes['Datapoints'][0]['Average'],
 #                				"Maximum":responseMD_DiskReadBytes['Datapoints'][0]['Maximum']
 #            				}
 #        			}
 #    			]

	# 		client.write_points(json_body)
	# 	else:
	# 		print("Datapoints is null.",instanceMD)
	# else:
	# 	print("Result is null.",instanceMD)

	responseVX_DiskReadBytes = clientVX.get_metric_statistics(
				 Namespace='AWS/EC2',
		                MetricName='DiskReadBytes',
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
	print(responseVX_DiskReadBytes)
		
	if len(responseVX_DiskReadBytes)>0:
		if len(responseVX_DiskReadBytes['Datapoints'])>0:
			json_body=[
        			{
            				"measurement": "diskReadBytes",
            				"tags": {
                				"Instance-ID": instanceVX
           		 		},
            				"time": responseVX_DiskReadBytes['Datapoints'][0]['Timestamp'],
            				"fields": {
                				"Instance-ID": instanceVX,
                				"Minimum":responseVX_DiskReadBytes['Datapoints'][0]['Minimum'],
                				"Unit":responseVX_DiskReadBytes['Datapoints'][0]['Unit'],
                				"Sum":responseVX_DiskReadBytes['Datapoints'][0]['Sum'],
                				"SampleCount":responseVX_DiskReadBytes['Datapoints'][0]['SampleCount'],
                				"Average":responseVX_DiskReadBytes['Datapoints'][0]['Average'],
                				"Maximum":responseVX_DiskReadBytes['Datapoints'][0]['Maximum']
            				}
        			}
    			]

			client.write_points(json_body)
		else:
			print("Datapoints is null.",instanceVX)
	else:
		print("Result is null.",instanceVX)

if __name__ == '__main__':
    get_diskReadBytes()
