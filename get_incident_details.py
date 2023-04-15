#!/usr/bin/env python

import requests
import sys
import json
from datetime import date, timedelta
import csv

#Your PagerDuty API key.  A read-only key will work for this.
AUTH_TOKEN = 'YOURKEYHERE'
#The API base url, make sure to include the subdomain
BASE_URL = 'https://YOURSUBDOMAIN.pagerduty.com/api/v1'
#The service ID that you would like to query.  You can leave this blank to query all services.
service_id = ""
#The start date that you would like to search.  It's currently setup to start yesterday.
yesterday = date.today() - timedelta(1)
#since = yesterday.strftime('%Y-%m-%d')
since = "2014-04-28"
#The end date that you would like to search.
#until = date.today().strftime('%Y-%m-%d')
until = "2014-05-02"

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
        output = incident["id"] + "," + str(incident["incident_number"]) + "," + incident["service"]["name"] + "," + incident["created_on"] + "," + incident["last_status_change_on"] + ","
        output += incident["trigger_summary_data"]["subject"].replace(",","") + ","
        if incident["resolved_by_user"]:
            output += incident["resolved_by_user"]["name"] + ","
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
  get_incident_stats(since,until,"")

if __name__=='__main__':
  sys.exit(main())

