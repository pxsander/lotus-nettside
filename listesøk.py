#%%
import csv

#dette er kode som hvar på prøve exsamen så den er ikke like viktig men den skulle hvere en del av lotus nettsiden
def legg_til_navn_og_epost(navn, epost):
    with open('username_email.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([navn, epost])

def legg_til_flere_navn():
    antall_navn = int(input("Hvor mange navn vil du legge til? "))

    for _ in range(antall_navn):

        fornavn = input("Skriv inn ditt fornavn: ")
        etternavn = input("Skriv inn ditt etternavn: ")
        domene = "lotus.com"
        lag_brukernavn = fornavn[:3].lower() + etternavn[:1].lower()
        lag_epost = lag_brukernavn + "@" + domene

        navn = lag_brukernavn
        epost = lag_epost
        legg_til_navn_og_epost(navn, epost)

def søk_navn(navn):
    with open('username_email.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        funnet = False
        for rad in reader:
            if rad[0] == navn:
                print("Navn: ", rad[0])
                print("E-post: ", rad[1])
                funnet = True
                break
        if not funnet:
            print("Navnet ble ikke funnet i CSV-filen.")

def vis_liste():
    with open('username_email.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for rad in reader:
            if len(rad) >= 2:
                navn = rad[0]
                epost = rad[1]
                print("Navn: ", navn)
                print("E-post: ", epost)
                print("--------------------")
            else:
                print("Ugyldig rad i CSV-filen.")

def fjern_brukere_med_nøkkelord(nøkkelord):
    oppdatert_liste = []
    with open('username_email.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for rad in reader:
            navn = rad[0]
            epost = rad[1]
            if nøkkelord.lower() not in navn.lower():
                oppdatert_liste.append([navn, epost])
    
    return oppdatert_liste

def fjern_brukere_med_nøkkelord_og_oppdater_csv(nøkkelord):
    oppdatert_liste = fjern_brukere_med_nøkkelord(nøkkelord)

    with open('username_email.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for brukerinfo in oppdatert_liste:
            writer.writerow(brukerinfo)
    
    print("Brukere med nøkkelordet", nøkkelord, "er fjernet fra CSV-filen.")


valg = input("Velg 1 for å søke etter navn, 2 for å vise hele listen, 3 for å legge til flere navn, 4 for å fjerne brukere med nøkkelord: ")

if valg == "1":
    navn = input("Skriv inn navnet du ønsker å søke etter: ")
    søk_navn(navn)
elif valg == "2":
    vis_liste()
elif valg == "3":
    legg_til_flere_navn()
elif valg == "4":
    nøkkelord = input("Skriv inn nøkkelordet for å fjerne brukere: ")
    fjern_brukere_med_nøkkelord_og_oppdater_csv(nøkkelord)
else:
    print("Ugyldig valg.")
    # %%
