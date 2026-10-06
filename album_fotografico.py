
import csv

def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    album = []

    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader, None)  # Salta la prima riga delle intestazioni

            for riga in reader:
                if not riga or len(riga) < 5:
                    continue  # Salta righe vuote o malformate

                codice = riga[0].strip()
                titolo = riga[1].strip()
                autore = riga[2].strip()
                mese = int(riga[3].strip())
                anno = int(riga[4].strip())

                # Creiamo il dizionario della singola foto
                foto = {
                    'codice': codice,
                    'titolo': titolo,
                    'autore': autore,
                    'mese': mese,
                    'anno': anno
                }

                # Cerca se l'anno è già presente nell'album
                anno_trovato = False
                for gruppo in album:
                    if gruppo['anno'] == anno:
                        gruppo['foto'].append(foto)
                        anno_trovato = True
                        break

                # Se l'anno non è ancora presente, aggiungiamo una nuova voce per l'anno
                if not anno_trovato:
                    album.append({
                        'anno': anno,
                        'foto': [foto]
                    })

        print("Album caricato con successo!")
        return album

    except FileNotFoundError:
        print(f"Errore: Il file '{file_path}' non è stato trovato.")
        return None
    except Exception as e:
        print(f"Errore durante la lettura del file: {e}")
        return None


def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    # Verifica univocità codice
    if cerca_foto(album, codice) is not None:
        print(f"Errore: Esiste già una foto con il codice '{codice}'.")
        return None

    # Validazione del mese
    if not (1 <= mese <= 12):
        print("Errore: Il mese deve essere un numero compreso tra 1 e 12.")
        return None

    foto = {
        'codice': codice,
        'titolo': titolo,
        'autore': autore,
        'mese': mese,
        'anno': anno
    }

    # Inserimento nell'album
    anno_trovato = False
    for gruppo in album:
        if gruppo['anno'] == anno:
            gruppo['foto'].append(foto)
            anno_trovato = True
            break

    if not anno_trovato:
        album.append({
            'anno': anno,
            'foto': [foto]
        })

    # Aggiornamento/Aggiunta sul file CSV (modalità append)
    try:
        with open(file_path, mode='a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([codice, titolo, autore, mese, anno])
    except Exception as e:
        print(f"Avviso: Foto aggiunta in memoria, ma errore nella scrittura su file: {e}")

    return foto


def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice"""
    for gruppo in album:
        for foto in gruppo['foto']:
            if foto['codice'] == codice:
                return foto
    return None


def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    for gruppo in album:
        if gruppo['anno'] == anno:
            titoli = [foto['titolo'] for foto in gruppo['foto']]
            titoli.sort()
            return titoli
    return None


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is not None:
                    break

        elif scelta == "2":
            if not album:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()
            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto:
                print(f"Foto aggiunta con successo!")
            else:
                print("Non è stato possibile aggiungere la foto.")

        elif scelta == "3":
            if not album:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"Foto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if not album:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"Nessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()
