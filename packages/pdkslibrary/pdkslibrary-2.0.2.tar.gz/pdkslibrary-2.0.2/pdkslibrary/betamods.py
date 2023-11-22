from ast import Break
from itertools import count
import os
import re
import sys
import csv
import json
import time
import yaml
import wget
import boto3
import atexit
import shutil
import base64
import urllib3
import uniboost
import requests
import argparse
import botocore
import datetime
# import traceback
import subprocess
import boto.ec2.autoscale
# from boto.ec2.autoscale import AutoScaleConnection
# from boto.ec2.autoscale import ScalingPolicy
# conn = ScalingPolicy('<aws access key>', '<aws secret key>')
boto3.compat.filter_python_deprecation_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {'Content-type':'application/json'}

start_time = (datetime.datetime.now()).strftime("%I:%M:%S")

filesOGDir = uniboost.pwd()

def change_dir(cd_dir):
    os.chdir(cd_dir)

target_dir = '/opt/pfizer/etc/rancher-api'
this_target_dir = '/opt/pfizer/etc'
full_target_dir = '/opt/pfizer/etc/rancher-api/config_files/'

def resync_with_local_repo():
    target_dir = '/opt/pfizer/etc/rancher-api'
    change_dir(target_dir)
    
    proc_output = subprocess.Popen(["git", "fetch", "origin"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc_output.communicate()

    proc_output = subprocess.Popen(["git", "reset", "--hard", "origin/master"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc_output.communicate()

    proc_output = subprocess.Popen(["git", "clean", "-f", "-d"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc_output.communicate()

    # print('NOTE: Git resynced with local repo\n')

if('amraelp00007133' not in os.uname()[1]):
    resync_with_local_repo()

target_dir = '/opt/pfizer/etc/rancher-api'
this_target_dir = '/opt/pfizer/etc'
full_target_dir = '/opt/pfizer/etc/rancher-api/config_files/'

def git_sync_rancher_api(target_dir, this_target_dir):
    proc_output = subprocess.Popen(["chown", "root:amer", "prod"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc_output.communicate()
    proc_output = subprocess.Popen(["chmod", "775", "prod"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc_output.communicate()

    thisUser = 'mahah'
    if(os.path.exists(target_dir)):
        change_dir(target_dir)
        proc_output = subprocess.Popen(["git", "pull", "-n"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc_output.communicate()
    else:
        change_dir(this_target_dir)
        proc_output = subprocess.Popen(["git", "clone", "ssh://git@amrvlp000005282.pfizer.com:2222/secure/rancher-api.git"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc_output.communicate()

 # Git sync replaces wget using secure repo
if('amraelp00007133' not in os.uname()[1]):
    git_sync_rancher_api(target_dir, this_target_dir)

outputFilename = 'ecsAWSVariables_DEV'
outputFilename = 'ecsAWSVariables'

# change_dir(filesOGDir)

credentials_file_path = 'rancher2Variables.json'
credentials_file_path = full_target_dir + 'rancher2Variables'

if('amraelp00007133' not in os.uname()[1]):
    with open(credentials_file_path) as json_file:
        # print(str(json_file))
        rancher2Credentials_file = json.load(json_file)
        # print(uniboost.ppJSON(credentials_file)) 
else:
    proc_output = subprocess.Popen(["dzdo", "cat", credentials_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc_output.communicate()
    rancher2Credentials_file = json.loads(out)

aws_credentials_file_path = 'rancher2AWSVariables_DEV.json'
aws_credentials_file_path = full_target_dir + 'rancher2AWSVariables_DEV'

if('amraelp00007133' not in os.uname()[1]):
    with open(aws_credentials_file_path) as json_file:
        # print(str(json_file))
        aws_credentials_file = json.load(json_file)
        # print(uniboost.ppJSON(credentials_file))
        aws_credentials_file_data = aws_credentials_file
else:
    proc_output = subprocess.Popen(["dzdo", "cat", aws_credentials_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc_output.communicate()
    aws_credentials_file = json.loads(out)
    aws_credentials_file_data = aws_credentials_file

clusters_list = ['dhs-sts-nprod-tst11', 'dhs-sts-nprod-tst12', 'dhs-sts-nprod-tst13']
accounts = ['863380606983', '330470878083']

def base64Decoder(keySecret):
    coded_string = str(keySecret)
    try:
        keySecret = base64.b64decode(coded_string)
    except:
        pass

    return keySecret

def awsAPIConnection(aws_account):
    # print(aws_account)
    # print(type(aws_credentials_file_data[aws_account]['us-east-1']['key']))
    # print(aws_credentials_file_data[aws_account]['us-east-1']['key'])
    # print(base64Decoder(aws_credentials_file_data[aws_account]['us-east-1']['key']))
    # print(type(aws_credentials_file_data[aws_account]['us-east-1']['secret']))
    # print(aws_credentials_file_data[aws_account]['us-east-1']['secret'])
    # base64Decoder(aws_credentials_file_data[aws_account]['us-east-1']['secret'])

    this_key = base64Decoder(aws_credentials_file_data[aws_account]['us-east-1']['key']).strip()
    this_secret = base64Decoder(aws_credentials_file_data[aws_account]['us-east-1']['secret']).strip()

    key = this_key.decode("utf-8", errors="ignore")
    secret = this_secret.decode("utf-8", errors="ignore")

    # print(key)
    # print(secret)

    os.environ['AWS_ACCESS_KEY_ID'] = key
    os.environ['AWS_SECRET_ACCESS_KEY'] = secret
    os.environ['AWS_DEFAULT_OUTPUT'] = "json"
    os.environ['AWS_REGION'] = "us-east-1"
    os.environ['AWS_DEFAULT_REGION'] = "us-east-1"

    conn = boto.ec2.autoscale.connect_to_region(os.environ['AWS_REGION'],
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
    return conn

def describe_all_node_groups(clusters_list, aws_account='330470878083', credentials_file=aws_credentials_file):
    conn = awsAPIConnection(aws_account)

    client = boto3.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    # region = 'us-east-1'
    # regions.remove('eu-north-1')
   
    # if('amraelp00007133' not in os.uname()[1]):
    #     with open(credentials_file_path) as json_file:
    #         # print(str(json_file))
    #         rancher2Credentials_file = json.load(json_file)
    #         # print(uniboost.ppJSON(credentials_file)) 
    # else:
    #     # proc_output = subprocess.Popen(["dzdo", "cat", credentials_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #     # out, err = proc_output.communicate()
    #     # rancher2Credentials_file = json.loads(out)

    #     proc_output = subprocess.Popen(["dzdo", "cat", aws_credentials_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #     out, err = proc_output.communicate()
    #     # print(ppJSON(out))
    #     aws_credentials_file = json.loads(out)
    #     # print('Next')
    #     # print(ppJSON(aws_credentials_file))

    #     # out = json.loads(out)
    #     # # print(out)
    #     # print(out['hostname'])

    regionData = {}
    for region in regions:
        regionData.update( {region : []} )

    for region in regions:
        # print(region)
        try:
            eks = boto3.client(
                'eks',
                aws_access_key_id = base64Decoder(credentials_file[aws_account][region]['key']),
                aws_secret_access_key = base64Decoder(credentials_file[aws_account][region]['secret']),
                region_name=region
            )

            allResponses = []
            try:
                for cluster in clusters_list:
                    response = eks.list_nodegroups(
                        clusterName=cluster
                    )

                    allResponses.append([cluster, response])
                    # nodeGroups = response['nodegroups']
                    # print(nodeGroups)
            except:
                pass

            # eks = boto3.client('eks')
            # response = eks.list_nodegroups(
            #     clusterName=cluster_name
            # )

            # regionData.update( {region : []} )
                
            # print(len(allResponses))
            regionData[region].append(allResponses)
            # print(allResponses)
        except KeyError as e:
            # handle key errors you want
            if e.args[0] in regions:
                # print(e.args[0])
                # print('handled!')
                pass
            # reraise the exception if not handled
            else:
                raise
        
    return regionData

# for account in accounts:
#     # describe_all_node_groups(clusters_list, aws_account='330470878083', credentials_file=aws_credentials_file)
#     response = describe_all_node_groups(clusters_list, aws_account=account, credentials_file=aws_credentials_file)
#     print(uniboost.ppJSON(response))

# my_string = 'No cluster found for name: dhs-sts-nprod-tst11.'
# my_string = my_string.split("No cluster found for name: ",1)[1]
# my_string = my_string.split('.')
# this_failed_cluster = my_string[0]
# print(this_failed_cluster)

def get_all_node_group_info(cluster_name, node_group_name, aws_account='330470878083', credentials_file=aws_credentials_file):
    conn = awsAPIConnection(aws_account)

    client = boto3.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    # region = 'us-east-1'
    # regions.remove('eu-west-1')
   
    regionData = {}
    for region in regions:
        regionData.update( {region : []} )

    # print(regions)
    # for region in regions:
    #     print(region)

    try:
        for region in regions:
            if(region == 'us-east-1'):
                # print(region)
                # try:
                    eks = boto3.client(
                        'eks',
                        aws_access_key_id = base64Decoder(credentials_file[aws_account][region]['key']),
                        aws_secret_access_key = base64Decoder(credentials_file[aws_account][region]['secret']),
                        region_name=region
                    )

                    # print('debug')
                    # print(region)
                    # print(aws_account)
                    # print(cluster_name)
                    # print(node_group_name)
                    nodeGroupResponse = eks.describe_nodegroup(
                        clusterName=cluster_name,
                        nodegroupName=node_group_name
                    )
                    # print(nodeGroupResponse)
                # except KeyError as e:
                #     # handle key errors you want
                #     if e.args[0] in regions:
                #         # print(e.args[0])
                #         # print('handled!')
                #         pass
                #     # reraise the exception if not handled
                #     else:
                #         raise
    except Exception as e:
        print(e)
        # handle key errors you want
        if e.args[0] in regions:
            # print(e.args[0])
            # print('handled!')
            pass
        # reraise the exception if not handled
        else:
            raise

    return nodeGroupResponse

# helper to get name and version
def list_eks_cluster_description(cluster_name, aws_account='330470878083', credentials_file=aws_credentials_file):
    conn = awsAPIConnection(aws_account)

    client = boto3.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
   
    regionData = {}
    for region in regions:
        regionData.update( {region : []} )

    # print(regions)
    # for region in regions:
    #     print(region)

    # try:
    for region in regions:
        # if(region == 'ap-south-1'):
        if(region == 'us-east-1'):
        # print(region)
        # try:
            eks = boto3.client(
                'eks',
                aws_access_key_id = base64Decoder(credentials_file[aws_account][region]['key']),
                aws_secret_access_key = base64Decoder(credentials_file[aws_account][region]['secret']),
                region_name=region
            )

            cluster_list = []

            # response = eks.describe_cluster(
            #     name = cluster_name
            # )
            # # all descriptions are 2-tuples
            # print(response)
            # return (response['cluster']['name'],  response['cluster']['version'])
        
            # helper to get name and version
            def describe_cluster(cluster_name):
                response = eks.describe_cluster(
                    name = cluster_name
                )
                # all descriptions are 2-tuples
                return (response['cluster']['name'],  response['cluster']['version'])

            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks/client/list_clusters.html
            
            # handler for listing all clusters and getting descriptions
            if (cluster_name == 'all'):
                # returns only EKS clusters
                names = eks.list_clusters(
                )
                # indexing into output json
                for name in (names['clusters']):
                    cluster_list.append(describe_cluster(name))
            
            # if cluster name is specified, directly append description
            else:
                cluster_list.append(describe_cluster(cluster_name))
            
            # final return value
            return cluster_list
    # except:
    #     pass


# helper to get name and version
def raw_list_eks_native_cluster_description(cluster_name, aws_account='330470878083', credentials_file=aws_credentials_file):
    # print(uniboost.ppJSON(credentials_file))
    conn = awsAPIConnection(aws_account)

    client = boto3.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
   
    regionData = {}
    for region in regions:
        regionData.update( {region : []} )

    # print(regions)
    # for region in regions:
    #     print(region)
    # sys.exit()

    # try:
    for region in regions:
        # if(region == 'ap-south-1'):
        if(region == 'us-east-1'):
        # print(region)
        # try:
            eks = boto3.client(
                'eks',
                aws_access_key_id = base64Decoder(credentials_file[aws_account][region]['key']),
                aws_secret_access_key = base64Decoder(credentials_file[aws_account][region]['secret']),
                region_name=region
            )

            cluster_list = []

            # helper to get name and version
            def describe_cluster(cluster_name):
                response = eks.describe_cluster(
                    name = cluster_name
                )
                return response

            raw_response = describe_cluster(cluster_name)
            # print(raw_response)
            
            # final return value
            return raw_response
    # except:
    #     pass

def is_v1_or_v2_cluster(cluster_name, aws_account='330470878083', credentials_file=aws_credentials_file):
    conn = awsAPIConnection(aws_account)

    client = boto3.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
   
    regionData = {}
    for region in regions:
        regionData.update( {region : []} )

    for region in regions:
        try:
            eks = boto3.client(
                'eks',
                aws_access_key_id = base64Decoder(credentials_file[aws_account][region]['key']),
                aws_secret_access_key = base64Decoder(credentials_file[aws_account][region]['secret']),
                region_name=region
            )

            cluster_list = []

            def describeClusterEKS(cluster_name):
                response = eks.describe_cluster(
                    name = cluster_name
                )
                return response

            clusterTags = describeClusterEKS(cluster_name)['cluster']['tags']

            provisionTypeValue = ''
            for k, v in clusterTags.iteritems():
                if(k == 'ProvisionType'):
                    provisionTypeValue = v

            if(provisionTypeValue == 'PDCSv2'):
                provisionType = 'v2'
            elif(provisionTypeValue == 'PDCS'):
                provisionType = 'v1'

            if(provisionType is None):
                return 'undefined'
            else:
                return provisionType
        except Exception as e:
            # print(e)
            pass

def get_k8s_version(cluster_name, aws_account='330470878083', credentials_file=aws_credentials_file):
    conn = awsAPIConnection(aws_account)

    client = boto3.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
   
    regionData = {}
    for region in regions:
        regionData.update( {region : []} )

    for region in regions:
        try:
            eks = boto3.client(
                'eks',
                aws_access_key_id = base64Decoder(credentials_file[aws_account][region]['key']),
                aws_secret_access_key = base64Decoder(credentials_file[aws_account][region]['secret']),
                region_name=region
            )

            k8sVersion = eks.describe_cluster(name=cluster_name)['cluster']['version']
            print(k8sVersion)
            return k8sVersion
        except Exception as e:
            # print(e)
            pass
