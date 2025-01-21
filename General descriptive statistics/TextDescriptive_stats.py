pip install spacy textdescriptives pandas openpyxl
python -m spacy download it_core_news_lg

import spacy
import textdescriptives as td
import pandas as pd

# Carica il modello di spaCy per l'italiano
nlp = spacy.load("it_core_news_lg")

# Aggiungi il componente per le statistiche descrittive alla pipeline
nlp.add_pipe("textdescriptives/descriptive_stats")

#Carica il file Excel
file_path = 'corpus_controllo_ex.xlsx'  # Sostituisci con il nome del file corretto
df = pd.read_excel(file_path)

# Definisci una funzione per estrarre le metriche dal testo
def analyze_text(title, text):
    doc = nlp(text)  # Applica spaCy al testo
    metrics = doc._.descriptive_stats  # Estrai le metriche
    metrics['Titolo'] = title  # Aggiungi il titolo associato al testo
    return metrics


#  Applica l'analisi al dataset
results = []
for index, row in df.iterrows():
    title = row['Titolo']  # Colonna dei titoli
    text = row['Testo']    # Colonna del testo
    result = analyze_text(title, text)
    results.append(result)

# Crea un dataframe con i risultati
results_df = pd.DataFrame(results)
#  Visualizza o salva i risultati
print(results_df.head())  # Mostra le prime righe del dataframe
results_df.to_excel('controllo_textdescriptives.xlsx', index=False)