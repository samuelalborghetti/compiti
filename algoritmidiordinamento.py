from termcolor import colored

def bubble_sort(lista):
    """
    BUBBLE SORT  —  O(n²) medio/peggiore, O(n) migliore (lista già ordinata).
    Confronta coppie adiacenti e le scambia se sono nell'ordine sbagliato.
    Ad ogni passata il valore massimo 'galleggia' in fondo.
    Versione ottimizzata: se in un passaggio non avviene nessuno scambio,
    la lista è già ordinata e ci si ferma prima.
    """
    n = len(lista)
    lista = lista[:]
    i = 0
    CONTROLLO = True
    while i < n - 1 and CONTROLLO:
        scambiato = False
        j = 0
        while j < n - i - 1:
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                scambiato = True
            j += 1
        if not scambiato:
            CONTROLLO = False
        i += 1
    return lista


def selection_sort(lista):
    """
    SELECTION SORT  —  O(n²) sempre.
    Ad ogni passata cerca il minimo nella parte non ordinata
    e lo porta in testa. Fa sempre lo stesso numero di confronti
    ma il numero di scambi è al massimo n-1 (utile se scrivere è costoso).
    """
    lista = lista[:]
    n = len(lista)
    i = 0
    while i < n - 1:
        idx_min = i
        j = i + 1
        while j < n:
            if lista[j] < lista[idx_min]:
                idx_min = j
            j += 1
        if idx_min != i:
            lista[i], lista[idx_min] = lista[idx_min], lista[i]
        i += 1
    return lista


def insertion_sort(lista):
    """
    INSERTION SORT  —  O(n²) medio/peggiore, O(n) migliore.
    Costruisce la sequenza ordinata un elemento alla volta:
    prende il prossimo elemento e lo inserisce nella posizione
    corretta tra quelli già ordinati, come si fa con le carte in mano.
    Ottimo per liste piccole o quasi ordinate.
    """
    lista = lista[:]
    i = 1
    while i < len(lista):
        chiave = lista[i]
        j = i - 1
        while j >= 0 and lista[j] > chiave:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = chiave
        i += 1
    return lista


def merge_sort(lista):
    """
    MERGE SORT  —  O(n log n) sempre.
    Divide la lista a metà ricorsivamente finché restano sotto-liste
    da 1 elemento (già ordinate), poi le fonde (merge) in ordine.
    Stabile e prevedibile: garantisce O(n log n) in ogni caso.
    Richiede O(n) memoria aggiuntiva per le sotto-liste temporanee.
    """
    if len(lista) <= 1:
        return lista[:]

    meta = len(lista) // 2
    sinistra = merge_sort(lista[:meta])
    destra   = merge_sort(lista[meta:])

    return _merge(sinistra, destra)


def _merge(sinistra, destra):
    """Fonde due liste già ordinate in una unica lista ordinata."""
    risultato = []
    i = j = 0
    while i < len(sinistra) and j < len(destra):
        if sinistra[i] <= destra[j]:
            risultato.append(sinistra[i])
            i += 1
        else:
            risultato.append(destra[j])
            j += 1
    while i < len(sinistra):
        risultato.append(sinistra[i])
        i += 1
    while j < len(destra):
        risultato.append(destra[j])
        j += 1
    return risultato


def heap_sort(lista):
    """
    HEAP SORT  —  O(n log n) sempre, O(1) spazio aggiuntivo.
    Prima costruisce un max-heap dalla lista (il massimo sta sempre
    in cima), poi estrae ripetutamente il massimo portandolo in fondo.
    Non è stabile ma non richiede memoria extra: ordina 'sul posto'.
    """
    lista = lista[:]
    n = len(lista)

    def heapify(arr, n, i):
        """Ripristina la proprietà di max-heap a partire dal nodo i."""
        massimo = i
        sx = 2 * i + 1
        dx = 2 * i + 2
        if sx < n and arr[sx] > arr[massimo]:
            massimo = sx
        if dx < n and arr[dx] > arr[massimo]:
            massimo = dx
        if massimo != i:
            arr[i], arr[massimo] = arr[massimo], arr[i]
            heapify(arr, n, massimo)

    i = n // 2 - 1
    while i >= 0:
        heapify(lista, n, i)
        i -= 1

    i = n - 1
    while i > 0:
        lista[0], lista[i] = lista[i], lista[0]
        heapify(lista, i, 0)
        i -= 1

    return lista


