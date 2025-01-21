pip install stanza

import pandas as pd
import stanza

# Inizializza la pipeline per l'italiano
nlp = stanza.Pipeline('it', processors='tokenize,mwt,pos', use_gpu=False)

# Funzione per processare un singolo DataFrame e restituire i conteggi per riga
def conta_tempi_verbi_per_riga(df):
    risultati = []

    for index, row in df.iterrows():
        titolo = row['Titolo']
        testo = row['Testo']
        testo_completo = f"{titolo} {testo}"

        doc = nlp(testo_completo)

        counts = {"present": 0, "past": 0, "future": 0}

        for sent in doc.sentences:
            words = sent.words
            skip_next = False

            for i, word in enumerate(words):
                if skip_next:
                    skip_next = False
                    continue

                if word.upos == "AUX" and i + 1 < len(words) and words[i + 1].feats and "VerbForm=Part" in words[i + 1].feats:
                    aux_tense = ""
                    if isinstance(word.feats, str):
                        if "Tense=" in word.feats:
                            aux_tense = word.feats.split("Tense=")[1].split("|")[0]
                    else:
                        aux_tense = word.feats.get("Tense", "")

                    if aux_tense == "Pres":
                        counts["past"] += 1
                    elif aux_tense in {"Past", "Imp"}:
                        counts["past"] += 1
                    elif aux_tense == "Fut":
                        counts["future"] += 1
                    skip_next = True
                elif word.upos == "VERB":
                    verb_tense = ""
                    if isinstance(word.feats, str):
                        if "Tense=" in word.feats:
                            verb_tense = word.feats.split("Tense=")[1].split("|")[0]
                    else:
                        verb_tense = word.feats.get("Tense", "")

                    if verb_tense == "Pres":
                        counts["present"] += 1
                    elif verb_tense in {"Past", "Imp"}:
                        counts["past"] += 1
                    elif verb_tense == "Fut":
                        counts["future"] += 1

        risultati.append({
            "Titolo": titolo,
            "present": counts["present"],
            "past": counts["past"],
            "future": counts["future"]
        })

    return pd.DataFrame(risultati)

# Processa i tre file Excel e salva tre file di output
def processa_e_salva_file_tempi(file1, file2, file3, output1, output2, output3):
    # Leggi i file
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)
    df3 = pd.read_excel(file3)

    # Controlla le colonne richieste
    for df in [df1, df2, df3]:
        if 'Titolo' not in df.columns or 'Testo' not in df.columns:
            raise ValueError("Ogni file deve contenere le colonne 'Titolo' e 'Testo'.")

    # Conta i tempi verbali per ciascun file e salva i risultati
    risultati1 = conta_tempi_verbi_per_riga(df1)
    risultati2 = conta_tempi_verbi_per_riga(df2)
    risultati3 = conta_tempi_verbi_per_riga(df3)

    risultati1.to_excel(output1, index=False)
    risultati2.to_excel(output2, index=False)
    risultati3.to_excel(output3, index=False)

    print(f"File di output salvati in: {output1}, {output2}, {output3}")

processa_e_salva_file_tempi(
    "corpus_anoressia_ex.xlsx",
    "corpus_bulimia_ex.xlsx",
    "corpus_controllo_ex.xlsx",
    "output_anoressia_tempi.xlsx",
    "output_bulimia_tempi.xlsx",
    "output_controllo_tempi.xlsx"
)
