import requests
from bs4 import BeautifulSoup
import re

def formatta_numero_telefono(numero_telefono):
    """Formatta il numero di telefono con le parentesi quadre."""
    return f"[{numero_telefono}]"

def cerca_su_epios(numero_telefono):
    """Cerca il nome collegato al numero di telefono su epios.com."""
    url = f"https://www.epios.com/search?q={numero_telefono}"
    
    try:
        risposta = requests.get(url)
        risposta.raise_for_status()

        soup = BeautifulSoup(risposta.text, 'html.parser')
        
        # Estrarre il nome dalla pagina di epios
        nome = None
        nome_tag = soup.find('div', class_='nome-classe')  # Verificare l'elemento che contiene il nome
        if nome_tag:
            nome = nome_tag.get_text().strip()
            print(f"Nome trovato su Epios: {nome}")
        else:
            print("Nessun nome trovato su Epios per questo numero.")
        
        return nome
    except requests.exceptions.RequestException as e:
        print(f"Errore durante la ricerca su Epios: {e}")
        return None

def cerca_nome_e_cognome(numero_telefono, nome):
    """Utilizza un Google Dork per cercare il nome e il cognome associato al numero di telefono."""
    if nome:
        url_dork = f"https://www.google.com/search?q=site:facebook.com+%22{nome}%22+intitle:%22nome+cognome%22"
    else:
        url_dork = f"https://www.google.com/search?q=site:facebook.com+%22{numero_telefono}%22+intitle:%22nome+cognome%22"

    try:
        risposta = requests.get(url_dork)
        risposta.raise_for_status()

        print(f"\n{'-' * 40}\nRisultati del Google Dork per il numero {formatta_numero_telefono(numero_telefono)}:\n{'-' * 40}")
        soup = BeautifulSoup(risposta.text, 'html.parser')
        risultati = soup.find_all('a')

        for risultato in risultati:
            link = risultato['href']
            testo = risultato.get_text().strip()
            if testo:  # Mostra solo risultati con testo
                print(f"{testo}: {link}")

    except requests.exceptions.RequestException as e:
        print(f"Impossibile recuperare i risultati della ricerca. Errore: {e}")

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

    # Cerca il nome su epios.com
    nome = cerca_su_epios(numero_telefono)
    
    # Cerca ulteriori informazioni usando Google Dork
    cerca_nome_e_cognome(numero_telefono, nome)

if __name__ == "__main__":
    main()
