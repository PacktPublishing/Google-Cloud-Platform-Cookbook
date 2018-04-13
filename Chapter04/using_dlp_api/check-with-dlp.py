# -*- coding: utf-8 -*-
"""
@author: Legorie
# The code identifies sensitive information and logs it on the console
"""
import json
import requests

# Enter the API Key which has access to the DLP API
api_key = "<Enter API Key>"

# Functions returns true if the likelihood is acceptable
def verify_likelihood(match):
    if match in ['POSSIBLE','LIKELY','VERY_LIKELY']:
        return 1
    else:
        return 0

# 1) Reads the file line by line
# 2) Generates the JSON and calls the DLP API
# 3) If the results is returned and with an acceptable likelihood, it logs a message
def main():
    data = {}
    line_num = 0
    with open('data.csv') as txtfile:
        for line in txtfile:
            #print(line)
            line_num+=1
            data['item'] = {}
            data['item']['type'] = 'text/plain'
            data['item']['value'] = line
            
            data['inspectConfig'] = {}
            data['inspectConfig']['infoTypes'] = []
    
            pNum = {}
            pNum['name'] = 'PHONE_NUMBER'
    
            data['inspectConfig']['infoTypes'].append(pNum)
            
            eMail = {}
            eMail['name'] = 'EMAIL_ADDRESS'
            
            data['inspectConfig']['infoTypes'].append(eMail)
                        
            json_data = json.dumps(data)
            #print(json_data)
            
            r = requests.post('https://dlp.googleapis.com/v2beta2/projects/<Project ID>/content:inspect?key=' + api_key, data=json_data)
            #print(r.status_code)
            response = r.json()
            #print(response)
            
            if 'findings' in response['result']:
                if len(response['result']['findings']) == 2 and \
                    verify_likelihood(response['result']['findings'][0]['likelihood']) and \
                    verify_likelihood(response['result']['findings'][1]['likelihood']):
                #if response['result']['findings']['infoType']['name'] == 'PHONE_NUMBER':
                    print("Phone number and Email address are present in line #" + str(line_num))
                elif response['result']['findings'][0]['infoType']['name'] == 'PHONE_NUMBER' and \
                     verify_likelihood(response['result']['findings'][0]['likelihood']):
                    print("Phone number is present in line #" + str(line_num))
                elif response['result']['findings'][0]['infoType']['name'] == 'EMAIL_ADDRESS' and \
                     verify_likelihood(response['result']['findings'][0]['likelihood']):
                    print("Email address is present in line #" + str(line_num))

if __name__ == "__main__":
    main()
