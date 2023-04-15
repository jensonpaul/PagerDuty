#Get the latest activity for all users within a PagerDuty account.
#This script is not supported by PagerDuty.

#!/usr/bin/env python

import datetime
import requests
import sys

#Your PagerDuty API key.  A read-only key will work for this.
AUTH_TOKEN = '5QfeCFdpZoqt9LwXrjYd'
#The API base url, make sure to include the subdomain
BASE_URL = 'https://pdt-ryan.pagerduty.com/api/v1'

HEADERS = {
	'Authorization': 'Token token={0}'.format(AUTH_TOKEN),
	'Content-type': 'application/json',
}

user_count = 0

def get_user_count():
	global user_count
	count = requests.get(
		'{0}/users'.format(BASE_URL),
		headers=HEADERS
	)
	user_count = count.json()['total']

def get_users(offset):
	global user_count

	params = {
		'offset':offset
	}
	all_users = requests.get(
		'{0}/users'.format(BASE_URL),
		headers=HEADERS,
	params=params
	)
	print "Listing all users:"
	for user in all_users.json()['users']:
		print user['name']
		print user['id']
		get_log_entries(user['id'])


def get_log_entries(user_id):
	log_entries = requests.get(
		'{0}/users/{1}/log_entries'.format(BASE_URL, user_id),
		headers=HEADERS
	)
	if log_entries.json()['total'] > 0:
		log_entry = log_entries.json()['log_entries'][0]
		print log_entry['created_at']
	else:
		print "No activity"

def main(argv=None):
	if argv is None:
		argv = sys.argv

	get_user_count()

	for offset in xrange(0,user_count):
		if offset % 25 == 0:
			get_users(offset)

if __name__=='__main__':
	sys.exit(main())
