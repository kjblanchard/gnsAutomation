#! /usr/bin/python3
# this requires appsettings.json file
# {
# instance = 'xyz'
# }
# TODO update the security group as well for when IP address changes - put this off as it is bedtime!
import argparse
from time import sleep
import boto3
import json
import urllib

RETRIES = 10
SLEEP_TIME = 5


def update_r53_record(zone_id, record_name, ip_address):
    client = boto3.client('route53')
    response = client.change_resource_record_sets(
        HostedZoneId=zone_id,
        ChangeBatch={
            "Comment": "Update Gns3 ip",
            "Changes": [
                {
                    "Action": "UPSERT",
                    "ResourceRecordSet": {
                        "Name": record_name,
                        "Type": "A",
                        "TTL": 300,
                        "ResourceRecords": [
                            {
                                "Value": ip_address
                            },
                        ],
                    }
                },
            ]
        }
    )
    print(response)


def update_security_group(ip, sg_id, sg_rules):
    """Update the security group with our public IP."""
    sg_rules = [create_rule_string(rule, ip) for rule in sg_rules]
    response = ec2_client.modify_security_group_rules(
        GroupId=sg_id, SecurityGroupRules=sg_rules)


def create_rule_string(sg_rule_data: dict, ip: str) -> dict:
    return {'SecurityGroupRuleId': sg_rule_data.get('id'),
            'SecurityGroupRule': {
                'IpProtocol': sg_rule_data.get('protocol'),
                'FromPort': sg_rule_data.get('from'),
                'ToPort': sg_rule_data.get('to'),
                'CidrIpv4': f'{ip}/32',
                'Description': sg_rule_data.get('description')
    }
    }


def wait_for_public_ip(instance_id) -> str:
    print(f'Instance has been started, waiting for instance to get a public ip address..')
    for i in range(RETRIES):
        print(f'Attempt {i} of {RETRIES}')
        response = ec2_client.describe_instances(
            InstanceIds=[
                instance_id
            ],
        )
        public_ip = response.get('Reservations')[0].get(
            'Instances')[0].get('PublicIpAddress')
        if not public_ip:
            print('Waiting for next attempt..')
            sleep(SLEEP_TIME)
            continue
        else:
            return public_ip
    exit(1, 'Could not get IP address')


def start_instance(instance_id) -> str:
    print(f'Starting instance {instance_id}')
    response: dict = ec2_client.start_instances(
        InstanceIds=[
            instance_id
        ],
    )
    current_state_json = response.get('StartingInstances')
    if not current_state_json:
        pass
    current_state_json = current_state_json[0]
    return wait_for_public_ip(instance_id)


def stop_instance(instance_id):
    response: dict = ec2_client.stop_instances(
        InstanceIds=[
            instance_id
        ],
    )


parser = argparse.ArgumentParser(
    prog='Update GNS',
    description='Starts the GNS box, and updates the r53 ip for it, also can stop',
    epilog='Wut do you mean')
parser.add_argument('action', choices=[
                    'start', 'stop'], help="If you should start or stop the instance.")           # positional argument
with open('appsettings.json', 'r') as config_file:
    json_data: dict = json.load(config_file)

args = parser.parse_args()
should_start = True if 'start' in args.action else False
ec2_client = boto3.client("ec2")
instance_id = json_data.get('instance')
security_group_id = json_data.get('security_group_id')
security_group_rules = json_data.get('security_group_rules')

assert instance_id, 'No instance id inside of appsettings.json, closing..'
if (should_start):
    ip = start_instance(instance_id)
    zone = json_data.get('zone_id')
    record = json_data.get('record_name')
    update_r53_record(zone, record, ip)
    external_ip = urllib.request.urlopen(
        'https://ipinfo.io/ip').read().decode('utf8')
    update_security_group(external_ip, security_group_id, security_group_rules)
else:
    stop_instance(instance_id)

# Describe the thing.
