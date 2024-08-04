import requests

def format_phone_number(phone_number):
    return f"[{phone_number}]"

def find_accounts(phone_number):
    # Search for accounts connected to the phone number using a search engine
    search_urls = [
        (f"https://www.google.com/search?q=telegram+accounts+connected+to+%5B{phone_number}%5D", "Telegram"),
        (f"https://www.google.com/search?q=watsapp+accounts+connected+to+%5B{phone_number}%5D", "WhatsApp"),
        (f"https://www.google.com/search?q=instagram+accounts+connected+to+%5B{phone_number}%5D", "Instagram")
    ]

    for search_url, platform in search_urls:
        search_response = requests.get(search_url)

        if search_response.status_code == 200:
            print(f"{format_phone_number(phone_number)} Results from Google search on {platform}:")
            print(search_response.text)
        else:
            print(f"Failed to fetch search results for {platform}.")

def reverse_phone_lookup(phone_number):
    # Whitepages.com lookup
    whitepages_url = f"https://www.whitepages.com/phone/{phone_number}"
    whitepages_response = requests.get(whitepages_url)

    if whitepages_response.status_code == 200:
        print(f"{format_phone_number(phone_number)} {whitepages_response.text}")
    else:
        print("Failed to fetch Whitepages information.")

    # Intelius.com lookup
    intelius_url = f"https://www.intelius.com/phone/{phone_number}"
    intelius_response = requests.get(intelius_url)

    if intelius_response.status_code == 200:
        print(f"{format_phone_number(phone_number)} {intelius_response.text}")
    else:
        print("Failed to fetch Intelius information.")

    # ZabaSearch.com lookup
    zabasearch_url = f"https://www.zabasearch.com/people/{phone_number}"
    zabasearch_response = requests.get(zabasearch_url)

    if zabasearch_response.status_code == 200:
        print(f"{format_phone_number(phone_number)} {zabasearch_response.text}")
    else:
        print("Failed to fetch ZabaSearch information.")

def find_name_and_search(phone_number):
    # Use a Google Dork to search for the phone number and name
    dork_url = f"https://www.google.com/search?q=site%3Afacebook.com+%22{phone_number}%22+intitle%3A%22{name%22"
    
    # Make an HTTP request to the URL
    response = requests.get(dork_url)

    if response.status_code == 200:
        print(f"{format_phone_number(phone_number)} Results from Google Dork:")
        print(response.text)
        
        # Extract the name from the search results
        for line in response.text.splitlines():
            if "name" in line.lower() and "<b>" in line:
                extracted_name = line.split("<b>").split("</b>")
                print(f"{format_phone_number(phone_number)} Name found: {extracted_name}")

        # Search for additional information based on the extracted name
        if extracted_name:
            search_url = f"https://www.google.com/search?q={extracted_name}"
            search_response = requests.get(search_url)

            if search_response.status_code == 200:
                print(f"{format_phone_number(phone_number)} Additional results from Google search:")
                print(search_response.text)
            else:
                print("Failed to fetch additional search results.")
    else:
        print("Failed to fetch search results.")

def main():
    phone_number = input("Inserisci il numero di telefono da cercare: ")

    # Print a rectangular frame for the results
    print("-" * 80)
    print(f"| {format_phone_number(phone_number)} Results |")
    print("-" * 80)

    find_accounts(phone_number)
    reverse_phone_lookup(phone_number)
    find_name_and_search(phone_number)

if __name__ == "__main__":
    main()
