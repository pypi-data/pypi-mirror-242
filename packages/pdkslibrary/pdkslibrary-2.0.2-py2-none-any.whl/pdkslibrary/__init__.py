#!/user/bin/env python3 
"""
pdkslibrary: This library is used for Rancher purposes.
Requirements: python2.7 or later.
"""

__author__ = "Michael Shobitan"
__copyright__ = "Copyright 2023, BTCS Platform Engineering"
__credits__ = ["Michael Shobitan"]
__license__ = "PFE"
__maintainer__ = "Michael Shobitan"
__email__ = "michael.shobitan@pfizer.com"
__status__ = "Production"

import os
import re
import sys
import csv
import wget
import json
import time
import boto3
import atexit
import shutil
import base64
import urllib3
import argparse
import requests
import subprocess
import boto.ec2.autoscale
boto3.compat.filter_python_deprecation_warnings()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {'Content-type':'application/json'}

default_aws_account = "330470878083"

def pwd():
    cwd = os.getcwd()
    return cwd

def change_dir(cd_dir):
    os.chdir(cd_dir)

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

# with open(credentials_file_path) as json_file:
#     # print(str(json_file))
#     rancher2Credentials_file = json.load(json_file)
#     # print(uniboost.ppJSON(credentials_file)) 

aws_credentials_file_path = 'rancher2AWSVariables_DEV.json'
aws_credentials_file_path = full_target_dir + 'rancher2AWSVariables_DEV'

if('amraelp00007133' not in os.uname()[1]):
    with open(aws_credentials_file_path) as json_file:
        # print(str(json_file))
        aws_credentials_file = json.load(json_file)
        # print(uniboost.ppJSON(credentials_file))
