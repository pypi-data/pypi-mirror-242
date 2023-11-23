import requests
from requests.exceptions import HTTPError

class WebhookSite:
    def delete_all_requests_of_a_token(self, tokenId):
        url = 'https://webhook.site/token/'+tokenId+'/request'
        try:
            response = requests.delete(url)
        except HTTPError as http_err:
            print(f'HTTP error occureed: {http_err}')    
        else:
            return response.status_code

    def get_latest_request_raw_content(self, tokenId):
        url = 'https://webhook.site/token/'+tokenId+'/request/latest/raw'
        print(url)
        try:
            response = requests.get(url)
        except HTTPError as http_err:
            print(f'HTTP error occurred:{http_err}')
        else:
            if response.status_code == 200:
                return response.json()




