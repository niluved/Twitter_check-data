import datetime
import requests
import os

profilo = 'nonmilamento'

url_profilo = f'https://twitter-followers.p.rapidapi.com/{profilo}/profile'
url_followers = f'https://twitter-followers.p.rapidapi.com/{profilo}/followers'
url_following = f'https://twitter-followers.p.rapidapi.com/{profilo}/following'

querystring = {"page": "1"}

headers = {
    "X-RapidAPI-Key": "",  # inserire la chiave API
    "X-RapidAPI-Host": "twitter-followers.p.rapidapi.com"
}

# profilo_info = requests.get(url_profilo, headers=headers)


def chiamata_api():
    # faccio la chiamata api per la lista dei followers
    followers = requests.get(
        url_followers, headers=headers, params=querystring)

    # controllo che la risposta del server sia 200 e scrivo i followers nel file
    if followers.status_code == 200:
        print(
            f'Followers API request successful. Status code: {followers.status_code}')
        with open('myprofile_followers.txt', 'w') as file:
            file.write(followers.text)

    else:
        print(
            f"Followers API request failed. Error code: {followers.status_code}")
        return

    # faccio la chiamata api per la lista dei following e la scrivo in un file di testo
    following = requests.get(
        url_following, headers=headers, params=querystring)

    # Check if the response status code is 200
    if following.status_code == 200:
        print(
            f'Following API request successful. Status code: {following.status_code}')
        with open('myprofile_following.txt', 'w') as file:
            file.write(following.text)
    else:
        print(
            f"Following API request failed. Error code:{following.status_code}")
        return


# chiedo all'utente se vuole spendere due chiamate api (limite max 10 ogni 24hr) per aggiornare followers e following (altrimenti verranno stampati i valori già salvati nei file)
decisione = input(
    'Effettuare una chiamata api per aggiornare i dati del profilo in realtime? (y/n) ').lower()

if decisione == 'y':
    decisione_flag = 1
else:
    decisione_flag = 0

# lancio le chiamate api in caso di assenso dell'utente
if decisione_flag == 1:
    chiamata_api()

# ---- FOLLOWERS -----

# leggo i followers dal file di testo
with open('myprofile_followers.txt', 'r') as file:
    contents_followers = file.readlines()

# creo la lista dei followers tirando fuori l'unico elemento della lista del file (nel file c'è un'unico elemento) e splittarlo con la virgola
lista_followers = contents_followers[0].split('","')

# pulisco il primo e ultimo elemento dai doppi apici iniziali/finali e dalla parentesi quadra iniziale/finale
lista_followers[0] = lista_followers[0].replace('["', '')
lista_followers[-1] = lista_followers[-1].replace('"]', '')

# print('Followers:', lista_followers)
# print('Followers:', len(lista_followers))

# ---- FOLLOWING -----

# leggo i following dal file di testo
with open('myprofile_following.txt', 'r') as file:
    contents_following = file.readlines()

# creo la lista dei following tirando fuori l'unico elemento della lista del file (nel file c'è un'unico elemento) e splittarlo con la virgola
lista_following = contents_following[0].split('","')

# pulisco il primo e ultimo elemento dai doppi apici iniziali/finali e dalla parentesi quadra iniziale/finale
lista_following[0] = lista_following[0].replace('["', '')
lista_following[-1] = lista_following[-1].replace('"]', '')

# print('Following:', lista_following)
# print('Following:', len(lista_following))

# ---- TROVA MUTUALS, SOLO FOLLOWERS E SOLO FOLLOWING

mutuals = []
solo_followers = []
solo_following = []

for i in lista_followers:
    if i in lista_following:
        mutuals.append(i)

for i in lista_followers:
    if i not in lista_following:
        solo_followers.append(i)

for i in lista_following:
    if i not in lista_followers:
        solo_following.append(i)

# stampo a schermo i risultati
print('\nNome del profilo:', profilo, '\n')
print('Followers:', len(lista_followers))
print('Following:', len(lista_following))
print('Mutuals:', len(mutuals))
print('Followers univoci:', len(solo_followers))
print('Following univoci:', len(solo_following))

# scrivo le liste dei mutuals, solo followers e solo following in files di testo
with open('myprofile_mutuals.txt', 'w') as file:
    for i in mutuals:
        file.write(f'{i}\n')

with open('myprofile_solo_followers.txt', 'w') as file:
    for i in solo_followers:
        file.write(f'{i}\n')

with open('myprofile_solo_following.txt', 'w') as file:
    for i in solo_following:
        file.write(f'{i}\n')

print('\nTutti i dati di dettaglio sono stati salvati nei file di testo.\n')

# ---- CHECK DEFOLLOWS-----


def check_var_followers():
    # imposto la data e ora correnti
    adesso = datetime.datetime.now()
    oggi = adesso.strftime("%Y-%m-%d_%H-%M-%S")

    # leggo i "vecchi" followers dal file di testo
    with open('myprofile_followers_static.txt', 'r') as file:
        contents_followers_static = file.readlines()

    # creo la lista dei followers tirando fuori l'unico elemento della lista del file (nel file c'è un'unico elemento) e splittarlo con la virgola
    lista_followers_static = contents_followers_static[0].split('","')

    # pulisco il primo e ultimo elemento dai doppi apici iniziali/finali e dalla parentesi quadra iniziale/finale
    lista_followers_static[0] = lista_followers_static[0].replace('["', '')
    lista_followers_static[-1] = lista_followers_static[-1].replace('"]', '')

    # verifico le liste dei followers vecchi e nuovi per trovare le differenze
    nuovi_followers = []
    defollows = []

    for i in lista_followers:
        if i not in lista_followers_static:
            nuovi_followers.append(i)

    for i in lista_followers_static:
        if i not in lista_followers:
            defollows.append(i)

    print('Nuovi followers:', len(nuovi_followers), '\n', nuovi_followers)
    print('Defollows:', len(defollows), '\n', defollows)

    # creo il file di log versionato nella sottocartella logs
    # per farlo verifico la cartella corrente e imposto il percorso della sottocartella 'logs'
    cartella_corrente = os.path.dirname(__file__)
    sottocartella = os.path.realpath(os.path.join(cartella_corrente, 'logs'))

    # with open(f'C:/Nick/Coding/api_project/Twitter/logs/log_{oggi}.txt','w') as file:
    with open(f'{sottocartella}\\log_{oggi}.txt', 'w') as file:
        file.write('Nuovi followers:\n')
        for i in nuovi_followers:
            file.write(i)
            file.write('\n')
        file.write('\nDefollows:\n')
        for i in defollows:
            file.write(i)
            file.write('\n')

    # sovrascrivo il file dei followers static con i nuovi followers per resettare il conteggio
    with open('myprofile_followers.txt', 'r') as file:
        followers_letti = file.read()

    with open('myprofile_followers_static.txt', 'w') as file:
        file.write(followers_letti)


# lancio la funzione di verifica dei followers in caso di chiamata api effettuata
if decisione_flag == 1:
    check_var_followers()
