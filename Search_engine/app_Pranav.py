import streamlit as st
import sqlite3
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Connect to the SQLite database
def connect_db(database_path):
    conn = sqlite3.connect(database_path)
    return conn

# Function to retrieve top 10 unique names based on query
def get_top_10_unique_names(query, conn, model):
    c = conn.cursor()
    query_embedding = model.encode([query])
    similarities = []
    c.execute("SELECT * FROM records")
    for row in c.fetchall():
        record_num, record_name, record_embeddings = row
        embeddings = json.loads(record_embeddings)
        embeddings = np.array(embeddings).reshape(1, -1)
        similarity = cosine_similarity(query_embedding, embeddings)[0][0]
        similarities.append((record_name, similarity))
    
    sorted_names = [name for name, _ in sorted(similarities, key=lambda x: x[1], reverse=True)]
    unique_names = []
    for name in sorted_names:
        if name not in unique_names:
            unique_names.append(name)
            if len(unique_names) == 10:
                break
    
    return unique_names

# Main function to run the Streamlit app
def main():
    st.title(':rainbow[Movie Title Search Engine by Pranav]:sunglasses:')
    st.header(':orange[Enter words related to movie!]', divider='rainbow')
    query = st.text_input('Enter your query:')
    
    if st.button('Search'):
        if query:
            conn = connect_db('chroma.sqlite3')
            model = SentenceTransformer('bert-base-nli-mean-tokens')
            top_10_unique_names = get_top_10_unique_names(query, conn, model)
            st.write('Top 10 Unique Names:')
            for i, (name) in enumerate(top_10_unique_names, start=1):
                st.write(f"{i}. {name}")
            # for name in top_10_unique_names:
            #     st.write(name)
            conn.close()

if __name__ == '__main__':
    main()
