import requests
import json
import csv
from time import sleep
import os

def search_chrome_store(query, language="en", country="US"):
    url = f"https://chrome.google.com/webstore/ajax/item"
    params = {
        "hl": language,
        "gl": country,
        "pv": "20210820",
        "mce": "atf,pii,rtr,rlb,gtc,hcn,svp,wtd,hap,nma,dpb,utb,hbh,ebo,hqb,ifm,ndd,ntd,oi,spd,ctm,ac,hot,hfi,dtp,mac,bga,fcf,rma",
        "count": 100,
        "searchTerm": query,
        "category": "extensions"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Accept": "*/*",
        "Accept-Language": f"{language}-{country},{language};q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    response = requests.post(url, params=params, headers=headers)
    if response.status_code == 200:
        
        json_str = response.text[5:]  
        try:
            data = json.loads(json_str)
            if len(data) > 1 and isinstance(data[1], list):
                return data[1][1]  
        except Exception as e:
            print(f"JSON parsing error: {e}")
    return []

def get_vpn_extensions():
    print("Searching for VPN extensions in both Turkish and English...")
    extensions = []
    
   
    search_terms = ["vpn", "proxy"]
    
    
    languages = [
        {"lang": "en", "country": "US"},
        {"lang": "tr", "country": "TR"}
    ]
    
    for lang in languages:
        print(f"\nSearching in {lang['lang']} language...")
        for term in search_terms:
            print(f"Searching for '{term}'...")
            results = search_chrome_store(term, lang["lang"], lang["country"])
            for item in results:
                try:
                    extension_id = item[0]  # Extension ID
                    name = item[1]  # Extension name
                    
                    
                    if isinstance(name, str):
                       
                        if '\\u' in name:
                            
                            name = bytes(name, 'utf-8').decode('unicode_escape')
                    
                    if extension_id and name:
                        extensions.append({
                            'id': extension_id,
                            'name': name,
                            'language': lang['lang']
                        })
                except Exception as e:
                    print(f"Error: {e}")
                    continue
            
            print(f"Number of extensions found so far: {len(extensions)}")
            sleep(1)  
    
    # Clean up duplicate extensions
    unique_extensions = []
    seen_ids = set()
    for ext in extensions:
        if ext['id'] not in seen_ids:
            seen_ids.add(ext['id'])
            unique_extensions.append(ext)
    
    return unique_extensions

def get_csv_save_location():
 
    possible_locations = [
      
        os.getcwd(),
       
        os.path.join(os.path.expanduser("~"), "Documents"),
     
        r"C:\Users\Public\Documents"
    ]
    
    
    save_dir = None
    for location in possible_locations:
        if os.path.exists(location) and os.access(location, os.W_OK):
            save_dir = location
            break
    

    if not save_dir:
        save_dir = os.getcwd()
    
    default_location = os.path.join(save_dir, 'vpn_extensions.csv')
    
    print("\nAvailable save locations:")
    for i, loc in enumerate(possible_locations, 1):
        if os.path.exists(loc):
            status = "exists, writable" if os.access(loc, os.W_OK) else "exists, not writable"
        else:
            status = "does not exist"
        print(f"{i}. {loc} ({status})")
    
    print(f"\nDefault save location: {default_location}")
    custom_location = input("Enter a custom save location or press Enter to use the default: ")
    
    if custom_location.strip():
       
        directory = os.path.dirname(custom_location)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"Created directory: {directory}")
            except Exception as e:
                print(f"Error creating directory: {e}")
                print("Using default location instead.")
                return default_location
        return custom_location
    
    return default_location

def save_to_csv(extensions, csv_path):
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'name', 'language']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for extension in extensions:
                writer.writerow(extension)
        return True
    except Exception as e:
        print(f"Error saving CSV file: {e}")
        return False

def main():
    extensions = get_vpn_extensions()
    print(f"\nTotal {len(extensions)} VPN extensions found.")
    
    csv_path = get_csv_save_location()
    
    if save_to_csv(extensions, csv_path):
        print(f"Data saved to {csv_path}")
        
        # Open CSV file for verification
        print("\nFirst 5 lines of saved data:")
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f):
                    if i > 5:
                        break
                    print(line.strip())
        except Exception as e:
            print(f"File reading error: {e}")
    else:
        print("Failed to save data.")

if __name__ == "__main__":
    main()