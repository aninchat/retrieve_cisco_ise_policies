"""
Date: 06/14/2021
Author: Aninda Chatterjee
Input:
    ISE credentials (username/password and IP address)
    Path to .csv file where data will be stored
Output:
    .csv file where ISE policy data is stored
Usage: This script is designed gather policy information from ISE and store it in a .csv file. 
"""
import rich
import csv
import requests
import warnings
import getpass
import json
from requests.auth import HTTPBasicAuth
from rich.console import Console
from rich.table import Column, Table

def gather_sgt_data_from_ise(ip_address, username, password):
    """function to return a SGT lookup dictionary
    using ISE API
    """

    sgt_dict = {}
    url_for_all_sgts = "https://" + ip_address + ":9060/ers/config/sgt"

    warnings.filterwarnings("ignore")
    try:
        get_sgts = requests.get(url_for_all_sgts, headers={"Content-Type": "application/json", "Accept": "application/json"}, auth=HTTPBasicAuth(username, password), verify=False, timeout=2)
    except:
        rich.print("[red]Authentication failure. Please verify username/password and try again.")
        return

    for sgt in get_sgts.json()['SearchResult']['resources']:
        temp_dict = {}

        # find SGT value now using another API

        url_for_sgt_value = "https://" + ip_address + ":9060/ers/config/sgt/" + sgt['id'] 
        sgt_details_with_value_api = requests.get(url_for_sgt_value, headers={"Content-Type": "application/json", "Accept": "application/json"}, auth=HTTPBasicAuth(username, password), verify=False, timeout=2)

        # assign it all to temp dictionary

        temp_dict = {
                sgt['id']: {
                    'name': sgt['name'], 
                    'description': sgt['description'], 
                    'value': sgt_details_with_value_api.json()['Sgt']['value']
                    }
                }

        # append to main SGT lookup dictionary

        sgt_dict.update(temp_dict)

    return sgt_dict

def create_policy_lookup_dict(ip_address, username, password, sgt_lookup_dict):
    """ function to return a policy lookup dictionary
    containing ISE policies using ISE APIs
    """

    policy_dict = {}

    policy_url = "https://" + ip_address + ":9060/ers/config/egressmatrixcell"
    try:
        policy_url_response = requests.get(policy_url, headers={"Content-Type": "application/json", "Accept": "application/json"}, auth=HTTPBasicAuth(username, password), verify=False)
    except:
        rich.print("[red]Authentication failure. Please verify username/password and try again.")
        return

    policy_list = policy_url_response.json()['SearchResult']['resources']

    # loop through each policy in the policy list 
    # and retrieve the full policy information

    for policy in policy_list:
        temp_dict = {}

        # build detailed policy URL first

        policy_detail_url = "https://" + ip_address + ":9060/ers/config/egressmatrixcell/" + policy['id']
        policy_detail_url_response = requests.get(policy_detail_url, headers={"Content-Type": "application/json", "Accept": "application/json"}, auth=HTTPBasicAuth(username, password), verify=False)

        policy_data = policy_detail_url_response.json()['EgressMatrixCell']

        # from policy data, we need to find out contents of the SGACLs
        # stored inside the policy (since it is stored as an ID)

        sgacl_url = 'https://' + ip_address + ":9060/ers/config/sgacl/" + policy_data['sgacls'][0]
        sgacl_url_response = requests.get(sgacl_url, headers={"Content-Type": "application/json", "Accept": "application/json"}, auth=HTTPBasicAuth(username, password), verify=False)
        sgacl_data = sgacl_url_response.json()['Sgacl']

        # convert source and destination SGT IDs into names
        
        # special case for default policy (any-any) since this is not listed
        # in get-all SGT API and needs to be accounted for separately

        if policy_data['name'] == 'ANY-ANY':
            temp_dict = {
                    policy['id']: {
                        'policy_name': 'ANY-ANY',
                        'source_sgt_name': 'ANY',
                        'dest_sgt_name': 'ANY',
                        'source_sgt_value': '65535',
                        'dest_sgt_value': '65535',
                        'status': policy_data['matrixCellStatus'],
                        'contract_name': sgacl_data['name'],
                        'contract_description': sgacl_data['description'],
                        'aces': sgacl_data['aclcontent']
                        }
                    }
            policy_dict.update(temp_dict)
            continue

        # convert SGT IDs into names

        policy_source_sgt_name = sgt_lookup_dict[policy_data['sourceSgtId']]['name']
        policy_dest_sgt_name = sgt_lookup_dict[policy_data['destinationSgtId']]['name']

        # get SGT numeric values

        policy_source_sgt_value = sgt_lookup_dict[policy_data['sourceSgtId']]['value']
        policy_dest_sgt_value = sgt_lookup_dict[policy_data['destinationSgtId']]['value']

        # build temp_dict with all policy data

        temp_dict = {
                policy['id']: {
            'policy_name': policy_data['name'],
            'source_sgt_name': policy_source_sgt_name, 
            'dest_sgt_name': policy_dest_sgt_name,
            'source_sgt_value': policy_source_sgt_value,
            'dest_sgt_value': policy_dest_sgt_value,
            'status': policy_data['matrixCellStatus'], 
            'contract_name': sgacl_data['name'],
            'contract_description': sgacl_data['description'],
            'aces': sgacl_data['aclcontent']
            }
        }
        policy_dict.update(temp_dict)
    return policy_dict

