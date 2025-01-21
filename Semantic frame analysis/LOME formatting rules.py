#prende in input file excel, combina le colonne e divide le righe salvandole in file txt separati
import pandas as pd
import os

# Load the Excel file
file_path = 'corpus_controllo_ex.xlsx'  # Update with your Colab file path
df = pd.read_excel(file_path)

# Exclude the header row
df = df.iloc[1:]

# Create a directory to store the text files
output_dir = 'singletxtfiles_cn'
os.makedirs(output_dir, exist_ok=True)

# Loop through each row and save to a text file in the directory
for index, row in df.iterrows():
    # Merge the title and text columns
    content = f"{row[0]}\n{row[1]}"
    # Save to a text file in the specified directory
    with open(f"{output_dir}/text_{index}.txt", "w") as file:
        file.write(content)

print(f"Text files created successfully in '{output_dir}'.")

#formattare tutti i file nella cartella
import re
import os

def format_text(text):
    # Assicura che ogni segno di punteggiatura sia separato da spazi
    text = re.sub(r'(?<!\s)([,:;.!?])', r' \1', text)
    text = re.sub(r'([,:;.!?])(?!\s)', r'\1 ', text)

    # Normalizza gli spazi attorno ai segni per garantire consistenza
    text = re.sub(r'\s+', ' ', text)

    # Va a capo solo dopo l'ultimo segno di punteggiatura ripetuto
    text = re.sub(r'([.!?])\s(?=[.!?])', r'\1', text)  # Rimuove spazi tra segni ripetuti
    text = re.sub(r'([.!?]) ', r'\1\n', text)          # Va a capo dopo l'ultimo segno

    # Sostituisci parole che non esistono
    text = re.sub(r'\bxke\b', 'perché', text)
    text = re.sub(r'\bperchè\b', 'perché', text)
    text = re.sub(r'\bke\b', 'che', text)
    text = re.sub(r'\bki\b', 'chi', text)
    text = re.sub(r"\bo'\b", "perché", text)
    text = re.sub(r"\ba'\b", "à", text)
    text = re.sub(r"\bo'\b", "ò", text)
    text = re.sub(r"\bu'\b", "ù", text)
    text = re.sub(r"\bi'\b", "ì", text)
    text = re.sub(r"\be'\b", "é", text)
    text = re.sub(r"\bdott\b", "dottore", text)
    text = re.sub(r"\bgine\b", "ginecologo", text)
    text = re.sub(r"\bplease\b", "per favore", text)
    text = re.sub(r"\bcry\b", "piango", text)
    text = re.sub(r"\bprp\b", "proprio", text)
    text = re.sub(r"\bsn\b", "sono", text)
    text = re.sub(r"\bqst\b", "quest", text)
    text = re.sub(r"\bqualkosa\b", "qualcosa", text)
    text = re.sub(r"\bnn\b", "non", text)

    return text.strip()

def process_directory(input_dir, output_dir):
    # Crea la directory di output se non esiste
    os.makedirs(output_dir, exist_ok=True)

    # Loop through all files in the input directory
    for filename in os.listdir(input_dir):
        input_file = os.path.join(input_dir, filename)
        output_file = os.path.join(output_dir, filename)

        # Process only text files
        if os.path.isfile(input_file) and filename.endswith('.txt'):
            # Legge il contenuto del file di input
            with open(input_file, 'r', encoding='utf-8') as file:
                text = file.read()

            # Applica la formattazione al testo
            formatted_text = format_text(text)

            # Scrive il testo formattato nel file di output
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(formatted_text)

    print(f"Tutti i file sono stati processati e salvati nella directory '{output_dir}'.")

# Specifica le directory di input e output
input_dir = 'singletxtfiles_cn'
output_dir = 'singletxt_cn_formatted'

# Processa la directory
process_directory(input_dir, output_dir)