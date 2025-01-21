pip install pandas transformers openpyxl

import pandas as pd
import re
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from collections import Counter


#Sentiment Analysis and Emotion Detection tasks and Mismatches
import pandas as pd
import re
from transformers import pipeline
from transformers import AutoTokenizer
from collections import Counter

# Funzione per caricare il file Excel
def load_excel(file_path):
    df = pd.read_excel(file_path)
    return df

# Funzione per pulire il testo
def clean_text(text):
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)  # Rimuove punteggiatura e caratteri speciali
    text = re.sub(r'\s+', ' ', text)  # Rimuove spazi extra
    return text.strip()

def split_text(text, tokenizer, max_length=500):
    tokens = tokenizer(text, truncation=False, padding=False, return_tensors='pt')['input_ids'][0]
    chunks = [tokens[i:i + max_length] for i in range(0, len(tokens), max_length)]
    return [tokenizer.decode(chunk, skip_special_tokens=True) for chunk in chunks]

# Funzione per l'analisi delle emozioni
def analyze_emotions(texts, emotion_pipeline):
    emotion_results = []
    for text in texts:
        result = emotion_pipeline(text)
        for emotion in result:
            emotion_results.append(emotion['label'])
    return emotion_results

# Funzione per l'analisi dei sentimenti
def analyze_sentiments(texts, sentiment_pipeline):
    sentiment_results = []
    for text in texts:
        result = sentiment_pipeline(text)
        for sentiment in result:
            sentiment_results.append(sentiment['label'])
    return sentiment_results

# Funzione principale per l'analisi del file Excel
def analyze_file(file_path, output_file_path):
    # Caricamento del file Excel
    df = load_excel(file_path)

    # Caricamento dei modelli e dei tokenizer
    sentiment_model_name = "MilaNLProc/feel-it-italian-sentiment"
    emotion_model_name = "MilaNLProc/feel-it-italian-emotion"

    tokenizer_sentiment = AutoTokenizer.from_pretrained(sentiment_model_name)
    tokenizer_emotion = AutoTokenizer.from_pretrained(emotion_model_name)

    sentiment_pipeline = pipeline("text-classification", model=sentiment_model_name, tokenizer=tokenizer_sentiment, return_all_scores=False)
    emotion_pipeline = pipeline("text-classification", model=emotion_model_name, tokenizer=tokenizer_emotion, return_all_scores=False)

    # Liste per memorizzare i risultati
    sentiment_results = []
    emotion_results = []

    # Analisi di ogni riga
    for index, row in df.iterrows():
        title = row['Titolo']
        text = row['Testo']
        combined_text = clean_text(f"{title} {text}")

        # Suddividi il testo in chunk
        text_chunks = split_text(combined_text, tokenizer_sentiment)

        # Esegui l'analisi dei sentimenti e delle emozioni
        sentiments = analyze_sentiments(text_chunks, sentiment_pipeline)
        emotions = analyze_emotions(text_chunks, emotion_pipeline)

        # Aggrega i risultati (se suddiviso in chunk, prendi il primo risultato)
        if len(sentiments) > 0:
            sentiment = sentiments[0]
        if len(emotions) > 0:
            emotion = emotions[0]

        # Double-check: controlla se c'è coerenza tra sentiment ed emozione
        if (sentiment == "positive" and emotion != "joy") or (sentiment == "negative" and emotion == "joy"):
            print(f"Mismatch tra sentiment e emozione alla riga: {index + 1}")
            print(f"Testo: {combined_text}")

        # Aggiungi i risultati alle liste
        sentiment_results.append(sentiment)
        emotion_results.append(emotion)

    # Aggiungi le colonne di sentiment ed emozioni al dataframe
    df['Sentiment'] = sentiment_results
    df['Emotion'] = emotion_results

    # Salva il nuovo file Excel con i risultati
    df.to_excel(output_file_path, index=False)
    print(f"File con risultati salvato come: {output_file_path}")

# Esegui l'analisi sul file di input e salva il risultato
input_file = 'corpus_controllo_ex.xlsx'
output_file = 'feel_it_controllo.xlsx'
analyze_file(input_file, output_file)

