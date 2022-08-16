# Get Monthly Ticket Info Per Company

This repo is to automate retrieving monthly ticket information per organization from Zendesk. The script works by using the Zendesk API to hit your organization Zendesk data. It returns the following formate: Ticket Id, Ticket Priority, Organization SLA, Ticket reply time.

## Prerequisites

1. Latest [Python](https://www.python.org/downloads/) Version
2. [Zendesk API key](https://support.zendesk.com/hc/en-us/articles/4408889192858-Generating-a-new-API-token)
3. Update the line 11-15 inside `org-tickets.py`
4. Go in the directory of the python file

## Usage

```bash
    python3 org-tickets.py
```

**** PLEASE USE THIS AT YOUR OWN RISK ****
