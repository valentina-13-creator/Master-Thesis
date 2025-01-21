pip install stanza

import pandas as pd
import stanza

# Inizializza la pipeline per l'italiano
nlp = stanza.Pipeline('it', processors='tokenize,mwt,pos', use_gpu=False)

# Funzione per processare un singolo DataFrame e restituire i conteggi per riga
def conta_pronomi_persona_per_riga(df):
    risultati = []

    for index, row in df.iterrows():
        titolo = row['Titolo']
        testo = row['Testo']
        testo_completo = f"{titolo} {testo}"

        doc = nlp(testo_completo)

        counts = {"1st sing.": 0, "1st plur.": 0, "2nd": 0, "3rd": 0}

        for sent in doc.sentences:
            for word in sent.words:
                if word.feats:
                    if 'Person=1' in word.feats and 'Number=Sing' in word.feats:
                        counts["1st sing."] += 1
                    elif 'Person=1' in word.feats and 'Number=Plur' in word.feats:
                        counts["1st plur."] += 1
                    elif 'Person=2' in word.feats:
                        counts["2nd"] += 1
                    elif 'Person=3' in word.feats:
                        counts["3rd"] += 1

        risultati.append({
            "Titolo": titolo,
            "1st sing.": counts["1st sing."],
            "1st plur.": counts["1st plur."],
            "2nd": counts["2nd"],
            "3rd": counts["3rd"]
        })

    return pd.DataFrame(risultati)

# Processa i tre file Excel e salva tre file di output
def processa_e_salva_file_pronomi(file1, file2, file3, output1, output2, output3):
    # Leggi i file
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    df3 = pd.read_excel(file3)

    # Controlla le colonne richieste
    for df in [df1, df2, df3]:
        if 'Titolo' not in df.columns or 'Testo' not in df.columns:
            raise ValueError("Ogni file deve contenere le colonne 'Titolo' e 'Testo'.")

    # Conta i pronomi per ciascun file e salva i risultati
    risultati1 = conta_pronomi_persona_per_riga(df1)
    risultati2 = conta_pronomi_persona_per_riga(df2)
    risultati3 = conta_pronomi_persona_per_riga(df3)

    risultati1.to_excel(output1, index=False)
    risultati2.to_excel(output2, index=False)
    risultati3.to_excel(output3, index=False)

    print(f"File di output salvati in: {output1}, {output2}, {output3}")

# Esempio di utilizzo della funzione
# Sostituisci i percorsi con quelli dei tuoi file
processa_e_salva_file_pronomi(
    "corpus_anoressia_ex.xlsx",
    "corpus_bulimia_ex.xlsx",
    "corpus_controllo_ex.xlsx",
    "output_anoressia_pronomi.xlsx",
    "output_bulimia_pronomi.xlsx",
    "output_controllo_pronomi.xlsx"
)
