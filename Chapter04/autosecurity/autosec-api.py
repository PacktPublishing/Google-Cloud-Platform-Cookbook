"""
@Purpose: The program read the logs for instance creation activity and terminates instances
which are not authorised to be created
Snippets taken from GCP Github samples : https://github.com/GoogleCloudPlatform/python-docs-samples

@author: Legorie
"""

from apiclient.discovery import build
from oauth2client.client import GoogleCredentials
from googleapiclient.errors import HttpError
import googleapiclient.discovery
import json
import argparse
import datetime
import time

def format_rfc3339(datetime_instance=None):
    """Formats a datetime per RFC 3339.
    :param datetime_instance: Datetime instanec to format, defaults to utcnow
    """
    return datetime_instance.isoformat("T") + "Z"

def get_start_time():
    # Return now- 5 minutes
    start_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=600)
    return format_rfc3339(start_time)


def get_now_rfc3339():
    # Return now
    return format_rfc3339(datetime.datetime.utcnow())

def wait_for_operation(compute, project, zone, operation):
    print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()

        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result

        time.sleep(1)

def delete_instance(compute, project, zone, name):
    return compute.instances().delete(
        project=project,
        zone=zone,
        instance=name).execute()

def verify_mctype_kill(machine, user, instance_name, zone, project):
	# A * to indicate the NOT allowed machine types
	allowed_machines = ['*f1-micro','g1-small', 'n1-standard', '*n1-highmem', '*n1-highcpu', '*n1-megamem']
	mc_split = machine.split('-')
	if len(mc_split) == 3:
		mc_split.pop()
	mc_type = '-'.join(mc_split)

	if mc_type not in allowed_machines:
		print(instance_name + ' has a machine type of ' + mc_type + ' which is not an allowed.')
		compute = googleapiclient.discovery.build('compute', 'v1')
		print("Verifying if machine is present ..." + instance_name)
		try:
			request  = compute.instances().get(project=project_id, zone=zone, instance=instance_name)
			response = request.execute()
		except HttpError as err:
			# If the error is a rate limit or connection error,
			# wait and try again.
			if err.resp.status in [404]:
				print("Instance not found")
				return
			else: raise
		print('Deleting instance ' + instance_name)
		op = delete_instance(compute, project_id, zone, instance_name)
		wait_for_operation(compute, project, zone, op['name'])


def check_logs(project_id):
	# Checks the logs for the creation event of an instance using filters & processes the response
	credentials = GoogleCredentials.get_application_default()
	service = build('logging', 'v2', credentials=credentials)

	req_body = { "resourceNames": ["projects/"+ project_id], 
				"filter": 'logName=projects/'+ project_id +'/logs/cloudaudit.googleapis.com%2Factivity AND ' 
							'resource.type=gce_instance AND protoPayload.methodName=beta.compute.instances.insert AND '
							'operation.first=True AND '
							'timestamp >= "' + get_start_time() + '"' 
				}
	collection = service.entries()
	request = collection.list(body=req_body)
	response = request.execute()
	#print(response)
	#print('----')
	if response != {} :
		for res in response['entries']:
			mctype = res['protoPayload']['request']['machineType'].split('/')
			user = res['protoPayload']['authenticationInfo']['principalEmail']
			instance = res['protoPayload']['resourceName'].split('/')
			zone = res['resource']['labels']['zone']
			verify_mctype_kill(mctype[-1], user, instance[-1], zone, project_id)
	else:
		print('No instance creation activity found.')


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
	description="Automated security check xxxx",
	formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument('project_id', help='Your Cloud Platform project ID.')

	args = parser.parse_args()
	project_id = args.project_id

	check_logs(project_id)