#Types, Tokens, TTR

python -m spacy download it_core_news_sm

import pandas as pd
import spacy

# Load the Italian SpaCy model
nlp = spacy.load("it_core_news_sm")  

def process_text_data(input_file, output_file):
    # Load the dataset
    df = pd.read_excel(input_file)

    # Merge 'Titolo' and 'Testo' into a single column
    df['Merged_Text'] = df['Titolo'].fillna('') + ' ' + df['Testo'].fillna('')

    # Initialize lists to store results
    tokens_list = []
    types_list = []
    ttr_list = []

    for text in df['Merged_Text']:
        # Process the text using SpaCy
        doc = nlp(text)

        # Extract tokens, excluding stopwords, punctuation, and whitespace
        tokens = [token.text for token in doc if not token.is_punct and not token.is_space] #and not token.is_stop]

        # Compute the number of tokens
        num_tokens = len(tokens)
        tokens_list.append(num_tokens)

        # Compute the number of types (unique tokens)
        num_types = len(set(tokens))
        types_list.append(num_types)

        # Compute the Type-Token Ratio (TTR)
        ttr = num_types / num_tokens if num_tokens > 0 else 0
        ttr_list.append(ttr)

    # Add results to the DataFrame
    df['N_Tokens'] = tokens_list
    df['N_Types'] = types_list
    df['TTR'] = ttr_list

    # Prepare the output file with required columns
    output_df = df[['Titolo', 'N_Tokens', 'N_Types', 'TTR']]
    output_df.to_excel(output_file, index=False, engine='openpyxl')

    print(f"Processing complete. Results saved to {output_file}.")

# Replace 'your_input_file.xlsx' with your input file path and 'output_tokens_types_ttr.xlsx' with your desired output file path
input_file = "corpus_controllo_ex.xlsx"  # Input file
output_file = "output_tokens_types_ttr_cn.xlsx"  # Output file

process_text_data(input_file, output_file)