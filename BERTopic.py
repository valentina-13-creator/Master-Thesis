pip install bertopic[spacy]
pip install sentence-transformers
pip install spacy
pip install pandas
pip install openpyxl
python -m spacy download it_core_news_lg

from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import spacy
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

# Modello di embedding per l'italiano
embedding_model = SentenceTransformer('distiluse-base-multilingual-cased-v2')

# Carica il modello italiano di SpaCy
nlp = spacy.load('it_core_news_lg')

# Aggiungi stopwords italiane
stop_words = spacy.lang.it.stop_words.STOP_WORDS
#nlp.Defaults.stop_words.update(stop_words)


# Aggiungi le stopwords personalizzate alla lista di SpaCy
custom_stop_words = {"mi", "essere", "avere", "il", "la", "un", "in", "di", "per", "nn", "ke", "ciao", "bulimia", "sn"}

# Aggiungi le stopwords personalizzate alla lista di stopwords di SpaCy
for stopword in custom_stop_words:
    nlp.Defaults.stop_words.add(stopword)

#debug
if "volere" in stop_words:
    print("La parola 'volere' è presente nella lista di stopwords.")
else:
    print("La parola 'volere' non è presente nella lista di stopwords.")

def preprocess_text_debug(text):
    # Converti qualsiasi float in stringa
    if isinstance(text, float):
        text = str(text)
    doc = nlp(text)
    #for token in doc:
        #print(f"Token: {token.text}, Lemma: {token.lemma_}, Stopword: {token.is_stop}")
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)



# Carica il file Excel
file_path = 'corpus_bulimia_ex.xlsx'  # Inserisci il percorso corretto del file Excel
df = pd.read_excel(file_path)

# Combina il titolo e il testo in un unico campo
df['combined'] = df['Titolo'] + " " + df['Testo']


# Esegui su un esempio di commento per vedere il comportamento
df['processed_debug'] = df['combined'].apply(preprocess_text_debug)

# Estrai tutti i commenti combinati (titolo + testo)
docs = df['processed_debug'].tolist()

# Convert any floats to strings in the docs list
docs1 = [str(doc) for doc in docs]

# Verifica il testo preprocessato prima del topic modeling
print(docs1[:5])  # Controlla i primi 5 documenti per vedere se le stopwords sono state rimosse


# Crea un vectorizer con stopwords personalizzate
vectorizer_model = CountVectorizer(stop_words=list(stop_words))  

# Passa il vectorizer personalizzato a BERTopic
topic_model = BERTopic(embedding_model=embedding_model, vectorizer_model=vectorizer_model)

# Applica il topic modeling sui commenti preprocessati
topics, probs = topic_model.fit_transform(docs1)

# Mostra informazioni sui temi generati
topic_info = topic_model.get_topic_info()
print(topic_info)

# Visualizza le parole chiave con un grafico a barre
topic_model.visualize_barchart()

