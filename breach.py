import hashlib
import requests #for communication with api

def check_breach(password):
    
    if not password:
        return 0

    # 1. Password  SHA-1 hash 
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1_password[:5] # k-anonymity model rule 
    suffix = sha1_password[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return 0
            
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return int(count) 
                
    except Exception as e:
        print(f"Connection Error: {e}")
        return 0
        
    return 0