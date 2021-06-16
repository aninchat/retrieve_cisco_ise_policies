# retrieve_cisco_ise_policies

This script is built to retrieve all policy information from ISE and store it in an easily consumable .csv file. Sample run of the script:

```
(python3.8) aninchat@aninchat-ubuntu:~/Automation/Python/$ python get_policies_from_ise.py 
Please provide the IP address for the ISE PAN: 172.16.3.1
Please provide the username for login: admin
Please provide the password for login: 
Please provide the exact path (with file name) where the policy information will need to be stored: /home/aninchat/Automation/Python/test.csv
Gathering SGT information from ISE
Gathering policy information from ISE


Finished writing into policy file, stored in path /home/aninchat/Automation/Python/test.csv
```
