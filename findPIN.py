#importo le libreire necessarie
import hashlib
import time

#mio Numero di matricola
matricola = "0082200738"

#hash target fornito
target_hash = "5ef6514ed33a3cf66b95b982541114ac352c52729dbf80747775a9d1a733af93"

#ansi: definisco i colori per una migliore visualizzazione nel terminale
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'

#html: per l'esportazione del file HTML mi basta solo il rosso
RED_HTML = '<span style="color: red;">'
RESET_HTML = '</span>'

#funzione per calcolare il numero di collisioni
def count_collisions(hash1, hash2):
    return sum(1 for i in range(len(hash1)) if hash1[i] == hash2[i])

"""
funzione per evidenziare in verde le collisioni negli hash intermedi
qui uso il verde per differenziarle con quelle del risultao
NOTA: questa funzione l'ho utilizzato solo nel termonale
"""
def highlight_collisions(intermediate_hash, target_hash):
    highlighted_hash = ""
    for i in range(len(intermediate_hash)):
        if intermediate_hash[i] == target_hash[i]:
            highlighted_hash += f"{GREEN}{intermediate_hash[i]}{RESET}"
        else:
            highlighted_hash += intermediate_hash[i]
    return highlighted_hash

#funzione chiave per trovare il PIN con almeno 13 collisioni
def find_pin_with_collisions():
    pin = 1  #inizializzo il PIN a 1 perchè deve essere un intero non nullo
    start_time = time.time()  #calcolo il tempo di esecuzione
    while True:
        #concateno il pin con la mia matricola e faccio la codifica  utf8
        data = (str(pin) + matricola).encode('utf-8')

        #calcolo dell'hash SHA-256
        computed_hash = hashlib.sha256(data).hexdigest()

        #Conto le collisioni tra l'hash calcolato e quello target
        collisions = count_collisions(computed_hash, target_hash)

        #opzionale
        #ogni 500 iterazioni, stampa lo stato del programma
        #si potrebbe aumentare ma diventerebbe barboso, un po alla google
        if pin % 500 == 0:
            elapsed_time = time.time() - start_time
            highlighted_hash = highlight_collisions(computed_hash, target_hash)
            print(f"Tentativo: {pin}, Hash generato: {highlighted_hash}, Collisioni: {collisions}, Tempo trascorso: {elapsed_time:.2f} sec")

        #se trovo almeno 13 collisioni ho trovato il PIN
        if collisions >= 13:
            return pin, computed_hash, collisions

        #incrementa il PIN per provare il successivo
        pin += 1

print("\nOutout a campione ogni 500 tentativi fino a trovare le 13 collisioni:\n")

#eseguo la funzione
pin, resulting_hash, collision_count = find_pin_with_collisions()

print("\nTrovate le 13 Collisioni nelle seguenti posizioni e nei seguenti caratteri:\n")

#preparo i risultati per la stampa e l'esportazione in nel fil html
results = []
results.append("<html><body>")
results.append("<h2>Risultati Finali</h2>")
results.append(f"<p>Numero di matricola: {matricola}</p>")
results.append(f"<p>PIN trovato: {pin}</p>")
results.append(f"<p>Hash generato: {resulting_hash}</p>")
results.append(f"<p>Numero di collisioni: {collision_count}</p>")
results.append("<h3>Collisioni nelle seguenti posizioni e nei seguenti caratteri:</h3><ul>")

#stampo le collisioni specifiche (senza colorazione nel terminale)
for i in range(len(resulting_hash)):
    if resulting_hash[i] == target_hash[i]:
        collision_detail = f"Posizione {i + 1}: {resulting_hash[i]}"
        print(collision_detail)
        results.append(f"<li>Posizione {i + 1}: {resulting_hash[i]}</li>")

#aggiungo la sezione con il PIN trovato, hash generato e numero di collisioni nell'output del terminale
print("\nPIN trovato:", pin)
print("Hash generato:", resulting_hash)
print("Numero di collisioni:", collision_count)

#mostro l'hash target e l'hash generato con le collisioni evidenziate in ROSSO solo nel confronto finale
results.append("<h3>Confronto Hash Target e Hash Generato</h3>")
target_line = "Hash target:   "
generated_line = "Hash generato: "

#aggiungo dei caratteri rossi per le collisioni nel confronto finale
for i in range(len(target_hash)):
    if resulting_hash[i] == target_hash[i]:
        target_line += f"{RED_HTML}{target_hash[i]}{RESET_HTML}"
        generated_line += f"{RED_HTML}{resulting_hash[i]}{RESET_HTML}"
    else:
        target_line += target_hash[i]
        generated_line += resulting_hash[i]

#stampo il confronto con collisioni in rosso nel terminale per una migliore leggibilità
print(f"\n{target_line.replace(RED_HTML, RED).replace(RESET_HTML, RESET)}")
print(f"{generated_line.replace(RED_HTML, RED).replace(RESET_HTML, RESET)}")

#aggiungo il confronto all'output HTML
results.append(f"<p>{target_line}</p>")
results.append(f"<p>{generated_line}</p>")
results.append("</body></html>")

#esporto il file html
try:
    with open("risultati_collisioni.html", "w") as file:
        file.write("\n".join(results))
    print("\nFile HTML esportato con successo!")
except Exception as e:
    print(f"\nErrore nell'esportazione del file HTML: {e}")




