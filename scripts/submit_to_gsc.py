import os
import sys
import time
import xml.etree.ElementTree as ET
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    'https://www.googleapis.com/auth/indexing',
    'https://www.googleapis.com/auth/webmasters.readonly'
]
CLIENT_SECRET_FILE = '/home/gobeam/Downloads/client_secret_1014385004109-fjrjisk5md8idkkilvk43jeh0c64o8q5.apps.googleusercontent.com.json'
TOKEN_FILE = '/home/gobeam/Projects/joyofcare-web/scripts/gsc_token.json'
SITEMAP_FILE = '/home/gobeam/Projects/joyofcare-web/dist/sitemap-0.xml'
SITE_URL = 'https://www.joyofcare.net/' # Ensure trailing slash if needed

def get_urls_from_sitemap(sitemap_path):
    if not os.path.exists(sitemap_path):
        print(f"Error: Sitemap not found at {sitemap_path}")
        return []
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = []
    for url in root.findall('ns:url/ns:loc', namespaces):
        if '/blog/' in url.text:
            urls.append(url.text)
    return urls

def authenticate():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Failed to refresh token: {e}")
                creds = None
        
        if not creds:
            if not sys.stdin.isatty():
                print("Error: Authentication required. Please run this script manually in a terminal to authenticate.")
                sys.exit(1)
            print("Interactive authentication required...")
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0, open_browser=False)
        
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return creds

def check_and_submit(creds, urls):
    searchconsole = build('searchconsole', 'v1', credentials=creds)
    indexing = build('indexing', 'v3', credentials=creds)
    
    # Dynamically find the exact siteUrl registered in GSC
    actual_site_url = SITE_URL
    try:
        sites_response = searchconsole.sites().list().execute()
        site_list = sites_response.get('siteEntry', [])
        found = False
        for site in site_list:
            if 'joyofcare.net' in site.get('siteUrl', ''):
                actual_site_url = site.get('siteUrl')
                print(f"Using verified GSC property: {actual_site_url}")
                found = True
                break
        if not found:
            print(f"Warning: joyofcare.net not found in verified sites. Found: {[s.get('siteUrl') for s in site_list]}")
            print(f"Make sure bimo@bratasena.com has access to the property in Google Search Console.")
            sys.exit(1)
    except Exception as e:
        print(f"Could not list sites: {e}")

    for url in urls:
        print(f"Checking index status for {url}...")
        try:
            request = {
                'siteUrl': actual_site_url,
                'inspectionUrl': url,
                'languageCode': 'id-ID'
            }
            response = searchconsole.urlInspection().index().inspect(body=request).execute()
            status = response.get('inspectionResult', {}).get('indexStatusResult', {}).get('coverageState', '')
            
            # The coverage state could be 'Indexed, not submitted in sitemap', 'Submitted and indexed', etc.
            if 'Indexed' not in status:
                print(f"  URL not indexed ({status}). Submitting to Indexing API...")
                idx_resp = indexing.urlNotifications().publish(
                    body={
                        "url": url,
                        "type": "URL_UPDATED"
                    }
                ).execute()
                print(f"  Submitted successfully.")
            else:
                print(f"  URL is already indexed.")
                
            time.sleep(2) # Basic rate limiting
        except HttpError as e:
            print(f"  API Error for {url}: {e.reason}")
            time.sleep(2)
        except Exception as e:
            print(f"  Unexpected error: {e}")

if __name__ == '__main__':
    print("Extracting blog URLs from sitemap...")
    urls = get_urls_from_sitemap(SITEMAP_FILE)
    print(f"Found {len(urls)} blog URLs.")
    
    if not urls:
        sys.exit(0)
    
    print("Authenticating...")
    creds = authenticate()
    
    print("Checking and submitting URLs...")
    check_and_submit(creds, urls)
