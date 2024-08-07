import requests
from bs4 import BeautifulSoup
import re

def formatta_numero_telefono(numero_telefono):
    """Formatta il numero di telefono con le parentesi quadre."""
    return f"[{numero_telefono}]"

def cerca_accounts(numero_telefono):
    """Cerca account collegati al numero di telefono utilizzando Google Search."""
    url_ricerca = {
        "Telegram": f"https://www.google.com/search?q=telegram+account+collegati+a+{formatta_numero_telefono(numero_telefono)}",
        "WhatsApp": f"https://www.google.com/search?q=whatsapp+account+collegati+a+{formatta_numero_telefono(numero_telefono)}",
        "Instagram": f"https://www.google.com/search?q=instagram+account+collegati+a+{formatta_numero_telefono(numero_telefono)}",
        "Facebook": f"https://www.google.com/search?q=facebook+account+collegati+a+{formatta_numero_telefono(numero_telefono)}"
    }

    for piattaforma, url in url_ricerca.items():
        risposta = requests.get(url)

        if risposta.status_code == 200:
            print(f"\n{'-' * 40}\nRisultati della ricerca su {piattaforma} per il numero {formatta_numero_telefono(numero_telefono)}:\n{'-' * 40}")
            soup = BeautifulSoup(risposta.text, 'html.parser')
            risultati = soup.find_all('div', {'class': re.compile('yuRUbf')})

            for risultato in risultati:
                testo = risultato.get_text().strip()
                link = risultato.find('a')['href']
                print(f"[ {testo} ]({link})")
        else:
            print(f"Impossibile recuperare i risultati della ricerca per {piattaforma}.")

def ricerca_inverso_numero_telefono(numero_telefono):
    """Ricerca inversa del numero di telefono utilizzando vari siti web."""
    url_ricerca = {
        "Whitepages": f"https://www.whitepages.com/phone/{numero_telefono}",
        "Intelius": f"https://www.intelius.com/phone/{numero_telefono}",
        "ZabaSearch": f"https://www.zabasearch.com/people/{numero_telefono}",
        "Spokeo": f"https://www.spokeo.com/phone-lookup/{numero_telefono}",
        "Truecaller": f"https://www.truecaller.com/search/it/{numero_telefono}"
    }

    for piattaforma, url in url_ricerca.items():
        risposta = requests.get(url)

        if risposta.status_code == 200:
            print(f"\n{'-' * 40}\nRisultati della ricerca inversa per il numero {formatta_numero_telefono(numero_telefono)} su {piattaforma}:\n{'-' * 40}")
            soup = BeautifulSoup(risposta.text, 'html.parser')
            print(soup.prettify())
        else:
            print(f"Impossibile recuperare le informazioni da {piattaforma}.")

def cerca_nome_e_cognome(numero_telefono):
    """Utilizza un Google Dork per cercare il numero di telefono e il nome."""
    url_dork = f"https://www.google.com/search?q=site:facebook.com+%22{numero_telefono}%22+intitle:%22nome+cognome%22"

    risposta = requests.get(url_dork)

    if risposta.status_code == 200:
        print(f"\n{'-' * 40}\nRisultati del Google Dork per il numero {formatta_numero_telefono(numero_telefono)}:\n{'-' * 40}")
        soup = BeautifulSoup(risposta.text, 'html.parser')
        risultati = soup.find_all('div', {'class': re.compile('yuRUbf')})

        for risultato in risultati:
            testo = risultato.get_text().strip()
            link = risultato.find('a')['href']
            print(f"[ {testo} ]({link})")

            # Estrae il prefisso del numero di telefono per capire in che area geografica si trova
            prefisso = numero_telefono[:5]
            citta = None
            if prefisso in ["+3906", "+39351"]:
                citta = "Roma"
            elif prefisso in ["+3902", "+39346", "+39347"]:
                citta = "Milano"
            # Aggiungi qui altri prefissi e città se necessario

            if citta:
                print(f"\nIl prefisso {prefisso} indica che il numero potrebbe essere registrato a {citta}.")

                # Esegue una ricerca inversa del nome e cognome nella città specifica
                url_ricerca_citta = f"https://www.google.com/search?q={testo}+{citta}"
                risposta_ricerca_citta = requests.get(url_ricerca_citta)

                if risposta_ricerca_citta.status_code == 200:
                    print(f"\nRisultati della ricerca inversa del nome e cognome nella città di {citta}:")
                    soup_citta = BeautifulSoup(risposta_ricerca_citta.text, 'html.parser')
                    risultati_citta = soup_citta.find_all('div', {'class': re.compile('yuRUbf')})

                    for risultato_citta in risultati_citta:
                        testo_citta = risultato_citta.get_text().strip()
                        link_citta = risultato_citta.find('a')['href']
                        print(f"[ {testo_citta} ]({link_citta})")
                else:
                    print("Impossibile recuperare i risultati della ricerca inversa del nome e cognome nella città specifica.")
            else:
                print("Impossibile determinare la città associata al prefisso del numero di telefono.")

    else:
        print("Impossibile recuperare i risultati della ricerca.")

def main():
    numero_telefono = input("Inserisci il numero di telefono con prefisso (es. +393491234567): ")

    # Validazione del numero di telefono
    pattern = re.compile(r'^\+39\d{10}$')
    if not pattern.match(numero_telefono):
        print("Il numero di telefono inserito non è valido. Assicurati di inserire un numero di telefono italiano con il prefisso +39.")
        return

    print("\n" + "-" * 80)
    print(f"| Risultati per il numero {formatta_numero_telefono(numero_telefono)} |")
    print("-" * 80)

    cerca_accounts(numero_telefono)
    ricerca_inverso_numero_telefono(numero_telefono)
    cerca_nome_e_cognome(numero_telefono)

if __name__ == "__main__":
    main()
