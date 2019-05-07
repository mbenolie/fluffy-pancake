#
# Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.
#
# Author: Michel Benoliel michel.benoliel@oracle.com
#
# Description: a python Fn function triggered by a CreateSubnet audit event
#              the function checks that the subnet was created with a free_form tag named "owner", 
#              if not,  it publishes a message to an ons topic with ocid = env variable ALERTS_TOPIC_ID
#

import oci
import io
import os
import base64
import json
import logging

from fdk import response

from oci.core import compute_client
from oci.core import virtual_network_client


try:
    import pytest

    def test_list_vcns():

        test_config, test_compartment_id = create_signer()
        oci_network = virtual_network_client.VirtualNetworkClient(test_config)
        result = oci_network.list_vcns(test_compartment_id)
        assert len(result.data) >= 0

except ImportError:
    pass


def ensure_env_var(key):
    val = os.environ.get(key)
    if not val:
        raise Exception(f"{val} is not set")

    return val


def create_signer():
    compartment_id = ensure_env_var("OCI_COMPARTMENT")

    config = {
        "key_content": base64.b64decode(
            ensure_env_var("OCI_PRIVATE_KEY_BASE64")),
        "pass_phrase": os.environ.get("OCI_PRIVATE_KEY_PASS", ""),
        "user": ensure_env_var("OCI_USER"),
        "tenancy": ensure_env_var("OCI_TENANCY"),
        "fingerprint": ensure_env_var("OCI_FINGERPRINT"),
        "region": ensure_env_var("OCI_REGION"),
    }

    return config, compartment_id

def convertAttributeName(att):
    newAtt = ""
    firstChar = True	
    for c in att:
        if c.isupper():
            if firstChar:
                newAtt += c.lower()
            else:
                newAtt += "_"
                newAtt += c.lower()
        else:
            newAtt += c
        firstChar = False
 			
    return newAtt

def createAuditEvent(event):
    ev = oci.audit.models.AuditEvent()
    eventData =  event.get("data")    
    for att in eventData:
        try:
            setattr(ev, convertAttributeName(att), eventData.get(att))
        except:
            print(traceback.format_exc())
			
    return ev


def handler(ctx, data: io.BytesIO=None):
    responseText  = "subnet is OK"
    try:
        config, compartment_id = create_signer()
        body = json.loads(data.getvalue())
        logging.info("Event Body=\n" + json.dumps(body))
 
        auditEvent = createAuditEvent(body)
        logging.info(f"Event Name: {auditEvent.event_name}")
        payload = auditEvent.response_payload
        if (auditEvent.event_name== "CreateSubnet"):
            subnetId = auditEvent.response_payload["Id"]
            logging.info(f"SubnetId: {subnetId}")
            config, compartment_id = create_signer()
            network_client = virtual_network_client.VirtualNetworkClient(config)
            subnet = network_client.get_subnet(subnetId).data
            logging.info(f"Subnet Data: {subnet.display_name}")
            if "owner" not in subnet.freeform_tags:
                ons_client = oci.ons.NotificationDataPlaneClient(config)
                responseText  = f"subnet {subnet.display_name} does not have an owner tag defined"
                topic_id = ensure_env_var("ALERTS_TOPIC_ID")
                onsMessage = oci.ons.models.MessageDetails()
                onsMessage.body = responseText  
                print (topic_id)
                ons_client.publish_message(topic_id, onsMessage)

            logging.info (responseText )
            
 
    except (Exception, ValueError) as ex:
        logging.info(str(ex))

    return response.Response(
        ctx, response_data=json.dumps(
            {"message": responseText  }),
        headers={"Content-Type": "application/json"}
    )
