<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <link rel="dns-prefetch" href="https://github.githubassets.com">
  <link rel="dns-prefetch" href="https://avatars0.githubusercontent.com">
  <link rel="dns-prefetch" href="https://avatars1.githubusercontent.com">
  <link rel="dns-prefetch" href="https://avatars2.githubusercontent.com">
  <link rel="dns-prefetch" href="https://avatars3.githubusercontent.com">
  <link rel="dns-prefetch" href="https://github-cloud.s3.amazonaws.com">
  <link rel="dns-prefetch" href="https://user-images.githubusercontent.com/">
    </head>
    <body>
# OCI Resource Configuration Governance using Events, Notifications, Audit and Functions Services


<p><b>Details</b><p>
The sample demonstrates the combination of 4 different OCI services to monitor OCI resource configuration. Specifically it checks in near real time whether a subnet was created wit the correct tags and if not alerts an administrator.
  
When a subnet is created an Audit event is automatically  emitted by the OCI Audit service to the OCI Events service. A rule within Events triggers an OCI Fucntion to  analyse the Audit event. 
The python sample looks for AuditEvents with eventName = "CreateSubnet"  and checks if the subnet was created with a free form tag named "owner". If not, it publishes a message on the OCI Notifiction topic. The sample can be easily extended to monitor other event types.

<h2><a id="user-content-deployment" class="anchor" aria-hidden="true" href="#deployment"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>Configuration</h2>
<p><b>Configure the Notifications Service</b></p>
<ul>
<li> Create a notification topic and name it "AuditAlerts" and write down the topic ocid, as you wil
     use it in your function configuration
  <div class="highlight highlight-source-shell"><pre>
      $ oci ons topic create --name CloudEventsAlerts --compartment-id your_compartment_id
      </pre></div>
</li>
<li> Subscribe to the topic with   protocol=Email
  <div class="highlight highlight-source-shell"><pre>
      $ oci ons subscription  create --protocol email \
        --subscription-endpoint michel.benoliel@oracle.com \
        --topic-id your_topic_id \
        --compartment-id your_compartment_id
      </pre></div>
  </li>
</ul>




<p><b>Required function configuration:</b></p>
<ul>
<li>OCI_USER - OCI user</li>
<li>OCI_TENANCY - OCI user tenancy</li>
<li>OCI_FINGERPRINT OCI user private key fingerprint</li>
<li>OCI_REGION - OCI region to talk to</li>
<li>OCI_COMPARTMENT - OCI compartment ID to search instances at</li>
<li>OCI_PRIVATE_KEY_BASE64 - OCI user private key encoded in BASE64</li>
<li>OCI_PRIVATE_KEY_PASS - OCI user private key pass phrase</li>
<li>ALERTS_TOPIC_ID - ONS  topic Id, to publish alerts</li>  
</ul>


<p>Test code locally</p>
Install pytest:

    python3 -m venv .venv
    source .venv/bin/activate
    pip3 install -r requirements.txt pytest
    
<p>Run tests:</p>

pytest -v -s --tb=long func.py

<p>Result:</p>
<div class="highlight highlight-source-shell"><pre>pytest -v -s --tb=long func.py 
========================= test session starts =========================
  
platform linux -- Python 3.7.1, pytest-4.0.1, py-1.8.0, pluggy-0.9.0 -- /home/opc/functions/python-fn/.venv/bin/python3.7
cachedir: .pytest_cache
rootdir: /home/opc/functions/create-subnet-event-fn, inifile:
plugins: asyncio-0.9.0
collected 1 item

func.py::test_list_vcns 2019-05-07 10:04:13,135 - oci.base_client.140249303662152 - INFO - Request: GET https://iaas.us-phoenix-1.oraclecloud.com/20160918/vcns
2019-05-07 10:04:13,139 - oci._vendor.urllib3.connectionpool - DEBUG - Starting new HTTPS connection (1): iaas.us-phoenix-1.oraclecloud.com:443
2019-05-07 10:04:13,815 - oci._vendor.urllib3.connectionpool - DEBUG - https://iaas.us-phoenix-1.oraclecloud.com:443 "GET /20160918/vcns?compartmentId=ocid1.compartment.oc1..aaaaaaaan7xxltzqchrbmhy76z6kcq5vjgk53bomoshzjdmvgmtu33hpwnrq HTTP/1.1" 200 759
2019-05-07 10:04:13,816 - oci.base_client.140249303662152 - DEBUG - Response status: 200
2019-05-07 10:04:13,818 - oci.base_client.140249303662152 - DEBUG - python SDK time elapsed for deserializing: 0.0017494764178991318
2019-05-07 10:04:13,818 - oci.base_client.140249303662152 - DEBUG - time elapsed for request: 0.6830082833766937
PASSED
====================== 1 passed in 2.43 seconds =======================
</pre></div>

<h2><a id="user-content-deployment" class="anchor" aria-hidden="true" href="#deployment"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a>Deployment</h2>
<p>Deploying a function:</p>
<div class="highlight highlight-source-shell"><pre>fn --verbose deploy --app oci</pre></div>
<p>Update your local env with the following <a href="https://github.com/mbenolie/oci-fn-audit-events/blob/master/scripts/setup_local.sh">script</a>.</p>
<p>Updating configuration:</p>
<div class="highlight highlight-source-shell"><pre>fn config fn oci list-instances OCI_USER <span class="pl-smi">${OCI_USER}</span>
fn config fn oci create-subnet-event-fn OCI_TENANCY <span class="pl-smi">${OCI_TENANCY}</span>
fn config fn oci create-subnet-event-fn OCI_FINGERPRINT <span class="pl-smi">${OCI_FINGERPRINT}</span>
fn config fn oci create-subnet-event-fn OCI_REGION <span class="pl-smi">${OCI_REGION}</span>
fn config fn oci create-subnet-event-fn OCI_COMPARTMENT <span class="pl-smi">${OCI_COMPARTMENT}</span>
fn config fn oci create-subnet-event-fn OCI_PRIVATE_KEY_BASE64 <span class="pl-smi">${OCI_PRIVATE_KEY_BASE64}</span>
fn config fn oci create-subnet-event-fn OCI_PRIVATE_KEY_PASS <span class="pl-smi">${OCI_PRIVATE_KEY_PASS}</span>
fn config fn oci create-subnet-event-fn ALERTS_TOPIC_ID <span class="pl-smi">${ALERTS_TOPIC_ID}</span>

</pre></div>
<p>Check the configuration:</p>
<div class="highlight highlight-source-shell"><pre>fn inspect fn oci list-instances</pre></div>
<p>make sure you're ok with a function's configuration you get from <code>inspect</code> command.</p>
</article>
      </div>
  </div>
 
<p><b>Configure the events Service</b></p>

You can create the Events rule in the Events service console or use the python <a href="https://github.com/mbenolie/oci-fn-audit-events/blob/master/scripts/createEventRule.py">script</a></p>
<div class="highlight highlight-source-shell">
  <pre>
     python3.7 createEventrule.py  --rule_name your_rule_name --function_id your_function_id
    
   </pre>
</div>   
      
<p><b>Test the whole scneario</b></p>
 <div class="highlight highlight-source-shell"><pre>
 <ul>
  <li> In OCI Console create a subnet. make sure you don't define a free-form tag named "owner"</li>
  <li>Check your mail for a notification message , saying "subnet <your subnet name> does not have an owner tag defined"</li>
  </ul>
 </pre>
</div>
</body></html>
