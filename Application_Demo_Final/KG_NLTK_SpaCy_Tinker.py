# -*- coding: utf-8 -*-
"""

Input: Path to PDF File in Row #146
To further enhance entities and triples extraction based on specific document 

# NUS-ISS MTECH EBAC Capstone Project (2023)
# Team Members: Kwan Yick Tan, Hiew Ming Yu, Lim Kim Hui, Chua Khai Shing, Ivan Ong Jun Yi

"""

import PyPDF2
import re
import spacy

# to plot knowledge graph
import networkx as nx
import matplotlib.pyplot as plt

# for data preprocessing before tokenization
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# for exporting csv with timestamp
import csv
import datetime

# for creating user interface 
import tkinter as tk
from tkinter import ttk

# ========================================
#               Functions
# ========================================

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            text += page.extract_text()
                  
    return text

def extract_entities_and_triples(text): #This part is specific to policy document & objective
    

    # Preprocess the text: lowercase, remove punctuation, and tokenize (split)
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    tokens = [word for word in tokens if word not in stop_words]

    # Remove specific words and numbers using regular expressions
    tokens = [word for word in tokens if not re.match(r'^(chapter|section|'
                                                     r'\d+(st|nd|rd|th)?|'
                                                     r'days?|weeks?|months?|years?)$', word)]

    cleaned_text = " ".join(tokens)    

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(cleaned_text)

    entities = []
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))

    triples = []
    
    for i in range(len(entities)):
        for j in range(i+1, len(entities)):
            subject, subject_type = entities[i]
            object_, object_type = entities[j]
            
            # Skip entities with label "CARDINAL" aka numerals that do not fall under another type
            if "CARDINAL" in (subject_type, object_type):
                continue                               
                        
            if subject_type != object_type:
                relation = "has_relation_with"  # Default relation label for entities of different types
                if subject_type == "PERSON" and object_type == "ORG":  # Customize relation labels based on entity types
                    relation = "connect_to"
                elif subject_type == "ORG" and object_type == "PERSON":
                    relation = "connect_to"
                elif subject_type == "PERSON" and object_type == "PERSON":
                    relation = "connect_to"
                elif subject_type == "ORG" and object_type == "ORG":
                    relation = "collaborates_with"
                elif object_type == "DATE":
                    relation = "mentioned_with"
                elif subject_type == "REGION":
                    relation = "located_in"
                elif subject_type == "PERSON" and object_type == "NORP":
                    relation = "is_a"
                      
                #append triple as a tuple
                triples.append((subject, relation, object_))
                
    
    return entities, triples

def generate_knowledge_graph(triples):
    # Create a directed graph
    graph = nx.DiGraph()

    # Add triples to the graph
    for triple in triples:
        subject, relation, object_ = triple
        graph.add_node(subject, label=subject, type='entity')
        graph.add_node(object_, label=object_, type='entity')  # Use object_ here
        graph.add_edge(subject, object_, label=relation)  # Use object_ here

    return graph


def display_entity_knowledge_graph(selected_entity, triples):
    entity_triples = []
    
    for triple in triples:
        subject, relation, object_ = triple
        if subject == selected_entity or object_ == selected_entity:
            entity_triples.append(triple)
    
    entity_knowledge_graph = generate_knowledge_graph(entity_triples)

    pos = nx.spring_layout(entity_knowledge_graph, seed=42, k=0.6)  # Adjust k parameter
    nx.draw_networkx(entity_knowledge_graph, pos, with_labels=True, node_size=2000, font_size=8, font_color='black')
    edge_labels = {(u, v): d['label'] for u, v, d in entity_knowledge_graph.edges(data=True)}
    nx.draw_networkx_edge_labels(entity_knowledge_graph, pos, edge_labels=edge_labels, font_size=6)
    plt.show()

def on_entity_selection(entity_combobox, unique_triples):
    selected_entity = entity_combobox.get()
    if selected_entity:
        display_entity_knowledge_graph(selected_entity, unique_triples)


# ========================================
#               Main
# ========================================

def main():
    pdf_path = "NSD_EMPLOYERS_HANDBOOK.pdf"  # File saved in same folder where code is
    text = extract_text_from_pdf(pdf_path) # function 1
    entities, triples = extract_entities_and_triples(text) # function 2

    unique_entities = set() # To store unique entities 

    # Filter out entities with labels other than "PERSON" and "ORG"
    filtered_entities = [(entity, label) for entity, label in entities if label in ["PERSON", "ORG"]]
    unique_entities = set(entity for entity, _ in filtered_entities)  # Extract unique entities
    
    print("Extracted Entities:")
    for entity, label in entities:
        print(f"{entity} ({label})")

    unique_triples = set()  # To store unique triples

    
    for triple in triples:
        unique_triples.add(triple)
    
    unique_triples = list(unique_triples)  # Convert set back to list
    
    print("\nGenerated Triples:")
    for triple in unique_triples:
        print(triple)
               
    ## Export triples to a CSV file
    # Generate timestamp
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    csv_file_1 = f"entities_{timestamp}.csv"
    with open(csv_file_1, "w", newline="", encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Entity", "Label"])  # Header row
        csv_writer.writerows(entities)
        
    print(f"Entities exported to {csv_file_1}")

    csv_file_2 = f"triples_{timestamp}.csv"
    with open(csv_file_2, "w", newline="", encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Subject", "Relation", "Object"])  # Header row
        csv_writer.writerows(unique_triples)

    print(f"Triples exported to {csv_file_2}")
    
    ## Generate the knowledge graph
    knowledge_graph = generate_knowledge_graph(unique_triples)

    # Draw the knowledge graph
    pos = nx.spring_layout(knowledge_graph, seed=42, k=0.6)  # You can change layout algorithms
    nx.draw_networkx(knowledge_graph, pos, with_labels=True, node_size=2000, font_size=4, font_color='black')
    edge_labels = {(u, v): d['label'] for u, v, d in knowledge_graph.edges(data=True)}
    nx.draw_networkx_edge_labels(knowledge_graph, pos, edge_labels=edge_labels, font_size=6)
    plt.show()

    ## Create the main window
    root = tk.Tk()
    root.title("Specific-Entity Knowledge Graph Visualization")
    
    # Create a Combobox to select entities
    entity_label = ttk.Label(root, text="Select Entity:")
    entity_label.pack(pady=10)
    
    entity_combobox = ttk.Combobox(root, values=list(unique_entities))  # Use unique_entities here
    entity_combobox.pack()
    
    ok_button = ttk.Button(root, text="OK", command=lambda: on_entity_selection(entity_combobox, unique_triples))
    ok_button.pack(pady=10)
    
    # Run the GUI main loop
    root.mainloop() 


### running main ###

if __name__ == "__main__":
    main()

