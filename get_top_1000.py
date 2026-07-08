import requests

def download_top_1000_domains():
    print("Downloading Top 1000 URLs for FYP...")
    
    # Official Cybersecurity GitHub Repository for Top 1000 Domains
    url = "https://raw.githubusercontent.com/urbanadventurer/WhatWeb/master/plugin-development/alexa-top-1000.txt"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # File mein save karna
            with open("top_websites.txt", "w", encoding="utf-8") as f:
                f.write(response.text)
            print("Success! 'top_websites.txt' successfully ban gayi hai jisme 1000 websites hain.")
        else:
            print("Download failed. Status Code:", response.status_code)
    except Exception as e:
        print("Error:", e)

# Function ko call karein
download_top_1000_domains()