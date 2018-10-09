import boto3
import logging
import time
from botocore.exceptions import ClientError
import botocore
import os


def create_vpcs():

    ec2 = boto3.client('ec2')



    response = ec2.describe_vpcs()

    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

    logger=logging.getLogger('vpc')
    hdlr=logging.FileHandler('vpc.log')

    formatter = logging.Formatter('%(asctime)s %(message)s')

    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)




    for i in range(10):
        try:

            response = ec2.create_security_group(GroupName=str(i)+'HelloBOTO',

                                                 Description='Made by boto3',

                                                 VpcId=vpc_id)

            security_group_id = response['GroupId']

            print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))



            data = ec2.authorize_security_group_ingress(

                GroupId=security_group_id,

                IpPermissions=[

                    {'IpProtocol': 'tcp',

                     'FromPort': 80,

                     'ToPort': 80,

                     'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},

                    {'IpProtocol': 'tcp',

                     'FromPort': 22,

                     'ToPort': 22,

                     'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}

                ])

            print('Ingress Successfully Set %s' % data)


        except ClientError as e:


            print(e)
        logger.error('ERROR occurred')
        logger.info('INFO')


        timeout = time.time() + 5
        while True:
            test = 0
            if test == 5 or time.time() > timeout:
                break
            test = test - 1

def delete_vpcs():
    logger=logging.getLogger('vpc')
    hdlr=logging.FileHandler('vpc.log')

    formatter = logging.Formatter('%(asctime)s %(message)s')

    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    # Create EC2 client

    ec2 = boto3.client('ec2')



    # Delete security group
    for i in range(10):
        try:

            response = ec2.delete_security_group(GroupName=str(i)+'HelloBOTO')

            print('Security Group Deleted')

        except ClientError as e:

            print(e)
        logger.error('ERROR occurred')
        logger.info('deleted')

def check_groupid():
    client = boto3.client('ec2')

    result = client.describe_security_groups()
    for value in result["SecurityGroups"]:
        print(value['GroupId'])
        print(value['VpcId'])
        print(value['GroupName'])
