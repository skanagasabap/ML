import json
import requests
from pprint import pprint
import traceback

class SMAXHandler(object):  
    def __init__(self, url, tenent_id, username, password):     
        self.url = url
        self.tenent_id = tenent_id
        self.username = username
        self.password = password
        self.auth_token = None
        self.get_auth_token()

    def _verify_respone(self, response):
        if response.status_code not in [200]: 
            print(traceback.format_exec())           
            raise Exception(response.text)

    def get_auth_token(self):
        auth_url = f'{self.url}/auth/authentication-endpoint/authenticate/login?TENANTID={self.tenent_id}'
        payload = {
            "login": self.username,
            "password": self.password
        }
        payload = json.dumps(payload)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(auth_url, headers=headers, data=payload)
        self._verify_respone(response)        
        self.auth_token = response.text

        

    def create_request(self, offering_id, display_label, user_options):
        api_url = f'{self.url}/rest/{self.tenent_id}/ems/bulk'
        headers = {
            'Cookie': f'LWSSO_COOKIE_KEY={self.auth_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }        

        payload = {
            "entities": [
                {
                    "entity_type": "Request",
                    "properties": {
                        "RequestsOffering": offering_id,
                        "DisplayLabel": display_label,                        
                        "UserOptions": f'{{"complexTypeProperties":[{{"properties": { json.dumps(user_options) } }}]}}'
                    }
                }
            ],
            "operation": "CREATE"
        }
        payload = json.dumps(payload)
        response = requests.post(api_url, headers=headers, data=payload)
        self._verify_respone(response)
        return response.text
        
    def get_offering_details(self, id):
        """
        returns offering details based on id
        """
        api_end_point = f'{self.url}/rest/{self.tenent_id}/ess/catalog/offeringWithBundles/{id}'
        headers = {
            'Cookie': f'LWSSO_COOKIE_KEY={self.auth_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = requests.get(api_end_point, headers=headers)
        self._verify_respone(response)
        data = response.json()
        display_label = data.get("offering").get("properties").get("DisplayLabel")
        user_option = data.get("offering").get("properties").get("UserOptionsName")

        user_inputs = self.get_user_options(user_option)
        mandatory_inputs = self.get_mandatory_inputs(id)

        return dict(
                display_label=display_label,
                user_inputs=user_inputs,
                mandatory_inputs=mandatory_inputs,
                offering_type=data.get("offering").get("properties").get("OfferingType")
            )

    def get_user_options(self, user_option):
        api_end_point = f'{self.url}/rest/{self.tenent_id}/user-options/full/{user_option}'
        headers = {
            'Cookie': f'LWSSO_COOKIE_KEY={self.auth_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        response = requests.get(api_end_point, headers=headers)
        self._verify_respone(response)
        # pprint(response.json())
        user_options = {}
        labels = response.json().get("localizedLabels")
        for option in response.json().get('userOptionsDescriptor').get('userOptionsPropertyDescriptors'):
            if option.get("visibility"):
                user_options[option['name']] = {
                    "type": option['editorType'],
                    "display_label": labels.get(option['localized_label_key'])
                } 

        # pprint(user_options)
        return user_options

    def get_mandatory_inputs(self, id):
        api_end_point = f'{self.url}/rest/{self.tenent_id}/ess/workflow/simulator/Request'
        headers = {
            'Cookie': f'LWSSO_COOKIE_KEY={self.auth_token}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        payload = {
            "NewEntity": {
                "entity_type": "Request",
                "properties": {            
                    "RequestsOffering": id
                }
            }
        }
        payload = json.dumps(payload)

        response = requests.post(api_end_point, headers=headers, data=payload)
        # self._verify_respone(response)
        # pprint(response.json())
        mandatory_inputs = []        

        # pprint(response.json())
        return response.json().get('MandatoryFields')


   

# ================================= NOTES =================================
# UserOptions='{"complexTypeProperties":[{"properties":{"PrintName_c":"test","PrintProblem_c":"OutOfInk_c"}}]}'

# sample payload
        # payload = {
  #         "entities": [
  #             {
  #                 "entity_type": "Request",
  #                 "properties": {
  #                     "RequestedForPerson": "18838",
  #                     "StartDate": 1618987325463,
  #                     "RequestsOffering": "12601",
  #                     "CreationSource": "CreationSourceEss",
  #                     "RequestedByPerson": "18838",
  #                     "DataDomains": [
  #                         "Public"
  #                     ],
  #                     "CreateTime": 1618987325809,
  #                     "Description": "<p>testing 2 for chatbot</p>",
  #                     "UserOptions": "{\"complexTypeProperties\":[{\"properties\":{}}]}",
  #                     "DisplayLabel": "Employee on boarding"
  #                 }
  #             }
  #              ],
  #         "operation": "CREATE"
        # }
