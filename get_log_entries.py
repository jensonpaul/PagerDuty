#!/usr/bin/env python

import requests
import sys
import json
import csv
from datetime import date, timedelta

#This script will export all log entries associated with a PagerDuty user.  All data is written to log_entries.csv.

#Your PagerDuty API key.  A read-only key will work for this.
AUTH_TOKEN = 'CzV4D2s8n2zfiYP4kAWs'
#The API base url, make sure to include the subdomain
BASE_URL = 'https://pdt-ryan.pagerduty.com/api/v1'
#The user ID that you want to query.  It is a 7+ character alphanumeric string.
user_id = "PIE6ZH7"
#The start date that you would like to search.  It's currently setup to start yesterday.
since = "2015-01-28"
#The end date that you would like to search.
until = "2015-05-02"

HEADERS = {
    'Authorization': 'Token token={0}'.format(AUTH_TOKEN),
    'Content-type': 'application/json',
}

def get_log_entries(since, until, user_id, offset):

    outfile = file('log_entries.csv', 'a')
    writer = csv.writer(outfile, delimiter=",", quoting=csv.QUOTE_MINIMAL)

    params = {
        'is_overview': 'true',
        'since': since,
        'until': until,
        'offset': offset
    }

    all_log_entries = requests.get(
        '{0}/users/{1}/log_entries'.format(BASE_URL, user_id),
        headers=HEADERS,
        data=json.dumps(params)
    )

    for log_entry in all_log_entries.json()['log_entries']:
        writer.writerow([log_entry['id'], log_entry['type'], log_entry['created_at']])
    outfile.close()

    offset += 100
    if offset < all_log_entries.json()['total']:
        get_log_entries(since, until, user_id, offset)

def main(argv=None):
    if argv is None:
        argv = sys.argv
    print "Exporting all log entries for user {0} between {1} and {2}".format(user_id, since, until)
    get_log_entries(since, until, user_id, 0)

if __name__=='__main__':
    sys.exit(main())