def print_policies(policy_data):
    table = Table(title="Policy data from ISE", header_style="bold red")
    table.add_column("Policy ID", justify="center")
    table.add_column("Policy Name", justify="center")
    table.add_column("Source SGT Name", justify="center")
    table.add_column("Source SGT Value", justify="center")
    table.add_column("Destination SGT Name", justify="center")
    table.add_column("Destination SGT Value", justify="center")
    table.add_column("Status", justify="center")
    table.add_column("Contract Name", justify="center")
    table.add_column("Contract Description", justify="center")
    table.add_column("ACEs", justify="center")
    console = Console()

    for policy in policy_data:
        table.add_row(policy, policy_data[policy]['policy_name'], policy_data[policy]['source_sgt_name'], str(policy_data[policy]['source_sgt_value']), policy_data[policy]['dest_sgt_name'], str(policy_data[policy]['dest_sgt_value']), policy_data[policy]['status'], policy_data[policy]['contract_name'], policy_data[policy]['contract_description'], policy_data[policy]['aces']) 
    console.print(table)

def main():
    ise_ip_address = input("Please provide the IP address for the ISE PAN: ")
    ise_username = input("Please provide the username for login: ")
    ise_password = getpass.getpass(prompt="Please provide the password for login: ")
    policy_data_file_path = input("Please provide the exact path (with file name) where the policy information will need to be stored: ")

    # create SGT lookup dictionary

    try:
        sgt_lookup_dict = gather_sgt_data_from_ise(ise_ip_address, ise_username, ise_password)
        rich.print("[green]Gathering SGT information from ISE")
    except requests.exceptions.ConnectTimeout:
        rich.print("[red]\nHTTP GET request timed out - please validate the IP address specified and reachability to it")
        return
    except:
        rich.print("[red]\nAuthentication failure. Please retry with correct IP address, username and password")
        return

    # create policy lookup dictionary

    rich.print("[green]Gathering policy information from ISE")
    policy_lookup_dict = create_policy_lookup_dict(ise_ip_address, ise_username, ise_password, sgt_lookup_dict)

    # print rich table of policies

    print_policies(policy_lookup_dict)

    try:
        with open(policy_data_file_path, 'w', encoding='utf-8-sig') as policy_file:
            policy_file_writer = csv.writer(policy_file)
            policy_file_writer.writerow(['Policy ID', 'Policy Name', 'Source SGT Name', 'Source SGT Value', 'Destination SGT Name', 'Destination SGT Value', 'Status', 'Contract Name', 'Contract Description', 'ACEs'])
            for policy in policy_lookup_dict:
                policy_file_writer.writerow([policy, policy_lookup_dict[policy]['policy_name'], policy_lookup_dict[policy]['source_sgt_name'], str(policy_lookup_dict[policy]['source_sgt_value']), policy_lookup_dict[policy]['dest_sgt_name'], str(policy_lookup_dict[policy]['dest_sgt_value']), policy_lookup_dict[policy]['status'], policy_lookup_dict[policy]['contract_name'], policy_lookup_dict[policy]['contract_description'], policy_lookup_dict[policy]['aces']])
            rich.print(f"[green]\nFinished writing into policy file, stored in path {policy_data_file_path}")
    except:
        rich.print("[red]Could not open/write into file. Please check file path and write permissions")

if __name__ == '__main__':
    main()
