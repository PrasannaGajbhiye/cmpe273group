import boto3,datetime,time
import json
from flask import Flask, jsonify, Response
from boto3.session import Session
from influxdb import InfluxDBClient

app = Flask(__name__)

sessionPSG = Session(aws_access_key_id='xxxxxxxx',
	                    aws_secret_access_key='xxxxxxxx',
	                    region_name='xxxxx')

sessionML = Session(aws_access_key_id='xxxxxxx',
                aws_secret_access_key='xxxxxxxx',
                region_name='xxxxx')

sessionMD = Session(aws_access_key_id='xxxxxxx',
                aws_secret_access_key='xxxxxxxxxxxx',
                region_name='xxxxx')

sessionVX = Session(aws_access_key_id='xxxxxx',
                aws_secret_access_key='xxxxxxxxxxx',
                region_name='xxxxx')

instancePSG ='xxxx'
instanceML = 'xxxx'
instanceMD ='xxxx'
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
def get_cpuUtilization():
	# Instance: PSG, Metric: CPUUtilization
	responsePSG_CPUUtilization = clientPSG.get_metric_statistics(
				 Namespace='AWS/EC2',
		                MetricName='CPUUtilization',
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
		                Unit='Percent'
		            )
	# print(responseML_CPUUtilization)
		
	if len(responsePSG_CPUUtilization)>0:
		if len(responsePSG_CPUUtilization['Datapoints'])>0:
			json_body=[
        			{
            				"measurement": "cpuUtilizationWithTags",
            				"tags": {
                				"Instance-ID": instancePSG
           		 		},
            				"time": responsePSG_CPUUtilization['Datapoints'][0]['Timestamp'],
            				"fields": {
                				"Instance-ID": instancePSG,
                				"Minimum":responsePSG_CPUUtilization['Datapoints'][0]['Minimum'],
                				"Unit":responsePSG_CPUUtilization['Datapoints'][0]['Unit'],
                				"Sum":responsePSG_CPUUtilization['Datapoints'][0]['Sum'],
                				"SampleCount":responsePSG_CPUUtilization['Datapoints'][0]['SampleCount'],
                				"Average":responsePSG_CPUUtilization['Datapoints'][0]['Average'],
                				"Maximum":responsePSG_CPUUtilization['Datapoints'][0]['Maximum']
            				}
        			}
    			]

			client.write_points(json_body)
		else:
			print("Datapoints is null.",instancePSG)
	else:
		print("Result is null.",instancePSG)


	responseML_CPUUtilization = clientML.get_metric_statistics(
				 Namespace='AWS/EC2',
		                MetricName='CPUUtilization',
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
		                Unit='Percent'
		            )
	# print(responseML_CPUUtilization)
		
	if len(responseML_CPUUtilization)>0:
		if len(responseML_CPUUtilization['Datapoints'])>0:
			json_body=[
        			{
            				"measurement": "cpuUtilizationWithTags",
            				"tags": {
                				"Instance-ID": instanceML
           		 		},
            				"time": responseML_CPUUtilization['Datapoints'][0]['Timestamp'],
            				"fields": {
                				"Instance-ID": instanceML,
                				"Minimum":responseML_CPUUtilization['Datapoints'][0]['Minimum'],
                				"Unit":responseML_CPUUtilization['Datapoints'][0]['Unit'],
                				"Sum":responseML_CPUUtilization['Datapoints'][0]['Sum'],
                				"SampleCount":responseML_CPUUtilization['Datapoints'][0]['SampleCount'],
                				"Average":responseML_CPUUtilization['Datapoints'][0]['Average'],
                				"Maximum":responseML_CPUUtilization['Datapoints'][0]['Maximum']
            				}
        			}
    			]

			client.write_points(json_body)
		else:
			print("Datapoints is null.",instanceML)
	else:
		print("Result is null.",instanceML)

	# responseMD_CPUUtilization = clientMD.get_metric_statistics(
	# 			 Namespace='AWS/EC2',
	# 	                MetricName='CPUUtilization',
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
	# 	                Unit='Percent'
	# 	            )
	# print(responseMD_CPUUtilization)
		
	# if len(responseMD_CPUUtilization)>0:
	# 	if len(responseMD_CPUUtilization['Datapoints'])>0:
	# 		json_body=[
 #        			{
 #            				"measurement": "cpuUtilizationWithTags",
 #            				"tags": {
 #                				"Instance-ID": instanceMD
 #           		 		},
 #            				"time": responseMD_CPUUtilization['Datapoints'][0]['Timestamp'],
 #            				"fields": {
 #                				"Instance-ID": instanceMD,
 #                				"Minimum":responseMD_CPUUtilization['Datapoints'][0]['Minimum'],
 #                				"Unit":responseMD_CPUUtilization['Datapoints'][0]['Unit'],
 #                				"Sum":responseMD_CPUUtilization['Datapoints'][0]['Sum'],
 #                				"SampleCount":responseMD_CPUUtilization['Datapoints'][0]['SampleCount'],
 #                				"Average":responseMD_CPUUtilization['Datapoints'][0]['Average'],
 #                				"Maximum":responseMD_CPUUtilization['Datapoints'][0]['Maximum']
 #            				}
 #        			}
 #    			]

	# 		client.write_points(json_body)
	# 	else:
	# 		print("Datapoints is null.",instanceMD)
	# else:
	# 	print("Result is null.",instanceMD)

	responseVX_CPUUtilization = clientVX.get_metric_statistics(
				 Namespace='AWS/EC2',
		                MetricName='CPUUtilization',
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
		                Unit='Percent'
		            )
	print(responseVX_CPUUtilization)
		
	if len(responseVX_CPUUtilization)>0:
		if len(responseVX_CPUUtilization['Datapoints'])>0:
			json_body=[
        			{
            				"measurement": "cpuUtilizationWithTags",
            				"tags": {
                				"Instance-ID": instanceVX
           		 		},
            				"time": responseVX_CPUUtilization['Datapoints'][0]['Timestamp'],
            				"fields": {
                				"Instance-ID": instanceVX,
                				"Minimum":responseVX_CPUUtilization['Datapoints'][0]['Minimum'],
                				"Unit":responseVX_CPUUtilization['Datapoints'][0]['Unit'],
                				"Sum":responseVX_CPUUtilization['Datapoints'][0]['Sum'],
                				"SampleCount":responseVX_CPUUtilization['Datapoints'][0]['SampleCount'],
                				"Average":responseVX_CPUUtilization['Datapoints'][0]['Average'],
                				"Maximum":responseVX_CPUUtilization['Datapoints'][0]['Maximum']
            				}
        			}
    			]

			client.write_points(json_body)
		else:
			print("Datapoints is null.",instanceVX)
	else:
		print("Result is null.",instanceVX)

if __name__ == '__main__':
    get_cpuUtilization()