def quick_sort(lista):
    """
    QUICK SORT  —  O(n log n) medio, O(n²) peggiore (pivot sfortunato).
    Sceglie un pivot, sposta a sinistra i valori minori e a destra
    i maggiori, poi ricorre sulle due metà.
    Versione migliorata: pivot scelto come mediana di tre valori
    (primo, centrale, ultimo) per ridurre drasticamente i casi peggiori.
    In pratica è l'algoritmo più veloce su dati casuali.
    """
    if len(lista) <= 1:
        return lista[:]

    lista = lista[:]
    primo, ultimo, centro = lista[0], lista[-1], lista[len(lista) // 2]
    pivot = sorted([primo, centro, ultimo])[1] 

    minori  = [x for x in lista if x < pivot]
    uguali  = [x for x in lista if x == pivot]
    maggiori = [x for x in lista if x > pivot]

    return quick_sort(minori) + uguali + quick_sort(maggiori)


def shell_sort(lista):
    """
    SHELL SORT  —  O(n log² n) con la sequenza di Ciura (la migliore nota).
    Generalizzazione dell'insertion sort: invece di confrontare elementi
    adiacenti usa un 'gap' decrescente. Con gap grandi sposta elementi
    lontani velocemente; quando gap=1 è un insertion sort su una lista
    quasi già ordinata (quindi molto veloce).
    La sequenza di gap di Ciura: [701, 301, 132, 57, 23, 10, 4, 1].
    """
    lista = lista[:]
    gap_ciura = [701, 301, 132, 57, 23, 10, 4, 1]

    for gap in gap_ciura:
        i = gap
        while i < len(lista):
            temp = lista[i]
            j = i
            while j >= gap and lista[j - gap] > temp:
                lista[j] = lista[j - gap]
                j -= gap
            lista[j] = temp
            i += 1
    return lista



def counting_sort(lista):
    """
    COUNTING SORT  —  O(n + k), dove k è il valore massimo.
    Non confronta elementi tra loro: conta quante volte appare
    ogni valore intero, poi ricostruisce la lista ordinata.
    Perfetto per interi in un range limitato (es. voti, età).
    Non applicabile a float o stringhe generiche.
    """
    if len(lista) == 0:
        return []
    minimo = min(lista)
    massimo = max(lista)
    conteggio = [0] * (massimo - minimo + 1)

    for val in lista:
        conteggio[val - minimo] += 1

    risultato = []
    i = 0
    while i < len(conteggio):
        j = 0
        while j < conteggio[i]:
            risultato.append(i + minimo)
            j += 1
        i += 1
    return risultato


def radix_sort(lista):
    """
    RADIX SORT  —  O(n * d), dove d è il numero di cifre del massimo.
    Ordina cifra per cifra, dalla meno significativa alla più significativa,
    usando counting sort come ordinamento stabile su ogni cifra.
    Batte O(n log n) quando d è piccolo rispetto a n.
    Funziona solo su interi non negativi.
    """
    if len(lista) == 0:
        return []

    lista = lista[:]
    massimo = max(lista)
    exp = 1

    CONTROLLO = True
    while CONTROLLO:
        lista = _counting_sort_per_cifra(lista, exp)
        exp *= 10
        if exp > massimo:
            CONTROLLO = False

    return lista


def _counting_sort_per_cifra(lista, exp):
    """Counting sort stabile sulla cifra indicata da exp (1, 10, 100, ...)."""
    n = len(lista)
    output = [0] * n
    conteggio = [0] * 10

    for val in lista:
        cifra = (val // exp) % 10
        conteggio[cifra] += 1

    i = 1
    while i < 10:
        conteggio[i] += conteggio[i - 1]
        i += 1

    i = n - 1
    while i >= 0:
        cifra = (lista[i] // exp) % 10
        output[conteggio[cifra] - 1] = lista[i]
        conteggio[cifra] -= 1
        i -= 1

    return output
