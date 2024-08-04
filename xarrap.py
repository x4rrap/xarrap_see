import requests
from bs4 import BeautifulSoup
import re

print("by hagg4r")
def format_phone_number(phone_number):
    # Format phone number with square brackets
    return f"[{phone_number}]"

def find_accounts(phone_number):
    # Search for accounts connected to the phone number using Google Search
    search_urls = {
        "Telegram": f"https://www.google.com/search?q=telegram+accounts+connected+to+%5B{phone_number}%5D",
        "WhatsApp": f"https://www.google.com/search?q=whatsapp+accounts+connected+to+%5B{phone_number}%5D",
        "Instagram": f"https://www.google.com/search?q=instagram+accounts+connected+to+%5B{phone_number}%5D"
    }

    for platform, search_url in search_urls.items():
        search_response = requests.get(search_url)

        if search_response.status_code == 200:
            print(f"{format_phone_number(phone_number)} Results from Google search on {platform}:")
            soup = BeautifulSoup(search_response.text, 'html.parser')
            results = [result.get_text() for result in soup.find_all('div', {'class': 'yuRUbf'})]
            for result in results:
                print(result)
        else:
            print(f"Failed to fetch search results for {platform}.")

def reverse_phone_lookup(phone_number):
    # Reverse phone number lookup using various websites
    lookup_urls = {
        "Whitepages": f"https://www.whitepages.com/phone/{phone_number}",
        "Intelius": f"https://www.intelius.com/phone/{phone_number}",
        "ZabaSearch": f"https://www.zabasearch.com/people/{phone_number}"
    }

    for platform, lookup_url in lookup_urls.items():
        response = requests.get(lookup_url)

        if response.status_code == 200:
            print(f"{format_phone_number(phone_number)} {platform} results:")
            print(response.text)
        else:
            print(f"Failed to fetch {platform} information.")

def find_name_and_search(phone_number):
    # Use a Google Dork to search for the phone number and name
    dork_url = f"https://www.google.com/search?q=site%3Afacebook.com+%22{phone_number}%22+intitle%3A%22name%22"

    response = requests.get(dork_url)

    if response.status_code == 200:
        print(f"{format_phone_number(phone_number)} Results from Google Dork:")
        soup = BeautifulSoup(response.text, 'html.parser')
        results = [result.get_text() for result in soup.find_all('div', {'class': 'yuRUbf'})]
        for result in results:
            print(result)

            # Extract the name from the search results using regex
            name_match = re.search(r'intitle:"name":(.*?)<', result)
            if name_match:
                extracted_name = name_match.group(1)
                print(f"{format_phone_number(phone_number)} Name found: {extracted_name}")

                # Search for additional information based on the extracted name
                search_url = f"https://www.google.com/search?q={extracted_name}"
                search_response = requests.get(search_url)

                if search_response.status_code == 200:
                    print(f"{format_phone_number(phone_number)} Additional results from Google search:")
                    soup = BeautifulSoup(search_response.text, 'html.parser')
                    results = [result.get_text() for result in soup.find_all('div', {'class': 'yuRUbf'})]
                    for result in results:
                        print(result)
                else:
                    print("Failed to fetch additional search results.")
    else:
        print("Failed to fetch search results.")

def main():
    phone_number = input("Enter the phone number to search: ")

    print("-" * 80)
    print(f"| {format_phone_number(phone_number)} Results |")
    print("-" * 80)

    find_accounts(phone_number)
    reverse_phone_lookup(phone_number)
    find_name_and_search(phone_number)

if __name__ == "__main__":
    main()
