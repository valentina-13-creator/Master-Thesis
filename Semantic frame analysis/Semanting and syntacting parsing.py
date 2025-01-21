pip install spacy

spacy download it_core_news_lg

import json
import spacy
import os
import pandas as pd
from collections import defaultdict

# Load spaCy model
nlp = spacy.load("it_core_news_lg")

# Directory containing JSON files
input_directory = "/content/output_lome"

# Aggregate counters for SituationType, SituationKind, syntactic constructions, roles, and roots
situation_stats = defaultdict(lambda: defaultdict(lambda: {'count': 0, 'constructions': defaultdict(lambda: {'count': 0, 'roots': [], 'roles': [], 'frame_triggers': []})}))

# Function to align tokens by character spans
def align_tokens_by_char_span(lome_data, spacy_doc):
    alignment_map = {}
    for situation in lome_data['situationMentionSetList'][0]['mentionList']:
        lome_text = situation['text']
        start_idx = lome_data['text'].find(lome_text)
        end_idx = start_idx + len(lome_text)
        spacy_tokens = [token for token in spacy_doc if token.idx >= start_idx and token.idx < end_idx]
        spacy_token_indices = [token.i for token in spacy_tokens]
        alignment_map[lome_text] = spacy_token_indices
    return alignment_map

# Function to classify tokens according to the user's rules
def classify_token(token, roles, situation_kind, children):
    if token.pos_ != "VERB":
        if token.pos_ in ["ADJ", "NOUN"] and any(child.text == "è" and child.dep_ == "cop" for child in children):
            return "nominal construction"
        else:
            return "ARG"

    if any(child.dep_ == "expl:impers" for child in children) or ("Precipitation" in roles and not any(child.dep_ == "nsubj" for child in children)):
        return "impersonal"

    if (
        any(role in roles for role in ["Protagonist", "Entity", "Perceiver", "Perceiver_passive", "Patient", "Theme", "Experiencer"]) or
        not roles or
        "Existence" in situation_kind or
        token.dep_ == "acl"
    ):
        if any(child.lemma_ == "avere" and child.pos_ == "AUX" for child in children) or any(child.dep_ == "obj" for child in children):
            return "active"
        elif any(child.lemma_ == "essere" and child.dep_ == "aux" and any(grandchild.dep_ == "aux:pass" for grandchild in children) for child in children):
            return "passive"
        else:
            return "unaccusative"


    if any(child.dep_ in ["nsubj:pass", "aux:pass"] for child in children):
        if any(child.dep_ == "obl:agent" for child in children):
            return "passive with agent"
        else:
            return "passive"


    if any(child.lemma_ == "avere" and child.pos_ == "AUX" for child in children) or any(child.dep_ == "obj" for child in children):
        return "active"

    return "active"

# Process each JSON file in the directory
for filename in os.listdir(input_directory):
    if filename.endswith(".json"):
        filepath = os.path.join(input_directory, filename)
        with open(filepath) as f:
            lome_data = json.load(f)

        doc = nlp(lome_data['text'])
        alignment_map = align_tokens_by_char_span(lome_data, doc)

        for situation in lome_data['situationMentionSetList'][0]['mentionList']:
            lome_text = situation['text']
            spacy_indices = alignment_map.get(lome_text, [])
            roles = [arg['role'] for arg in situation['argumentList']]
            situation_type = situation.get('situationType', 'Unknown')
            situation_kind = situation.get('situationKind', 'Unknown')

            # Use the main token in SituationMentionList as the frame trigger
            frame_trigger = lome_text

            # Classify each token within the situation and count all syntactic constructions
            for i in spacy_indices:
                token = doc[i]
                children = list(token.children)
                construction_type = classify_token(token, roles, situation_kind, children)

                # Collect statistics based on SituationType and SituationKind
                situation_stats[situation_type][situation_kind]['count'] += 1
                situation_stats[situation_type][situation_kind]['constructions'][construction_type]['count'] += 1
                situation_stats[situation_type][situation_kind]['constructions'][construction_type]['roles'].extend(roles)
                situation_stats[situation_type][situation_kind]['constructions'][construction_type]['frame_triggers'].append(frame_trigger)

                # Add root verbs and their subjects as roots in the output
                if token.dep_ == "ROOT" or (token.dep_.startswith("nsubj") and token.head.dep_ == "ROOT"):
                    root_entry = token.text if token.dep_ == "ROOT" else f"{token.head.text} (subject: {token.text})"
                    situation_stats[situation_type][situation_kind]['constructions'][construction_type]['roots'].append(root_entry)

# Organize data for export to DataFrame
output_data = []
for situation_type, kinds in situation_stats.items():
    total_occurrences = sum(kind_data['count'] for kind_data in kinds.values())
    for situation_kind, kind_data in kinds.items():
        for construction, data in kind_data['constructions'].items():
            output_data.append({
                'SituationType': situation_type,
                'Total Occurrences': total_occurrences,
                'SituationKind': situation_kind,
                'Occurrences': kind_data['count'],
                'Construction Type': construction,
                'Construction Count': data['count'],
                'Roles': ', '.join(set(data['roles'])),
                'Roots': ', '.join(set(data['roots'])),
                'Frame Triggers': ', '.join(set(data['frame_triggers']))
            })

# Sort the DataFrame by occurrences in descending order
df = pd.DataFrame(output_data)
df = df.sort_values(by=['Total Occurrences', 'Occurrences'], ascending=False)

# Save to Excel
output_file = "/content/Control_lome_spacy_DEF.xlsx"
df.to_excel(output_file, index=False)
print(f"Results saved to {output_file}")
