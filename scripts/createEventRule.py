"""
create a cloud-events rule, with condition eventType=AuditEvents  and eventName=[CreateSubnet,UpdateSUbnet] and fires an Fn Function
"""

import oci
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--profile", help="OCI config profile to use", type=str, default="DEFAULT")
parser.add_argument("-f", "--function_id", help="function id to invoke", type=str, required=True)
parser.add_argument("-r", "--rule_name", help="rule name", type=str, required=True)

pargs = parser.parse_args(sys.argv[1:])

config = oci.config.from_file(profile_name=pargs.profile)

events_client = oci.cloud_events.cloud_events_client.CloudEventsClient(config)


result = events_client.create_rule(
	oci.cloud_events.models.CreateRuleDetails(
		display_name = pargs.rule_name,
		description = pargs.rule_name,
		is_enabled = True,
		# create and update events will trigger the function
		condition = '{"eventType":["com.oraclecloud.audit.v1"],"data": {"eventName":["CreateSubnet", "UpdateSubnet"]}}',
		compartment_id = config["tenancy"],

		actions = oci.cloud_events.models.ActionDetailsList(actions = 
			[
				oci.cloud_events.models.CreateFaaSActionDetails(
				action_type = "FAAS", 
				description = "Networking Event Aanalysis", 
				is_enabled = True,
				function_id = pargs.function_id)
			]
		)
	)
)

# wait until the rule is active
get_result  = oci.wait_until(
	events_client,
	events_client.get_rule(result.data.id),
	'lifecycle_state',
	'ACTIVE'
)

print (f"rule {get_result.data.display_name} is active")

