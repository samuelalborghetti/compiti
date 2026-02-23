import requests

BASE_URL = "https://fakeapi.net"


def recupera_categorie():
    risposta = requests.get(f"{BASE_URL}/products/categories")
    return risposta


def recupera_prodotti_per_categoria(categoria):
    risposta = requests.get(f"{BASE_URL}/products/category/{categoria}")
    return risposta


def recupera_dettaglio_prodotto(id_prodotto):
    risposta = requests.get(f"{BASE_URL}/products/{id_prodotto}")
    return risposta

def mostra_categorie(categorie):
    print("-" * 15)
    print("         CATEGORIE DISPONIBILI")
    print("-" * 15)
    for i, categoria in enumerate(categorie, start=1):
        print(f"  {i} - {categoria}")
    print("-" * 15)


def mostra_prodotti(prodotti, categoria):
    print(f"Prodotti nella categoria: '{categoria}'")
    print("-" * 20)
    print(f"  {'ID':<6} {'NOME':<35} {'PREZZO':>8}")
    print("-" * 20)
    for prodotto in prodotti:
        pid    = prodotto.get("id", "N/D")
        nome   = str(prodotto.get("title", "N/D"))[:33]
        prezzo = prodotto.get("price", 0)
        print(f"  {pid:<6} {nome:<35} €{prezzo:>7.2f}")
    print("-" * 20)


def mostra_dettaglio_prodotto(prodotto):
    print("-" * 20)
    print("DETTAGLIO PRODOTTO")
    print("-" * 20)
    print(f"  ID : {prodotto.get('id', 'N/D')}")
    print(f"  Nome  : {prodotto.get('title', 'N/D')}")
    print(f"  Prezzo: €{prodotto.get('price', 0):.2f}")
    print(f"  Categoria : {prodotto.get('category', 'N/D')}")
    print(f"  Brand: {prodotto.get('brand', 'N/D')}")
    print(f"  Descrizione : {prodotto.get('description', 'N/D')}")
    print("-" * 20)


def mostra_menu_principale():
    print("-" * 15)
    print("            MENU PRINCIPALE")
    print("-" * 15)
    print("  1 - Scegli una categoria")
    print("  0 - Esci dal programma")
    print("-" * 15)


def mostra_menu_prodotti():
    print("-" * 15)
    print("             MENU PRODOTTI")
    print("-" * 15)
    print("  1 - Visualizza dettaglio di un prodotto")
    print("  2 - Torna alla scelta delle categorie")
    print("  0 - Esci dal programma")
    print("-" * 15)


def chiedi_numero_valido(messaggio, minimo, massimo):
    numero    = 0
    numero_ok = False
    ripeti    = True
    while ripeti:
        testo = input(messaggio).strip()
        try:
            numero    = int(testo)
            numero_ok = True
        except:
            print(" Inserisci un numero intero valido.")
            numero_ok = False
        if numero_ok and (numero < minimo or numero > massimo):
            print(f" Inserisci un numero tra {minimo} e {massimo}.")
            numero_ok = False
        if numero_ok:
            ripeti = False
    return numero


def chiedi_nome_prodotto(mappa_nome_id):
    id_scelto   = 0
    ripeti = True
    nomi_validi = set(mappa_nome_id.keys())
    
    while ripeti:
        testo     = input("Inserisci il nome del prodotto da visualizzare: ").strip()
        if testo in nomi_validi:
            id_scelto = mappa_nome_id[testo]
            ripeti = False
        else:
            
            trovato = False
            for nome in nomi_validi:
                if testo.lower() in nome.lower():
                    id_scelto = mappa_nome_id[nome]
                    trovato = True
                    ripeti = False
                    break
            if not trovato:
                print(" Nome non trovato. Riprova.")
    return id_scelto


print("🛒  Benvenuto nel catalogo prodotti!")

categorie = []
prodotti  = []
categoria = ""
uscita    = False

ripeti_principale = True
while ripeti_principale:

    mostra_menu_principale()
    scelta_principale = chiedi_numero_valido("La tua scelta: ", 0, 1)

    if scelta_principale == 0:
        ripeti_principale = False
        uscita            = True

    elif scelta_principale == 1:

        risposta_categorie = recupera_categorie()

        if risposta_categorie.status_code == 200:
            categorie = risposta_categorie.json()
            mostra_categorie(categorie)
            indice    = chiedi_numero_valido("Inserisci il numero della categoria: ", 1, len(categorie))
            categoria = categorie[indice - 1]
        else:
            print(f"Errore nel recupero delle categorie. Codice: {risposta_categorie.status_code}")
            categoria = ""

        if categoria != "":

            risposta_prodotti = recupera_prodotti_per_categoria(categoria)

            if risposta_prodotti.status_code == 200:
                dati_prodotti = risposta_prodotti.json()
                prodotti = dati_prodotti.get("data", [])
            else:
                print(f"Errore nel recupero dei prodotti. Codice: {risposta_prodotti.status_code}")
                prodotti = []

            if len(prodotti) == 0:
                print("Nessun prodotto trovato in questa categoria.")

            elif len(prodotti) > 0:
                mostra_prodotti(prodotti, categoria)

                ripeti_prodotti = True
                while ripeti_prodotti:

                    mostra_menu_prodotti()
                    scelta_prodotti = chiedi_numero_valido("La tua scelta: ", 0, 2)

                    if scelta_prodotti == 0:
                        ripeti_prodotti   = False
                        ripeti_principale = False
                        uscita            = True

                    elif scelta_prodotti == 1:
                        mappa_nome_id     = {p.get("title"): p.get("id") for p in prodotti}
                        id_scelto         = chiedi_nome_prodotto(mappa_nome_id)
                        risposta_dettaglio = recupera_dettaglio_prodotto(id_scelto)

                        if risposta_dettaglio.status_code == 200:
                            dati_dettaglio = risposta_dettaglio.json()
                            prodotto_dettaglio = dati_dettaglio.get("data", dati_dettaglio)
                            mostra_dettaglio_prodotto(prodotto_dettaglio)
                        else:
                            print(f"Errore nel recupero del dettaglio. Codice: {risposta_dettaglio.status_code}")

                    elif scelta_prodotti == 2:
                        ripeti_prodotti = False

if uscita:
    print("Arrivederci!")