else:
    proc_output = subprocess.Popen(["dzdo", "cat", aws_credentials_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc_output.communicate()
    aws_credentials_file = json.loads(out)

outputFilePath = full_target_dir + outputFilename
if('amraelp00007133' not in os.uname()[1]):
    with open(outputFilePath) as json_file:
        data = json.load(json_file)
else:
    proc_output = subprocess.Popen(["dzdo", "cat", outputFilePath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc_output.communicate()
    data = json.loads(out)

def exampleFunc():
    """ 
    Summary line. 
  
    Extended description of function. 
  
    Parameters: 
    arg1 (int): Description of arg1 
  
    Returns: 
    int: Description of return value 
    """

    pass

def jsonPP(json_content):
    response = json.dumps(json_content, indent=4)
    return response

def ppJSON(json_content): # Works with more JSON outputs
    response = json.dumps(json_content, indent=4, sort_keys=True, default=str)
    return response

def latest():
    script = subprocess.Popen(["pip", "install", "uniboost", "-U"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    this_out, this_err = script.communicate()
    return this_out

def clusterInfo(url, key, secret):
    response = requests.get(url, auth=(key, secret), headers=headers, verify=False)
    binary = response.content
    output = json.loads(binary)

    return {'response': response, 'binary': binary, 'output': output}

def base64Decoder(keySecret):
    coded_string = str(keySecret)
    try:
        keySecret = base64.b64decode(coded_string)
    except:
        pass

    return keySecret

def get_env_creds(argument, credentials_file=rancher2Credentials_file):
    switch = credentials_file
    data = switch.get(argument, "ERROR: Invalid Environment!")

    env_url = data['env_url']
    key = base64Decoder(data['key'])
    secret = base64Decoder(data['secret'])

    return env_url, key, secret

def get_cluster_type(cluster):
    endpointList = (rancher2Credentials_file).keys()
    endpointList = list(endpointList)

    endpointsData = {}
    for endpoint in endpointList:
        values = get_env_creds(endpoint, rancher2Credentials_file)
        url = values[0] + "/clusters"
        key = base64Decoder(values[1])
        secret = base64Decoder(values[2].strip())

        response = requests.get(url, auth=(key, secret), headers=headers, verify=False)
        binary = response.content
        output = json.loads(binary)

        for counter in range(len(output['data'])):
            cluster_name = output['data'][counter]['name']  
            # print(endpoint + ': ' + cluster_name)
            endpointsData.update( {endpoint : []} )

    for endpoint in endpointList:
        values = get_env_creds(endpoint, rancher2Credentials_file)
        url = values[0] + "/clusters"
        key = base64Decoder(values[1])
        secret = base64Decoder(values[2].strip())

        response = requests.get(url, auth=(key, secret), headers=headers, verify=False)
        binary = response.content
        output = json.loads(binary)

        cluster_id = 'None'
        for counter in range(len(output['data'])):
            cluster_name = output['data'][counter]['name']   
            if(cluster == cluster_name):
                cluster_id = output['data'][counter]['id']   

                r2Endpoint = endpoint
                r2EndpointURL = url
                url = r2EndpointURL + '/' + cluster_id

                response = requests.get(url, auth=(key, secret), headers=headers, verify=False)
                binary = response.content
                apiEndpointOutput = json.loads(binary)

                try:
                    if('eks' in apiEndpointOutput['apiEndpoint']):
                        return 'eks'
                    else:
                        return 'custom'
                except:
                    return 'custom'

def get_cluster_ids():
    endpointList = (rancher2Credentials_file).keys()
    endpointList = list(endpointList)

    endpointsData = {}
    for endpoint in endpointList:
        endpointsData.update( {endpoint : []} )
        endpointsData[endpoint].append({'clusters': {}})

    for endpoint in endpointList:
        values = get_env_creds(endpoint, rancher2Credentials_file)
        url = values[0] + "/clusters"
        key = base64Decoder(values[1])
        secret = base64Decoder(values[2].strip())

        response = requests.get(url, auth=(key, secret), headers=headers, verify=False)
        binary = response.content
        output = json.loads(binary)

        for counter in range(len(output['data'])):
            cluster_name = output['data'][counter]['name']  
            cluster_id = output['data'][counter]['id']
            endpointsData[endpoint][0]['clusters'].update({cluster_name: cluster_id})

    return endpointsData

def get_rke_clusters():
    endpointList = (rancher2Credentials_file).keys()
    endpointList = list(endpointList)

    endpointsData = {}
    for endpoint in endpointList:
        values = get_env_creds(endpoint, rancher2Credentials_file)
        url = values[0] + "/clusters"
        key = base64Decoder(values[1])
        secret = base64Decoder(values[2].strip())

        response = requests.get(url, auth=(key, secret), headers=headers, verify=False)
        binary = response.content
        output = json.loads(binary)

        for counter in range(len(output['data'])):
            cluster_name = output['data'][counter]['name']  
            # print(endpoint + ': ' + cluster_name)
            endpointsData.update( {endpoint : []} )

    for endpoint in endpointList:
        values = get_env_creds(endpoint, rancher2Credentials_file)
        url = values[0] + "/clusters"
        key = base64Decoder(values[1])
        secret = base64Decoder(values[2].strip())

        response = requests.get(url, auth=(key, secret), headers=headers, verify=False)
        binary = response.content
        output = json.loads(binary)

        for counter in range(len(output['data'])):
            cluster_name = output['data'][counter]['name']  
            # print(endpoint + ': ' + cluster_name)
            endpointsData[endpoint].append(cluster_name)

    return endpointsData

def get_cluster_endpoint(cluster):
    endpointList = (rancher2Credentials_file).keys()
    endpointList = list(endpointList)

    endpointsData = {}
    for endpoint in endpointList:
        values = get_env_creds(endpoint, rancher2Credentials_file)
        url = values[0] + "/clusters"
        key = base64Decoder(values[1])
        secret = base64Decoder(values[2].strip())

        response = requests.get(url, auth=(key, secret), headers=headers, verify=False)
        binary = response.content
        output = json.loads(binary)

        for counter in range(len(output['data'])):
            cluster_name = output['data'][counter]['name']  
            # print(endpoint + ': ' + cluster_name)
            endpointsData.update( {endpoint : []} )

    for endpoint in endpointList:
        values = get_env_creds(endpoint, rancher2Credentials_file)
        url = values[0] + "/clusters"
        key = base64Decoder(values[1])
        secret = base64Decoder(values[2].strip())

        response = requests.get(url, auth=(key, secret), headers=headers, verify=False)
        binary = response.content
        output = json.loads(binary)

        for counter in range(len(output['data'])):
            cluster_name = output['data'][counter]['name']  
            # print(endpoint + ': ' + cluster_name)
            endpointsData[endpoint].append(cluster_name)

    for endpoint in endpointsData.keys():
        if(cluster in endpointsData[endpoint]):
            return endpoint
    
def set_env_var(var_name, var_value):
    os.environ[var_name] = var_value
    
def get_env_var(var_name):
    path = os.environ[var_name]
    return path

def file_to_json(json_file):
    with open(json_file, 'r') as handle:
        parsed = json.load(handle)
    return parsed

def jsonPP(json_content):
    response = json.dumps(json_content, indent=4)
    return response

def ppJSON(json_content): # Works with more JSON outputs
    response = json.dumps(json_content, indent=4, sort_keys=True, default=str)
    return response

def cd(cd_dir):
    os.chdir(cd_dir)

def file_exist(this_file):
    status = os.path.exists(this_file)
    if(status == True):
        if(os.path.isdir(this_file)):
            file_type = 'directory'
            # print(file_type)
        elif(os.path.isfile(this_file)):  
            file_type = 'file'
            # print(file_type)
        else:
            print("It is a special file (socket, FIFO, device file, etc.)" )
        status = 'exist'
    else:
        file_type = status
        status = status

    return {'file_type': file_type, 'status': status}

def delete_folder(folder_name):
    try:
        os.rmdir(folder_name)
    except OSError:
        print ("NOTE: Deletion of the directory %s failed" % folder_name + "\n")
    else:
        print ("NOTE: Successfully deleted the directory %s" % folder_name)

def awsAPIConnection(aws_account):
    # print(aws_account)
    os.environ['AWS_ACCESS_KEY_ID'] = base64Decoder(data[aws_account]['us-east-1']['key'])
    os.environ['AWS_SECRET_ACCESS_KEY'] = base64Decoder(data[aws_account]['us-east-1']['secret'])
    os.environ['AWS_DEFAULT_OUTPUT'] = "json"
    os.environ['AWS_REGION'] = "us-east-1"
    os.environ['AWS_DEFAULT_REGION'] = "us-east-1"

    conn = boto.ec2.autoscale.connect_to_region(os.environ['AWS_REGION'],
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
    return conn

def awsAPIConnectionOld():
    conn = boto.ec2.autoscale.connect_to_region(get_env_var('AWS_REGION'),
    aws_access_key_id=get_env_var('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=get_env_var('AWS_SECRET_ACCESS_KEY'))
    return conn

# def eks():
#     eks = boto3.client('eks')
#     return eks

def describe_cluster(eks, cluster):
    response = eks.describe_cluster(
        name=cluster
    )
    return response

# def cloudformation():
#     cloudformation = boto3.client('cloudformation')
#     return cloudformation

def describe_stack(cloudformation, cluster):
    stack_name = "%s-eks-worker-nodes" % (cluster)
    response = cloudformation.describe_stacks(
        StackName=stack_name,
    )
    return response

def list_all_users():
    aws_accounts = ['330470878083', '863380606983']
    for aws_current_account in aws_accounts:

        client = boto3.client(
            'iam',
            aws_access_key_id = base64Decoder(data[aws_current_account]['us-east-1']['key']),
            aws_secret_access_key = base64Decoder(data[aws_current_account]['us-east-1']['secret'])

            # os.environ['AWS_ACCESS_KEY_ID'] = base64Decoder(data[aws_account]['us-east-1']['key'])
            # os.environ['AWS_SECRET_ACCESS_KEY'] = base64Decoder(data[aws_account]['us-east-1']['secret'])
        )

        users = client.list_users()
        print(ppJSON(users))

def is_v1_or_v2_cluster(cluster, aws_account='330470878083', credentials_file=aws_credentials_file):
    conn = awsAPIConnection(aws_account)

    client = boto3.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    # region = 'us-east-1'
    # regions.remove('eu-north-1')
   
    regionData = {}
    for region in regions:
        regionData.update( {region : []} )

    provisionType = None
    for region in regions:
        try:
            eks = boto3.client(
                'eks',
                aws_access_key_id = base64Decoder(credentials_file[aws_account][region]['key']),
                aws_secret_access_key = base64Decoder(credentials_file[aws_account][region]['secret']),
                region_name=region
            )

            try:
                def describeClusterEKS():
                    response = eks.describe_cluster(name=cluster)
                    
                    return response

                clusterTags = describeClusterEKS()['cluster']['tags']

                provisionTypeValue = ''
                for k, v in clusterTags.iteritems():
                    # print('Tag: ' + k + ' | | Value: ' + v)
                    if(k == 'ProvisionType'):
                        # print('Tag: ' + k + ' | | Value: ' + v)
                        provisionTypeValue = v
                # print(provisionTypeValue)

                if(provisionTypeValue == 'PDCSv2'):
                    provisionType = 'v2'
                elif(provisionTypeValue == 'PDCS'):
                    provisionType = 'v1'
            except Exception as e:
                if('No cluster found for name' in e):
                    pass
        except KeyError as e:
            # handle key errors you want
            if e.args[0] in regions:
                # print(e.args[0])
                # print('handled!')
                pass
            # reraise the exception if not handled
            else:
                raise

    if(provisionType is None):
        return 'undefined'
    else:
        return provisionType

def get_all_arns(aws_account='330470878083', credentials_file=aws_credentials_file):
    conn = awsAPIConnection(aws_account)

    client = boto3.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    # region = 'us-east-1'
    # regions.remove('eu-north-1')
   
    regionData = {}
    for region in regions:
        regionData.update( {region : []} )

    for region in regions:
        try:
            ecs = boto3.client(
                'ecs',
                aws_access_key_id = base64Decoder(credentials_file[aws_account][region]['key']),
                aws_secret_access_key = base64Decoder(credentials_file[aws_account][region]['secret']),
                region_name=region
            )

            ecsclusterArnList = []
            try:
                response = ecs.list_clusters()
                for counter in range(len(response['clusterArns'])):
                    ca = response['clusterArns'][counter]
                    ecsclusterArnList.append(ca)
            except Exception as e:
                if('AccessDeniedException' in e.args[0]):
                    print('ERROR: Not able to retrieve ARNs from ' + region + ' due to IAM policy non-athorization!')

            regionData[region].append(ecsclusterArnList)
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

def get_all_node_group_info(cluster_name, node_group_name, aws_account='330470878083', credentials_file=aws_credentials_file):
    conn = awsAPIConnection(aws_account)

    client = boto3.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    # region = 'us-east-1'
    # regions.remove('eu-north-1')
   
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

            nodeGroupResponse = eks.describe_nodegroup(
                clusterName=cluster_name,
                nodegroupName=node_group_name
            )
        except KeyError as e:
            # handle key errors you want
            if e.args[0] in regions:
                # print(e.args[0])
                # print('handled!')
                pass
            # reraise the exception if not handled
            else:
                raise

    return nodeGroupResponse

def describe_all_node_groups(clusters_list, aws_account='330470878083', credentials_file=aws_credentials_file):
    conn = awsAPIConnection(aws_account)

    client = boto3.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    # region = 'us-east-1'
    # regions.remove('eu-north-1')
   
    if('amraelp00007133' not in os.uname()[1]):
        with open(aws_credentials_file_path) as json_file:
            # print(str(json_file))
            aws_credentials_file = json.load(json_file)
            # print(uniboost.ppJSON(credentials_file)) 
    else:
        # proc_output = subprocess.Popen(["dzdo", "cat", credentials_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # out, err = proc_output.communicate()
        # rancher2Credentials_file = json.loads(out)

        proc_output = subprocess.Popen(["dzdo", "cat", aws_credentials_file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc_output.communicate()
        # print(ppJSON(out))
        aws_credentials_file = json.loads(out)
        # print('Next')
        # print(ppJSON(aws_credentials_file))

        # out = json.loads(out)
        # # print(out)
        # print(out['hostname'])

    regionData = {}
    for region in regions:
        regionData.update( {region : []} )

    for region in regions:
        try:
            # print(region)
            # print(base64Decoder(aws_credentials_file[aws_account][region]['key']))
            # print(base64Decoder(aws_credentials_file[aws_account][region]['secret']))
            eks = boto3.client(
                'eks',
                aws_access_key_id = base64Decoder(aws_credentials_file[aws_account][region]['key']),
                aws_secret_access_key = base64Decoder(aws_credentials_file[aws_account][region]['secret']),
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

    # print(ppJSON(regionData))
    return regionData

# def describe_all_stacks(region_name, aws_account='330470878083', credentials_file=aws_credentials_file):
def describe_all_stacks(aws_account='330470878083', credentials_file=aws_credentials_file):
    # switch = credentials_file
    # print(ppJSON(credentials_file))
    # data = switch.get(aws_account, "ERROR: Invalid Environment!")
    
    # print(base64Decoder(credentials_file[aws_account]['us-east-1']['key']))
    # print(base64Decoder(credentials_file[aws_account]['us-east-1']['secret']))

    # print(aws_account)
    conn = awsAPIConnection(aws_account)

    # ['eu-north-1', 'ap-south-1', 'eu-west-3', 'eu-west-2', 'eu-west-1', 'ap-northeast-3', 'ap-northeast-2', 'ap-northeast-1', 'sa-east-1', 'ca-central-1', 'ap-southeast-1', 'ap-southeast-2', 'eu-central-1', 'us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']

    client = boto3.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    regions.remove('eu-north-1')
    # print(regions)
    
    # client = boto3.client(
    #     'cloudformation',
    #     aws_access_key_id = base64Decoder(data[aws_account]['us-east-1']['key']),
    #     aws_secret_access_key = base64Decoder(data[aws_account]['us-east-1']['secret']),
    #     region_name=thisRegionName
    # )

    regionData = {}
    # ec2 = boto3.client('ec2')

    # ec2 = boto3.client(
    #     'ec2',
    #     aws_access_key_id = base64Decoder(credentials_file[aws_account]['us-east-1']['key']),
    #     aws_secret_access_key = base64Decoder(credentials_file[aws_account]['us-east-1']['secret'])
    # )
    # print(ec2)

    # # region_name = 'us-east-1'

    # aws_access_key_id = base64Decoder(credentials_file[aws_account]['us-east-1']['key'])
    # aws_secret_access_key = base64Decoder(credentials_file[aws_account]['us-east-1']['secret'])
    # ec2 = boto3.resource('ec2', region_name=region_name, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    
    # ec2 = boto3.resource('ec2', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
    # print(regions)

    # regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    
    # try:
    #     a['a']
    # except KeyError as e:
    #     # handle key errors you want
    #     if e.args[0] == 'a':
    #         pass
    #     # reraise the exception if not handled
    #     else:
    #         raise
    
    for region in regions: # Useful, uncomment if reverting
        try:
            # print(region)
        # if(region_name == region_name):
            # thisRegionName = region['RegionName'] # Useful, uncomment if reverting
            thisRegionName = region # Delete if reverting
            # print(thisRegionName)
            # cloudformation = boto3.client('cloudformation', region_name=thisRegionName)

            cloudformation = boto3.client(
                'cloudformation',
                aws_access_key_id = base64Decoder(credentials_file[aws_account][thisRegionName]['key']),
                aws_secret_access_key = base64Decoder(credentials_file[aws_account][thisRegionName]['secret']),
                region_name=thisRegionName
            )

            regionData.update( {thisRegionName : []} )
            
            response = cloudformation.describe_stacks()
            allResponses = [response]

            if('NextToken' in response.keys()):
                hasNextToken = True
                thisCount = 1
                while hasNextToken == True:
                    response = cloudformation.describe_stacks(NextToken=response['NextToken'])
                    if('NextToken' in response.keys()):
                        num2words = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', \
                        6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', \
                        11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen', \
                        15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen', \
                        19: 'Nineteen', 20: 'Twenty', 30: 'Thirty', 40: 'Forty', \
                        50: 'Fifty', 60: 'Sixty', 70: 'Seventy', 80: 'Eighty', \
                        90: 'Ninety', 0: 'Zero'}
                        
                        def n2w(n):
                            try:
                                varName = num2words[n]
                            except KeyError:
                                try:
                                    print(num2words[n-n%10] + num2words[n%10].lower())
                                except KeyError:
                                    print('Number out of range')
                            
                            return varName

                        varName = n2w(thisCount)

                        my_data = {}
                        foo = varName
                        my_data[foo] = response
                        assert my_data[varName] == response

                        thisCount += 1
                        allResponses.append(my_data[varName])
                    else:
                        allResponses.append(response)
                        hasNextToken = False
                        if hasNextToken == False:
                            break

            # print(len(allResponses))
            regionData[thisRegionName].append(allResponses)
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

    # print(ppJSON(regionData))
    return regionData

def get_cf_stacks(cluster, aws_account='330470878083'):
    # print('debugging')
    conn = awsAPIConnection(aws_account)
    # print(conn)
    
    regionData = {}
    ec2 = boto3.client('ec2')
    # regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    for region in ec2.describe_regions()['Regions']:
        thisRegionName = region['RegionName']
        eks = boto3.client('eks', region_name=thisRegionName)
        for thisCluster in eks.list_clusters()['clusters']: # If region has at least one cluster
            # print(thisRegionName + ': ' + thisCluster)
            regionData.update( {thisRegionName : []} )

    for region in ec2.describe_regions()['Regions']:
        thisRegionName = region['RegionName']
        eks = boto3.client('eks', region_name=thisRegionName)
        for thisCluster in eks.list_clusters()['clusters']:
            regionData[thisRegionName].append(thisCluster)

    for region in regionData.keys():
        if(cluster in regionData[region]):
            cloudformation = boto3.client('cloudformation', region_name=region)
    
    try:
        response = cloudformation.describe_stacks()
    except UnboundLocalError:
        print('AWSAccountError: cluster not in specified account')
        sys.exit()
        # return 'AWSAccountError: aws account not specified'

    try:
        responseMore = cloudformation.describe_stacks(NextToken=response['NextToken'])
        allResponses = [response, responseMore]
    except:
        allResponses = [response]

    clusterStackNames = []
    stacksINFO = []
    def aggregateAllStackInfo(response):
        if(sys.version_info > (3, 0)):
            for counter in range(len(response['Stacks'])): # Python3.6
                stackName = response['Stacks'][counter]['StackName']
                if(cluster in stackName):
                    clusterStackNames.append(stackName)
                    # print(response['Stacks'][counter])
                    stacksINFO.append(response['Stacks'][counter])
                    # print(json.dumps(response['Stacks'][counter], indent=4, sort_keys=True, default=str))
        else:
            for counter in xrange(len(response['Stacks'])): # Python2.7
                stackName = response['Stacks'][counter]['StackName']
                if(cluster in stackName):
                    clusterStackNames.append(stackName)
                    # print(response['Stacks'][counter])
                    stacksINFO.append(response['Stacks'][counter])
                    # print(json.dumps(response['Stacks'][counter], indent=4, sort_keys=True, default=str))

        return clusterStackNames, stacksINFO

    for thisResponse in allResponses:
        allStackData = aggregateAllStackInfo(thisResponse)
    
    clusterStackNames.append(allStackData[0])
    stacksINFO.append(allStackData[1])
    
    actualStacksList = []
    if type(clusterStackNames) is list:
        for item in clusterStackNames:
            if type(item) is not list:
                actualStacksList.append(item)

    # if(len(clusterStackNames > 0)):
    if(actualStacksList):
        # return {'clusterStackNames': actualStacksList, 'stacksINFO': stacksINFO}
        return actualStacksList
        
    response = cloudformation.describe_stacks()
    responseMore = cloudformation.describe_stacks(NextToken=response['NextToken'])
    allResponses = [response, responseMore]

    clusterStackNames = []
    stacksINFO = []
    def aggregateAllStackInfo(response):
        clusterStackNames = []
        stacksINFO = []
        if(sys.version_info > (3, 0)):
            for counter in range(len(response['Stacks'])): # Python3.6
                stackName = response['Stacks'][counter]['StackName']
                if(cluster in stackName):
                    clusterStackNames.append(stackName)
                    # print(response['Stacks'][counter])
                    stacksINFO.append(response['Stacks'][counter])
                    # print(json.dumps(response['Stacks'][counter], indent=4, sort_keys=True, default=str))
        else:
            for counter in xrange(len(response['Stacks'])): # Python2.7
                stackName = response['Stacks'][counter]['StackName']
                if(cluster in stackName):
                    clusterStackNames.append(stackName)
                    # print(response['Stacks'][counter])
                    stacksINFO.append(response['Stacks'][counter])
                    # print(json.dumps(response['Stacks'][counter], indent=4, sort_keys=True, default=str))

        # print(clusterStackNames)
        return clusterStackNames, stacksINFO

    for thisResponse in allResponses:
        allStackData = aggregateAllStackInfo(thisResponse)
        # print(allStackData)
        clusterStackNames.append(allStackData[0])
        stacksINFO.append(allStackData[1])

    clusterStackNames = [x for x in clusterStackNames if x != []]
    clusterStackNamesCleaned = []
    for stack in clusterStackNames:
        stack = stack[0]
        # print(stack)
        clusterStackNamesCleaned.append(stack)
    # print(clusterStackNamesCleaned)

    actualStacksList = []
    if type(clusterStackNamesCleaned) is list:
        for item in clusterStackNamesCleaned:
            if type(item) is not list:
                actualStacksList.append(item)

    stacksINFO = [x for x in stacksINFO if x != []]
    stacksINFOCleaned = []
    for stack in stacksINFO:
        stack = stack[0]
        # print(stack)
        stacksINFOCleaned.append(stack)
    # print(stacksINFOCleaned)
    
    # return {'clusterStackNames': actualStacksList, 'stacksINFO': stacksINFOCleaned}
    return actualStacksList

key = None
def get_cf_stack_params(cluster, stack_name, aws_account='330470878083', key=key):
    conn = awsAPIConnection(aws_account)

    regionData = {}
    ec2 = boto3.client('ec2')
    # regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    for region in ec2.describe_regions()['Regions']:
        # print(region)
        thisRegionName = region['RegionName']
        eks = boto3.client('eks', region_name=thisRegionName)
        for thisCluster in eks.list_clusters()['clusters']: # If region has at least one cluster
            # print(thisRegionName + ': ' + thisCluster)
            regionData.update( {thisRegionName : []} )

    for region in ec2.describe_regions()['Regions']:
        thisRegionName = region['RegionName']
        eks = boto3.client('eks', region_name=thisRegionName)
        for thisCluster in eks.list_clusters()['clusters']:
            regionData[thisRegionName].append(thisCluster)

    for region in regionData.keys():
        if(cluster in regionData[region]):
            try:
                cloudformation = boto3.client('cloudformation', region_name=region)
            except:
                cloudformation = boto3.client('cloudformation')

    try:
        response = cloudformation.describe_stacks()
    except UnboundLocalError:
        print('AWSAccountError: cluster not in specified account')
        sys.exit()
        # return 'AWSAccountError: aws account not specified'
        
    try:
        responseMore = cloudformation.describe_stacks(NextToken=response['NextToken'])
        allResponses = [response, responseMore]
    except:
        allResponses = [response]

    clusterStackNames = []
    stacksINFO = []
    def aggregateAllStackInfo(response):
        if(sys.version_info > (3, 0)):
            for counter in range(len(response['Stacks'])): # Python3.6
                stackName = response['Stacks'][counter]['StackName']
                if(stack_name == stackName):
                    clusterStackNames.append(stackName)
                    # print(response['Stacks'][counter])
                    stacksINFO.append(response['Stacks'][counter])
                    # print(json.dumps(response['Stacks'][counter], indent=4, sort_keys=True, default=str))
        else:
            for counter in xrange(len(response['Stacks'])): # Python2.7
                stackName = response['Stacks'][counter]['StackName']
                if(stack_name == stackName):
                    clusterStackNames.append(stackName)
                    # print(response['Stacks'][counter])
                    stacksINFO.append(response['Stacks'][counter])
                    # print(json.dumps(response['Stacks'][counter], indent=4, sort_keys=True, default=str))

        return clusterStackNames, stacksINFO

    for thisResponse in allResponses:
        allStackData = aggregateAllStackInfo(thisResponse)

    clusterStackNames.append(allStackData[0])
    stacksINFO.append(allStackData[1])
    
    actualStacksList = []
    if type(clusterStackNames) is list:
        for item in clusterStackNames:
            if type(item) is not list:
                actualStacksList.append(item)

    # if(len(clusterStackNames > 0)):
    if(actualStacksList):
        # return {'clusterStackNames': actualStacksList, 'stacksINFO': stacksINFO}
        for instance in xrange(len(stacksINFO)):
            stacksINFO = stacksINFO[0]['Parameters']

            if(key is not None):
                specificData = {}
                for instance in xrange(len(stacksINFO)):
                    parameterKey = stacksINFO[instance]['ParameterKey']
                    if(parameterKey == key):
                        specificData.update( {'ParameterKey' : stacksINFO[instance]['ParameterKey']} )
                        specificData.update( {'ParameterValue' : stacksINFO[instance]['ParameterValue']} )
                stacksINFO = [specificData]

                return stacksINFO
            else:
                return stacksINFO

    response = cloudformation.describe_stacks()
    allResponses = [response]

    if('NextToken' in response.keys()):
        hasNextToken = True
        thisCount = 1
        while hasNextToken == True:
            response = cloudformation.describe_stacks(NextToken=response['NextToken'])
            if('NextToken' in response.keys()):
                num2words = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', \
                6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', \
                11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen', \
                15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen', \
                19: 'Nineteen', 20: 'Twenty', 30: 'Thirty', 40: 'Forty', \
                50: 'Fifty', 60: 'Sixty', 70: 'Seventy', 80: 'Eighty', \
                90: 'Ninety', 0: 'Zero'}
                
                def n2w(n):
                    try:
                        varName = num2words[n]
                    except KeyError:
                        try:
                            print(num2words[n-n%10] + num2words[n%10].lower())
                        except KeyError:
                            print('Number out of range')
                    
                    return varName

                varName = n2w(thisCount)

                my_data = {}
                foo = varName
                my_data[foo] = response
                assert my_data[varName] == response

                thisCount += 1
                allResponses.append(my_data[varName])
            else:
                allResponses.append(response)
                hasNextToken = False
                if hasNextToken == False:
                    break

    # responseMore = cloudformation.describe_stacks(NextToken=response['NextToken'])
    # allResponses = [response, responseMore]

    clusterStackNames = []
    stacksINFO = []
    def aggregateAllStackInfo(response):
        clusterStackNames = []
        stacksINFO = []
        if(sys.version_info > (3, 0)):
            for counter in range(len(response['Stacks'])): # Python3.6
                stackName = response['Stacks'][counter]['StackName']
                if(stack_name == stackName):
                    clusterStackNames.append(stackName)
                    # print(response['Stacks'][counter])
                    stacksINFO.append(response['Stacks'][counter])
                    # print(json.dumps(response['Stacks'][counter], indent=4, sort_keys=True, default=str))
        else:
            for counter in xrange(len(response['Stacks'])): # Python2.7
                stackName = response['Stacks'][counter]['StackName']
                if(stack_name == stackName):
                    clusterStackNames.append(stackName)
                    # print(response['Stacks'][counter])
                    stacksINFO.append(response['Stacks'][counter])
                    # print(json.dumps(response['Stacks'][counter], indent=4, sort_keys=True, default=str))

        # print(clusterStackNames)
        return clusterStackNames, stacksINFO

    for thisResponse in allResponses:
        allStackData = aggregateAllStackInfo(thisResponse)
        # print(allStackData)
        clusterStackNames.append(allStackData[0])
        stacksINFO.append(allStackData[1])

    clusterStackNames = [x for x in clusterStackNames if x != []]
    clusterStackNamesCleaned = []
    for stack in clusterStackNames:
        stack = stack[0]
        # print(stack)
        clusterStackNamesCleaned.append(stack)
    # print(clusterStackNamesCleaned)

    actualStacksList = []
    if type(clusterStackNamesCleaned) is list:
        for item in clusterStackNamesCleaned:
            if type(item) is not list:
                actualStacksList.append(item)

    stacksINFO = [x for x in stacksINFO if x != []]
    stacksINFOCleaned = []
    for stack in stacksINFO:
        stack = stack[0]
        # print(stack)
        stacksINFOCleaned.append(stack)
    # print(stacksINFOCleaned)
    
    # return {'clusterStackNames': actualStacksList, 'stacksINFO': stacksINFOCleaned}
    # return stacksINFOCleaned
    for instance in xrange(len(stacksINFOCleaned)):
        return stacksINFOCleaned
        stacksINFO = stacksINFOCleaned[0]['Parameters']

        if(key is not None):
            specificData = {}
            for instance in xrange(len(stacksINFO)):
                parameterKey = stacksINFO[instance]['ParameterKey']
                if(parameterKey == key):
                    specificData.update( {'ParameterKey' : stacksINFO[instance]['ParameterKey']} )
                    specificData.update( {'ParameterValue' : stacksINFO[instance]['ParameterValue']} )
            stacksINFO = [specificData]

            return stacksINFO
        else:
            return stacksINFO

def get_eks_clusters(aws_account='330470878083', credentials_file=aws_credentials_file):
    conn = awsAPIConnection(aws_account)

    # regionData = {}
    # ec2 = boto3.client('ec2')
    # # regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    # for region in ec2.describe_regions()['Regions']:
    #     thisRegionName = region['RegionName']
    #     eks = boto3.client('eks', region_name=thisRegionName)
    #     for thisCluster in eks.list_clusters()['clusters']: # If region has at least one cluster
    #         # print(thisRegionName + ': ' + thisCluster)
    #         regionData.update( {thisRegionName : []} )

    # for region in ec2.describe_regions()['Regions']:
    #     thisRegionName = region['RegionName']
    #     eks = boto3.client('eks', region_name=thisRegionName)
    #     for thisCluster in eks.list_clusters()['clusters']:
    #         regionData[thisRegionName].append(thisCluster)

    # return regionData

    # conn = awsAPIConnection(aws_account)

    client = boto3.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    # region = 'us-east-1'
    # regions.remove('eu-north-1')
   
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

            # for thisCluster in eks.list_clusters()['clusters']: # If region has at least one cluster
            #     # print(thisRegionName + ': ' + thisCluster)
            #     regionData.update( {thisRegionName : []} )

            for thisCluster in eks.list_clusters()['clusters']:
                regionData[region].append(thisCluster)

            # allResponses = []
            # for cluster in clusters_list:
            #     response = eks.list_nodegroups(
            #         clusterName=cluster
            #     )

            #     allResponses.append([cluster, response])
            #     # nodeGroups = response['nodegroups']
            #     # print(nodeGroups)

            # # eks = boto3.client('eks')
            # # response = eks.list_nodegroups(
            # #     clusterName=cluster_name
            # # )

            # # regionData.update( {region : []} )
                
            # # print(len(allResponses))
            # regionData[region].append(allResponses)
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

    # print(ppJSON(regionData))
    return regionData

def get_eks_cluster_region(cluster, aws_account='330470878083'):
    conn = awsAPIConnection(aws_account)

    regionData = {}
    ec2 = boto3.client('ec2')
    # regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    for region in ec2.describe_regions()['Regions']:
        thisRegionName = region['RegionName']
        eks = boto3.client('eks', region_name=thisRegionName)
        for thisCluster in eks.list_clusters()['clusters']: # If region has at least one cluster
            # print(thisRegionName + ': ' + thisCluster)
            regionData.update( {thisRegionName : []} )

    for region in ec2.describe_regions()['Regions']:
        thisRegionName = region['RegionName']
        eks = boto3.client('eks', region_name=thisRegionName)
        for thisCluster in eks.list_clusters()['clusters']:
            regionData[thisRegionName].append(thisCluster)

    for region in regionData.keys():
        if(cluster in regionData[region]):
            if(region is None):
                print('AWSAccountError: cluster not in specified account')
                sys.exit()
                # return 'AWSAccountError: aws account not specified'
            else:
                return region

def get_all_cf_node_info(aws_region, stack_name, aws_account='330470878083'):
    conn = awsAPIConnection(aws_account)

    ec2 = boto3.client('ec2')
    # regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    # for region in ec2.describe_regions()['Regions']:
        # if(region['RegionName'] == aws_region):
            # thisRegionName = region['RegionName']
    thisRegionName = aws_region
    cloudformation = boto3.client('cloudformation', region_name=thisRegionName)
    
    response = cloudformation.list_stack_resources(
        StackName=stack_name,
    )

    return response

def get_all_cf_info(aws_account='330470878083'):
    conn = awsAPIConnection(aws_account)

    regionData = {}
    ec2 = boto3.client('ec2')
    # regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    for region in ec2.describe_regions()['Regions']:
        thisRegionName = region['RegionName']
        # print(thisRegionName)
        cloudformation = boto3.client('cloudformation', region_name=thisRegionName)
        regionData.update( {thisRegionName : []} )
        
        response = cloudformation.list_stacks()
        allResponses = [response]

        if('NextToken' in response.keys()):
            hasNextToken = True
            thisCount = 1
            while hasNextToken == True:
                response = cloudformation.list_stacks(NextToken=response['NextToken'])
                if('NextToken' in response.keys()):
                    num2words = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', \
                    6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', \
                    11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen', \
                    15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen', \
                    19: 'Nineteen', 20: 'Twenty', 30: 'Thirty', 40: 'Forty', \
                    50: 'Fifty', 60: 'Sixty', 70: 'Seventy', 80: 'Eighty', \
                    90: 'Ninety', 0: 'Zero'}
                    
                    def n2w(n):
                        try:
                            varName = num2words[n]
                        except KeyError:
                            try:
                                print(num2words[n-n%10] + num2words[n%10].lower())
                            except KeyError:
                                print('Number out of range')
                        
                        return varName

                    varName = n2w(thisCount)

                    my_data = {}
                    foo = varName
                    my_data[foo] = response
                    assert my_data[varName] == response

                    thisCount += 1
                    allResponses.append(my_data[varName])
                else:
                    allResponses.append(response)
                    hasNextToken = False
                    if hasNextToken == False:
                        break

        # print(len(allResponses))
        regionData[thisRegionName].append(allResponses)
        # print(allResponses)

    # print(ppJSON(regionData))
    return regionData
    # return allRegionResponses

    # for thisResponse in allResponses:
    #     allStackData = aggregateAllStackInfo(thisResponse)
    #     # print(allStackData)
    #     clusterStackNames.append(allStackData[0])
    #     stacksINFO.append(allStackData[1])

    # regionData = {}
    # ec2 = boto3.client('ec2')
    # # regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    # for region in ec2.describe_regions()['Regions']:
    #     # print(region)
    #     thisRegionName = region['RegionName']
    #     eks = boto3.client('eks', region_name=thisRegionName)
    #     for thisCluster in eks.list_clusters()['clusters']: # If region has at least one cluster
    #         # print(thisRegionName + ': ' + thisCluster)
    #         regionData.update( {thisRegionName : []} )

    # for region in ec2.describe_regions()['Regions']:
    #     thisRegionName = region['RegionName']
    #     eks = boto3.client('eks', region_name=thisRegionName)
    #     for thisCluster in eks.list_clusters()['clusters']:
    #         regionData[thisRegionName].append(thisCluster)

    # for region in regionData.keys():
    #     if(cluster in regionData[region]):
    #         try:
    #             cloudformation = boto3.client('cloudformation', region_name=region)
    #         except:
    #             cloudformation = boto3.client('cloudformation')

def cahc(cluster):
    eks = eks()
    clusterINFO = describe_cluster(eks, cluster)
    # Enabled
    privateAccess = clusterINFO['cluster']['resourcesVpcConfig']['endpointPrivateAccess']
    # Disabled
    publicAccess = clusterINFO['cluster']['resourcesVpcConfig']['endpointPublicAccess']

    cloudformation = cloudformation()
    clusterStackINFO = describe_stack(cloudformation, cluster)
    for instance in xrange(len(clusterStackINFO['Stacks'][0]['Parameters'])):
        parameterKey = (clusterStackINFO['Stacks'][0]['Parameters'][instance]['ParameterKey'])
        if(parameterKey == 'PublicIp'):
            # False
            PulicIpValue = (clusterStackINFO['Stacks'][0]['Parameters'][instance]['ParameterValue'])
    
    return {'privateAccess': privateAccess, 'publicAccess': publicAccess, 'PulicIpValue': PulicIpValue}

def times():
    day = time.strftime("%A")
    month = time.strftime("%B")
    date = time.strftime("%d %H:%M:%S")
    year = time.strftime("%Y")

    return {'day': day, 'month': month, 'date': date, 'year': year}

printLogMsg = False
def logger(logFile, logMsg, printLogMsg, newLine):
    """ 
    Logger for calling program. 
    
    Parameters:
    logFile (str): File to be logged to
    logMsg (str): Message to be logged
    printLogMsg (bool): Option to print log message
    newLine (str): Option to prepend newline to the top, both or bottom only
  
    Returns: 
    int: Description of return value 
    """

    if(printLogMsg is True):
        print(logMsg)

    program = sys.argv[0]
    program = program.rsplit('/', 1)[-1]\
    
    if(newLine == 'top'):
        logFile.write('\n' + str(program) + " " + str(times()['day'][:3]) + " " + str(times()['month'][:3]) + " " + str(times()['date']) + " " + str(time.tzname[0]) + " " + str(times()['year']) + " - " + str(logMsg))    
    elif(newLine == 'both'):
        logFile.write('\n' + str(program) + " " + str(times()['day'][:3]) + " " + str(times()['month'][:3]) + " " + str(times()['date']) + " " + str(time.tzname[0]) + " " + str(times()['year']) + " - " + str(logMsg) + '\n')   
    elif(newLine == 'bottom'):
        logFile.write(str(program) + " " + str(times()['day'][:3]) + " " + str(times()['month'][:3]) + " " + str(times()['date']) + " " + str(time.tzname[0]) + " " + str(times()['year']) + " - " + str(logMsg) + '\n')

# def cluster_deletion():
#     env_clusters_url = env_url + "/clusters"
#     # projects_request = UrlRequest(env_clusters_url, key, secret)
#     # output = projects_request.output
        
#     response = requests.get(env_clusters_url, auth=(key, secret), headers=headers, verify=False)
#     binary = response.content
#     output = json.loads(binary)

#     for counter in range(len(output['data'])):
#         cluster_name = output['data'][counter]['name']           
#         if(folder_name == cluster_name):
#             cluster_id = output['data'][counter]['id']
#             cluster_delete_url = "%s/%s" % (env_clusters_url, cluster_id)
#             cluster_delete_url = cluster_delete_url[:4] + 's' + cluster_delete_url[4:]
#             cluster_delete_url = "curl -u \"%s:%s\" -X DELETE -H 'Accept: application/json' '%s'" % (key, secret, cluster_delete_url)
#             p = subprocess.Popen([cluster_delete_url], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             out, err = p.communicate()

# cluster_detected =  False
# def cluster_detection(url):
#     global cluster_detected
#     url = url + "/clusters"
#     # projects_request = UrlRequest(env_clusters_url, key, secret)
#     # output = projects_request.output
        
#     response = requests.get(url, auth=(key, secret), headers=headers, verify=False)
#     binary = response.content
#     output = json.loads(binary)

#     for counter in range(len(output['data'])):
#         cluster_name = output['data'][counter]['name']           
#         if(folder_name == cluster_name):
#             cluster_id = output['data'][counter]['id']
#             cluster_detected = True
#             print("ERROR: Cluster already exist!")
#             cd(folder_name)
#             shutil.rmtree(folder_name, ignore_errors=True)
#             print('NOTE: Cluster folder cleaning complete')
#             # cluster_deletion()
#             sys.exit()

# cluster_detection()        

#parses through a stack object for desired parameters, fixing order issues where necessary to meet SQL standards
def generateInsertCommand(info, stack, aws_account, rows, region):
    cmdbvals = []

    tags = ['PrimaryOwner', 'SharedInfrastructure', 'PatchGroup', 'ProvisionType', 'SecondaryOwner', 'ApplicationDeploymentCIID', 'CostCenterID', 'ProjectCode']
    #print(pdkslibrary.ppJSON(stack["Tags"]))
    cluster_name= ''
    nodegroupname = ''
    
    description = stack["Description"]
    NodeInstanceRole = ""
    NodeSecurityGroup = ""
    for dict in info["StackResourceSummaries"]:
        # print(pdkslibrary.ppJSON(dict))
        # for resources in dict:
            
        if (dict["LogicalResourceId"] == "NodeInstanceRole"):
            NodeInstanceRole = dict["PhysicalResourceId"]
            #print("NodeInstanceRole: " + NodeInstanceRole)
        if (dict["LogicalResourceId"] == "NodeSecurityGroup"):
            NodeSecurityGroup = dict["PhysicalResourceId"]
            #print("NodeSecurityGroup: " + NodeSecurityGroup)
    #print(pdkslibrary.ppJSON(info))
    count = 0
    valuesCommand = ""
    tempStore = ""
    subnetStore = ""
    flipped = False
    secondFlipped = False
    # print(stack_name)
    # print('')
    
    
    for param in stack["Parameters"]:
        #print(pdkslibrary.ppJSON(param["ParameterValue"]))
        #print(len(param))
        # if (count >= 1 & (param["ParameterKey"] != headers[count] )):
        #     valuesCommand = valuesCommand + "\'\',"
        if ('\'' in param["ParameterValue"]):
            param["ParameterValue"] = param["ParameterValue"].replace('\'', '\'\'')

        if (len(stack["Parameters"]) ==14 and count == 11):
            valuesCommand = valuesCommand + "\'" + NodeInstanceRole + "\', " + "\'" + NodeSecurityGroup + "\', " + "\'" + param["ParameterValue"] + "\', "
        
        elif (count == 0 and param["ParameterKey"] == "ClusterControlPlaneSecurityGroup"):
            flipped = True
            tempStore = param["ParameterValue"]

        elif (count == 7 and param["ParameterKey"] == "Subnets"):
            secondFlipped = True
            subnetStore = param["ParameterValue"]
            
        else:
            
            valuesCommand = valuesCommand + "\'" + param["ParameterValue"] + "\', "
            
            # if (count < len(stack["Parameters"])-1):
            #     valuesCommand = valuesCommand + ", "
            
            if(flipped == True and count == 1):
                valuesCommand = valuesCommand + "\'" + aws_account + "\', " + "\'" + tempStore + "\', "
            if(secondFlipped == True and count == 8):
                valuesCommand = valuesCommand + "\'" + subnetStore + "\',"
        if (count == 0 and flipped == False):
            valuesCommand = valuesCommand + "\'" + aws_account + "\',"
        if (param["ParameterKey"] == "ClusterName"):
            cluster_name = param["ParameterValue"]
        if (param["ParameterKey"] == "NodeGroupName"):
            nodegroupname = param["ParameterValue"]
        
        
        
        # if (count == len(param) -1):
        #     valuesCommand = valuesCommand + "\'" + description + "\'"
        count = count + 1
    # print(cluster_name)
    clusterindex = 0
    rowcount = 0
    for row in rows:
        
        if row[0] == cluster_name:
            clusterindex = rowcount % 8
            for clusterrow in rows[clusterindex: clusterindex+8]:
                cmdbvals.append(clusterrow[3])
                #print(clusterrows)
            break
        rowcount = rowcount + 1
    version = is_v1_or_v2_cluster(cluster_name, aws_account)
    
    valuesCommand = valuesCommand + "\'" + description + "\'," + "\'" + version + "\'"
    tagStore = ['', '', '', '', '', '', '', '']
    
    #print(pdkslibrary.ppJSON(stack["Tags"]))
    for tag in stack["Tags"]:
        if tag["Key"] in tags:
            index = tags.index(tag["Key"])
            tagStore[index] = tag["Value"]
        if tag["Key"] =="Patch Group":
            tagStore[2] = tag["Value"]
        
    for value in tagStore:
        if value == '':
            valuesCommand = valuesCommand + ",\'" + "N/A" + "\'"
        else:
            valuesCommand = valuesCommand + ",\'" + value + "\'"
    # node_info = pdkslibrary.get_all_node_group_info(cluster_name, nodegroupname)
    # print(pdkslibrary.ppJSON(node_info))
    #print(cmdbvals)
    valuesCommand = valuesCommand + ",\'" + region + "\', \'\', \'\'"
    return valuesCommand, nodegroupname, cluster_name
    # print (valuesCommand)
    # print ('')  

# def stack_modification(cluster_name, asgsss, tags):
#     if(tags is passed in then check for the respective variables):
#         pass

def downloadDelete(fileDownloadURL, outputFilename):
    if(os.path.exists(outputFilename)):
        os.remove(outputFilename) 

    wget.download(fileDownloadURL, out=outputFilename, bar=None)
    fileInMemory = open(outputFilename, "r")

    if(os.path.exists(outputFilename)):
        os.remove(outputFilename) 
    
    return fileInMemory

def create_csv(file_name, file_headers):
    with open(file_name,'w') as csvFile:
        writer = csv.DictWriter(csvFile,fieldnames=file_headers)
        writer.writeheader()
    csvFile.close()

def row_values_writer(data, file_name, file_headers):
    with open(file_name,'a+') as csvFile:
        writer = csv.DictWriter(csvFile,fieldnames=file_headers)
        writer.writerow(data)
        
def create_groups_two_rows(user_group_name, user_cluster_name, user_primary_cluster_owner, user_secondary_cluster_owner, user_requesting_user, file_name, file_headers):
    groupSSO = 'pdks-' + user_cluster_name + '-' + user_group_name + '-sso'
    domain = 'Amer'
    primaryOwnerNTID = user_primary_cluster_owner
    secondaryOwnerNTID = user_secondary_cluster_owner
    customOU = 'Amazon'

    members = user_primary_cluster_owner + ' ' + user_secondary_cluster_owner + ' ' + user_requesting_user
    description_base = 'PDKS EKS Cluster' + user_cluster_name + ' ' + user_group_name

    group_tags = ['U', 'S']
    for group in group_tags:
        if group == 'U':
            rowValuesList = {'GroupSSO': groupSSO, 'Domain': domain, 'GroupDescription': description_base + '-' + group , 'PrimaryOwnerNTID': primaryOwnerNTID, 'SecondaryOwnerNTID': secondaryOwnerNTID, 'CustomOU': customOU, 'Members': members}
            row_values_writer(rowValuesList, file_name, file_headers)
        elif (group == 'S'):
            rowValuesList = {'GroupSSO': groupSSO, 'Domain': domain, 'GroupDescription': description_base + '-' + group , 'PrimaryOwnerNTID': primaryOwnerNTID, 'SecondaryOwnerNTID': secondaryOwnerNTID, 'CustomOU': customOU, 'Members': ''}
            row_values_writer(rowValuesList, file_name, file_headers)
            
def create_groups_four_rows(user_group_name, user_cluster_name, user_primary_cluster_owner, user_secondary_cluster_owner, user_requesting_user, file_name, file_headers):
    # GroupSSO, updated
    sso_spec = ['cau', 'cas', 'cdu', 'cds']
    group_sso_base = 'pdks-' + user_cluster_name + '-'
    
    # Domain, constant
    domain = 'Amer'

    # group description, constant
    group_description_base = 'PDKS EKS Cluster ' + user_cluster_name + " Cust "

    # Primary and Secondary Owners, static
    primaryOwnerNTID = user_primary_cluster_owner
    secondaryOwnerNTID = user_secondary_cluster_owner

    # constant customOU
    customOU = 'Amazon'

    # constant members
    members = user_primary_cluster_owner + ' ' + user_secondary_cluster_owner + ' ' + user_requesting_user

    for i, sso in enumerate(sso_spec):
        group_sso_write = group_sso_base + sso + '-sso'
        group_description_write = ''
        # U group
        if i % 2 == 0:
            # Admin or DevOps
            if i < 2:
                group_description_write = group_description_base + 'Admin-U'
            else:
                group_description_write = group_description_base + 'DEVOPS-U'

        # S group
        else:
            # Admin or DevOps
            if i < 2:
                group_description_write = group_description_base + 'Admin-S'
            else:
                group_description_write = group_description_base + 'DEVOPS-S'
        
        if (sso == 'cau'):
            rowValuesList = {'GroupSSO': group_sso_write, 'Domain': domain, 'GroupDescription': group_description_write, 'PrimaryOwnerNTID': primaryOwnerNTID, 'SecondaryOwnerNTID': secondaryOwnerNTID, 'CustomOU': customOU, 'Members': members}
            row_values_writer(rowValuesList, file_name, file_headers)
        else:
            rowValuesList = {'GroupSSO': group_sso_write, 'Domain': domain, 'GroupDescription': group_description_write, 'PrimaryOwnerNTID': primaryOwnerNTID, 'SecondaryOwnerNTID': secondaryOwnerNTID, 'CustomOU': customOU, 'Members': ''}
            row_values_writer(rowValuesList, file_name, file_headers)

def create_active_groups_file(cluster_name, file_name, group_name, file_headers):
    spec = ['cau', 'cas', 'cdu', 'cds']
    account_id = '330470878083'
    file_type = 'ssofile'
    
    for s in spec:
        rowValuesList = {
            'account_id': account_id, 
            'cluster_name': cluster_name + '-' + spec + '-ps',
            'group_sso': 'pdks-' + cluster_name + '-cau-sso', 
            'group_name': group_name, 
            'file_type': file_type
        }
        row_values_writer(rowValuesList, file_name, file_headers)

        rowValuesList = {
                'account_id': account_id, 
                'cluster_name': cluster_name + group_name + "-ps",
                'group_sso': 'pdks-' + cluster_name + '-'+ group_name + '-sso', 
                'group_name': group_name, 
                'file_type': file_type
            }
        row_values_writer(rowValuesList, file_name, file_headers)
        