import requests
import re
import json
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_token(session):
    url = 'https://api.gofile.io/accounts'
    response = session.post(url)
    
    if response.status_code == 200:
        try:
            data = response.json()
            token = data.get('data', {}).get('token', '')
            if token:
                logging.info("Token fetched successfully.")
                return token
            else:
                logging.error("Token not found in response.")
                return None
        except json.JSONDecodeError:
            logging.error("Error decoding JSON response.")
            return None
    else:
        logging.error(f"Failed to fetch token, status code: {response.status_code}")
        return None

def get_gofile_links(session, gofile_url, token):
    gofile_id = gofile_url.split('/')[-1].split('?')[0]
    
    content_url = f'https://api.gofile.io/contents/{gofile_id}?wt=4fd6sg89d7s6&contentFilter=&page=1&pageSize=1000&sortField=createTime&sortDirection=-1'
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    response = session.get(content_url, headers=headers)
    
    if response.status_code == 200:
        links = re.findall(r'"link":"(https?://[^\"]+)"', response.text)
        
        if links:
            logging.info(f"Found {len(links)} links.")
            for link in links:
                print(f"{link}\n")
        else:
            logging.warning("No links found in the response.")
    else:
        logging.error(f"Failed to fetch content, status code: {response.status_code}")

def main():
    parser = argparse.ArgumentParser(description="Fetch GoFile direct download links.")
    parser.add_argument('gofile_url', help="The GoFile URL to fetch links from")
    
    args = parser.parse_args()
    
    with requests.Session() as session:
        token = get_token(session)
        if not token:
            logging.error("Unable to fetch token, exiting.")
            return

        get_gofile_links(session, args.gofile_url, token)

if __name__ == '__main__':
    main()
