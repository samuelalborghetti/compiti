from termcolor import colored
import os

FILE_FILM = "film.txt"


def carica_film():
    if os.path.exists(FILE_FILM):
        with open(FILE_FILM, "r", encoding="utf-8") as f:
            return [riga.strip() for riga in f.readlines() if riga.strip() != ""]
    return []


def salva_film(film):
    with open(FILE_FILM, "w", encoding="utf-8") as f:
        for nome in film:
            f.write(nome + "\n")


def visualizza_film(film):
    if len(film) == 0:
        print(colored("Nessun film in collezione.", "yellow"))
    else:
        print(colored("\n=== FILM VISTI ===", "cyan"))
        for i in range(len(film)):
            print(colored(f"  {i + 1}. {film[i]}", "white"))
        print()


def inserisci_film(film):
    nome = input(colored("Nome del film da aggiungere: ", "cyan")).strip()
    if nome != "":
        film.append(nome)
        salva_film(film)
        print(colored(f'Film "{nome}" aggiunto!', "green"))
    else:
        print(colored("Nome non valido.", "red"))


def modifica_film(film):
    visualizza_film(film)
    if len(film) > 0:
        CONTROLLO = True
        while CONTROLLO:
            try:
                scelta = int(input(colored("Numero del film da modificare: ", "cyan")))
                if 1 <= scelta <= len(film):
                    nuovo_nome = input(colored("Nuovo nome: ", "cyan")).strip()
                    if nuovo_nome != "":
                        vecchio = film[scelta - 1]
                        film[scelta - 1] = nuovo_nome
                        salva_film(film)
                        print(colored(f'"{vecchio}" modificato in "{nuovo_nome}".', "green"))
                    else:
                        print(colored("Nome non valido.", "red"))
                    CONTROLLO = False
                else:
                    print(colored(f"Inserisci un numero tra 1 e {len(film)}.", "red"))
                    CONTROLLO = False
            except ValueError:
                print(colored("Devi inserire un numero intero.", "red"))


def cancella_film(film):
    visualizza_film(film)
    if len(film) > 0:
        CONTROLLO = True
        while CONTROLLO:
            try:
                scelta = int(input(colored("Numero del film da cancellare: ", "cyan")))
                if 1 <= scelta <= len(film):
                    rimosso = film.pop(scelta - 1)
                    salva_film(film)
                    print(colored(f'Film "{rimosso}" cancellato.', "green"))
                    CONTROLLO = False
                else:
                    print(colored(f"Inserisci un numero tra 1 e {len(film)}.", "red"))
                    CONTROLLO = False
            except ValueError:
                print(colored("Devi inserire un numero intero.", "red"))


film = carica_film()
print(colored(f"Caricati {len(film)} film dal file.", "yellow"))

CONTROLLO = True
while CONTROLLO:
    print(colored("\n=== COLLEZIONE FILM ===", "cyan"))
    print(colored("  1. Visualizza film", "white"))
    print(colored("  2. Inserisci film", "white"))
    print(colored("  3. Modifica film", "white"))
    print(colored("  4. Cancella film", "white"))
    print(colored("  0. Esci", "white"))
    scelta = input(colored("Scelta: ", "cyan")).strip()

    if scelta == "1":
        visualizza_film(film)
    elif scelta == "2":
        inserisci_film(film)
    elif scelta == "3":
        modifica_film(film)
    elif scelta == "4":
        cancella_film(film)
    elif scelta == "0":
        print(colored("Arrivederci!", "yellow"))
        CONTROLLO = False
    else:
        print(colored("Scelta non valida.", "red"))