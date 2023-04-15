##Tested and verified in python3 env

#!/usr/bin/python3
import requests
import csv
import json

headers = {
    "Content-Type": "application/json",
    "Accept": "application/vnd.pagerduty+json;version=2",
    "Authorization": "Token token=xxxxxxxxxxxx" ##Replace your api token here
}

def get_pd_users():
    #CSV file header for your report file
    header=['UserName', 'Email', 'Role']
    with open('pagerduty_users.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for offset in range(0, 2000, 100):
            url = 'https://api.pagerduty.com/users?limit=100&offset={0}'.format(offset)
            response = requests.request("GET", url, headers=headers)
            p=json.loads(response.text)
            for x in range(len(p['users'])):
                Usr_name = p['users'][x]['name']
                Mail_id = p['users'][x]['email']
                Role = p['users'][x]['role']
                output = (Usr_name,Mail_id,Role)
                out_list = list(output)
                writer.writerow(out_list)

def main():
    get_pd_users()

if __name__ == "__main__":
    main()