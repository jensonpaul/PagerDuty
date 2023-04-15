#!/usr/bin/env python
 
import requests
import sys
import json
import time
from datetime import date, timedelta
 
#Your PagerDuty API key.  A read-only key will work for this.
AUTH_TOKEN = 'YOUR_API_TOKEN'
#The API base url, make sure to include the subdomain
BASE_URL = 'https://YOUR_SUBDOMAIN.pagerduty.com/api/v1'
#The service ID that you would like to query.  You can leave this blank to query all services.
service_id = ""
#The start date that you would like to search.
since = "2014-11-00"
#The end date that you would like to search.
until = "2014-11-25"
 
HEADERS = {
    'Authorization': 'Token token={0}'.format(AUTH_TOKEN),
    'Content-type': 'application/json',
}
 
def get_incident_count(since,until,service_id=None):
    global incident_count
 
    params = {
        'service':service_id,
        'since':since,
        'until':until
    }
    print '{0}/incidents/count'.format(BASE_URL)
    count = requests.get(
        '{0}/incidents/count'.format(BASE_URL),
        headers=HEADERS,
        data=json.dumps(params)
    )
    incident_count = count.json()['total']
 
def get_incidents(since, until, offset, service_id=None):
    print "offset:" + str(offset)
    file_name = 'pagerduty_export'
    output = ""
 
    params = {
        'service':service_id,
        'since':since,
        'until':until,
        'offset':offset
    }
 
    all_incidents = requests.get(
        '{0}/incidents'.format(BASE_URL),
        headers=HEADERS,
        data=json.dumps(params)
    )
 
    f = open(file_name + since + ".csv",'a')
    for incident in all_incidents.json()['incidents']:
        duration = (time.mktime(time.strptime(incident["last_status_change_on"], "%Y-%m-%dT%H:%M:%SZ")) - time.mktime(time.strptime(incident["created_on"], "%Y-%m-%dT%H:%M:%SZ")))/60
        output = str(incident["incident_number"]) + "," + incident["service"]["name"] + "," + incident["created_on"] + "," + incident["last_status_change_on"] + "," + str(duration) + ","
        if 'subject' in incident["trigger_summary_data"].keys():
            output += incident["trigger_summary_data"]["subject"].replace(",","") + ","
        elif 'description' in incident["trigger_summary_data"].keys():
            output += incident["trigger_summary_data"]["description"].replace(",","") + ","
        else:
            output += ","
        output += str(incident["number_of_escalations"]) + "\n"
        f.write(output)
 
def get_incident_stats(since,until,service_id=None):
    get_incident_count(since,until,service_id)
    print "Number of incidents: ", incident_count
    for offset in xrange(0,incident_count):
        if offset % 100 == 0:
            get_incidents(since, until, offset, service_id)
 
    print "Exporting has completed successfully."
 
def main(argv=None):
  if argv is None:
    argv = sys.argv
  get_incident_stats(since,until,service_id)
 
if __name__=='__main__':
  sys.exit(main())