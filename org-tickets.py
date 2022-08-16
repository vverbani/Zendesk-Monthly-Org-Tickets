# Importing the libraries
from ast import Or
import requests
from datetime import datetime

### IMPORTANT - YOU WILL NEED 4 OF THESE ITEMS FOR THIS TO WORK
### 1 - ZENDESK API KEY
### 2 - ORGANIZATION NAME: Modulr
### 3 - Start date, i.e 2022-07-01
### 4 - End date, i.e 2022-07-31
### 5 - Org Zendesk sub domain (can get while creating Zendesk API token)
ZENDESK_API_KEY= ''
ORGANIZATION_NAME= ''
STARTING_DATE= '2022-04-01' # %Y-%m-%d format
ENDING_DATE= '2022-04-30'   # %Y-%m-%d format
ZD_SUBDOMAIN= ''

HEADERS= {'Authorization': ZENDESK_API_KEY}

# Variables used
org_name_URL= "https://" + ZD_SUBDOMAIN + ".zendesk.com/api/v2/organizations/autocomplete.json?name=" + ORGANIZATION_NAME
org_name_json= requests.get(url= org_name_URL, headers= HEADERS).json()
org_id= org_name_json['organizations'][0]['id']
sla= org_name_json['organizations'][0]['organization_fields']['sla_type']
org_tickets_URL= "https://" + ZD_SUBDOMAIN + ".zendesk.com/api/v2/organizations/" + str(org_id) + "/tickets"

# Convert string dates into the correct date format
starting_date= datetime.strptime(STARTING_DATE, '%Y-%m-%d')
ending_date= datetime.strptime(ENDING_DATE, '%Y-%m-%d')

# Sending get request an saving the response as response object
org_tickets_data= requests.get(url= org_tickets_URL, headers= HEADERS).json()

print("=========================================")
print("Ticket Id", "Priority", "SLA", "Reply Time")
print("=========================================")

for ticket in org_tickets_data['tickets']:

    # Right scope as each ticket has a different reply time
    reply_time= ''

    # Get tickets in-between the start date and end date, i.e July1st - July 31st
    if datetime.strptime(ticket['created_at'][0:10], '%Y-%m-%d') >= starting_date and datetime.strptime(ticket['created_at'][0:10], '%Y-%m-%d') <= ending_date:

        full_ticket_metrics_URL= "https://" + ZD_SUBDOMAIN +".zendesk.com/api/v2/tickets/" + str(ticket['id']) + "/metrics"
        ticket_response= requests.get(url= full_ticket_metrics_URL, headers= HEADERS)
        ticket_response_data= ticket_response.json()

        # Gold is 24/7 while the other SLAs are weekday only, make sure to grab the correct reply time
        if sla == 'gold': reply_time= ticket_response_data['ticket_metric']['reply_time_in_minutes']['calendar']
        else: reply_time= ticket_response_data['ticket_metric']['reply_time_in_minutes']['business']

        if reply_time > 60:
             # Get hours with floor division and additional minutes with modulus
            hours= reply_time // 60
            minutes= reply_time % 60
        else:
            hours= 0
            minutes= reply_time

        print(ticket['id'], ticket['priority'], sla, "{}h {}".format(hours, minutes))




