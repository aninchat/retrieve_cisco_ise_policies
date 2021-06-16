# retrieve_cisco_ise_policies

This script is built to retrieve all policy information from ISE and store it in an easily consumable .csv file. Sample run of the script:

```
(python3.8) aninchat@aninchat-ubuntu:~/Automation/Python/$ python get_policies_from_ise.py 
Please provide the IP address for the ISE PAN: 172.16.3.1
Please provide the username for login: admin
Please provide the password for login: 
Please provide the exact path (with file name) where the policy information will need to be stored: /home/aninchat/Automation/Python/Infosys/test.csv
Gathering SGT information from ISE
Gathering policy information from ISE
                                                                               Policy data from ISE                                                                               
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃    Policy ID     ┃   Policy Name    ┃ Source SGT Name ┃ Source SGT Value ┃ Destination SGT  ┃ Destination SGT  ┃  Status  ┃ Contract Name ┃     Contract     ┃      ACEs       ┃
┃                  ┃                  ┃                 ┃                  ┃       Name       ┃      Value       ┃          ┃               ┃   Description    ┃                 ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ 92c1a900-8c01-1… │     ANY-ANY      │       ANY       │      65535       │       ANY        │      65535       │ ENABLED  │   Permit IP   │ Permit IP SGACL  │    permit ip    │
│ fd46e261-ccff-1… │ Developers-Grou… │   Developers    │        8         │   Group1_Type2   │        19        │ DISABLED │ AllowDHCPDNS  │ Sample contract  │ permit udp dst  │
│                  │                  │                 │                  │                  │                  │          │               │  to allow DHCP   │      eq 67      │
│                  │                  │                 │                  │                  │                  │          │               │     and DNS      │ permit udp dst  │
│                  │                  │                 │                  │                  │                  │          │               │                  │      eq 68      │
│                  │                  │                 │                  │                  │                  │          │               │                  │ permit tcp dst  │
│                  │                  │                 │                  │                  │                  │          │               │                  │      eq 53      │
│                  │                  │                 │                  │                  │                  │          │               │                  │ permit tcp dst  │
│                  │                  │                 │                  │                  │                  │          │               │                  │     eq 5353     │
│                  │                  │                 │                  │                  │                  │          │               │                  │ permit udp dst  │
│                  │                  │                 │                  │                  │                  │          │               │                  │      eq 53      │
│                  │                  │                 │                  │                  │                  │          │               │                  │ permit udp dst  │
│                  │                  │                 │                  │                  │                  │          │               │                  │     eq 5353     │
│                  │                  │                 │                  │                  │                  │          │               │                  │     deny ip     │
│ 90cabfd1-ccdc-1… │ Group1_Type1-Gr… │  Group1_Type1   │        18        │   Group1_Type2   │        19        │ ENABLED  │   AllowWeb    │ Sample contract  │ permit tcp dst  │
│                  │                  │                 │                  │                  │                  │          │               │ to allow access  │      eq 80      │
│                  │                  │                 │                  │                  │                  │          │               │      to Web      │ permit tcp dst  │
│                  │                  │                 │                  │                  │                  │          │               │                  │     eq 443      │
│                  │                  │                 │                  │                  │                  │          │               │                  │ permit udp dst  │
│                  │                  │                 │                  │                  │                  │          │               │                  │     eq 443      │
│                  │                  │                 │                  │                  │                  │          │               │                  │     deny ip     │
│ ec487371-ccff-1… │ Group1_Type1-Ne… │  Group1_Type1   │        18        │ Network_Services │        3         │ ENABLED  │    Deny IP    │  Deny IP SGACL   │     deny ip     │
│ f42ae231-ccff-1… │ Group1_Type2-Ex… │  Group1_Type2   │        19        │     Extranet     │        17        │ MONITOR  │    Deny IP    │  Deny IP SGACL   │     deny ip     │
└──────────────────┴──────────────────┴─────────────────┴──────────────────┴──────────────────┴──────────────────┴──────────┴───────────────┴──────────────────┴─────────────────┘

Finished writing into policy file, stored in path /home/aninchat/Automation/Python/test.csv
```
