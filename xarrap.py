import requests
from bs4 import BeautifulSoup
import re

print("by hagg4r")
def formatta_numero_telefono(numero_telefono):
    """Formatta il numero di telefono con le parentesi quadre."""
    return f"[{numero_telefono}]"

def cerca_accounts(numero_telefono):
    """Cerca account collegati al numero di telefono utilizzando Google Search."""
    url_ricerca = {
        "Telegram": f"https://www.google.com/search?q=telegram+account+collegati+a+%5B{numero_telefono}%5D",
        "WhatsApp": f"https://www.google.com/search?q=whatsapp+account+collegati+a+%5B{numero_telefono}%5D",
        "Instagram": f"https://www.google.com/search?q=instagram+account+collegati+a+%5B{numero_telefono}%5D",
        "Facebook": f"https://www.google.com/search?q=facebook+account+collegati+a+%5B{numero_telefono}%5D"
    }

    for piattaforma, url in url_ricerca.items():
        risposta = requests.get(url)

        if risposta.status_code == 200:
            print(f"\nRisultati della ricerca su {piattaforma} per il numero {formatta_numero_telefono(numero_telefono)}:")
            soup = BeautifulSoup(risposta.text, 'html.parser')
            risultati = soup.find_all('div', {'class': 'yuRUbf'})

            for risultato in risultati:
                testo = risultato.get_text().strip()
                link = risultato.find('a')['href']

                # Costruisce i link di WhatsApp e Telegram utilizzando il numero di telefono trovato nei risultati della ricerca
                if piattaforma == "WhatsApp" and "+" in testo:
                    link_whatsapp = f"https://api.whatsapp.com/send/?phone={testo.replace('+', '')}&text=&type=phone_number&app_absent=0"
                    print(f"[ {testo} ]({link_whatsapp})")
                elif piattaforma == "Telegram" and "+" in testo:
                    link_telegram = f"https://t.me/{testo.replace('+', '')}"
                    print(f"[ {testo} ]({link_telegram})")
                elif piattaforma in ["Instagram", "Facebook"] and "+" in testo:
                    link_placeholder = f"https://www.{piattaforma}.com/?hl=en&query={testo.replace('+', '')}"
                    print(f"[ {testo} ]({link_placeholder})")
                else:
                    print(f"[ {testo} ]({link})")
        else:
            print(f"Impossibile recuperare i risultati della ricerca per {piattaforma}.")

def ricerca_inverso_numero_telefono(numero_telefono):
    """Ricerca inversa del numero di telefono utilizzando vari siti web."""
    url_ricerca = {
        "Whitepages": f"https://www.whitepages.com/phone/{numero_telefono}",
        "Intelius": f"https://www.intelius.com/phone/{numero_telefono}",
        "ZabaSearch": f"https://www.zabasearch.com/people/{numero_telefono}"
    }

    for piattaforma, url in url_ricerca.items():
        risposta = requests.get(url)

        if risposta.status_code == 200:
            print(f"\nRisultati della ricerca inversa per il numero {formatta_numero_telefono(numero_telefono)} su {piattaforma}:")
            soup = BeautifulSoup(risposta.text, 'html.parser')
            print(soup.prettify())
        else:
            print(f"Impossibile recuperare le informazioni da {piattaforma}.")

def cerca_nome_e_cognome(numero_telefono):
    """Utilizza un Google Dork per cercare il numero di telefono e il nome."""
    url_dork = f"https://www.google.com/search?q=site%3Afacebook.com+%22{numero_telefono}%22+intitle%3A%22nome+cognome%22"

    risposta = requests.get(url_dork)

    if risposta.status_code == 200:
        print(f"\nRisultati del Google Dork per il numero {formatta_numero_telefono(numero_telefono)}:")
        soup = BeautifulSoup(risposta.text, 'html.parser')
        risultati = soup.find_all('div', {'class': 'yuRrisultati:

        for risultato in risultati:
            testo = risultato.get_text().strip()
            link = risultato.find('a')['href']
            print(f"[ {testo} ]({link})")

            corrispondenza_nome = re.search(r'intitle:"nome+cognome":(.*?)<', testo)
            if corrispondenza_nome:
                nome_estratto = corrispondenza_nome.group(1)
                print(f"\nNome e cognome trovati per il numero {formatta_numero_telefono(numero_telefono)}: {nome_estratto}")

                url_ricerca = f"https://www.google.com/search?q={nome_estratto}"
                risposta_ricerca = requests.get(url_ricerca)

                if risposta_ricerca.status_code == 200:
                    print(f"\nRisultati aggiuntivi della ricerca su Google per il nome {nome_estratto}:")
                    soup = BeautifulSoup(risposta_ricerca.text, 'html.parser')
                    risultati = soup.find_all('div', {'class': 'yuRUbf'})

                    for risultato in risultati:
                        testo = risultato.get_text().strip()
                        link = risultato.find('a')['href']
                        print(f"[ {testo} ]({link})")

                        # Estrae il nome utente, il nome e il cognome dal link del profilo di Instagram o Facebook
                        if "instagram.com" in link or "facebook.com" in link:
                            profilo = link.split("/")[-1]
                            nome_utente = profilo.split("?")[0]
                            nome_cognome = testo.split(" - ")[-1].split(" · ")[0]
                            print(f"Nome utente: {nome_utente}, Nome e cognome: {nome_cognome}")
                else:
                    print("Impossibile recuperare i risultati della ricerca aggiuntivi.")
    else:
        print("Impossibile recuperare i risultati della ricerca.")

def main():
    numero_telefono = input("Inserisci il numero di telefono da cercare: ")

    print("\n" + "-" * 80)
    print(f"| Risultati per il numero {formatta_numero_telefono(numero_telefono)} |")
    print("-" * 80)

    cerca_accounts(numero_telefono)
    ricerca_inverso_numero_telefono(numero_telefono)
    cerca_nome_e_cognome(numero_telefono)

if __name__ == "__main__":
    main()
