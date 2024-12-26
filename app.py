from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import pandas as pd
import numpy as np
import faiss
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings

app = Flask(__name__)

api_key = "your gemini api key"
genai.configure(api_key=api_key)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)

faq_data = pd.read_csv('Ecommerce_FAQs.csv', encoding='cp1252')

faq_data.columns = faq_data.columns.str.strip()
questions = faq_data['prompt'].tolist()  
answers = faq_data['response'].tolist() 

question_embeddings = embeddings.embed_documents(questions)

print(question_embeddings[:5])

embedding_dimension = len(question_embeddings[0])
faiss_index = faiss.IndexFlatL2(embedding_dimension) 
faiss_index.add(np.array(question_embeddings))

faiss.write_index(faiss_index, './faiss_index.index')
print("FAISS index created and saved.")

def get_response(query):
    if "hello" in query.lower() or "hi" in query.lower():
        return " Hello! welcome to shoppe"
    else:
        if not os.path.exists('./faiss_index.index'):
            raise FileNotFoundError("FAISS index file not found. Please run create_vectordb() first.")

        faiss_index = faiss.read_index('./faiss_index.index')
        query_embedding = embeddings.embed_query(query)
        k = 5 
        distances, indices = faiss_index.search(np.array([query_embedding]), k)
        relevant_questions = [questions[i] for i in indices[0]]
        relevant_answers = [answers[i] for i in indices[0]]
        context = "\n".join([f"Q: {q}\nA: {a}" for q, a in zip(relevant_questions, relevant_answers)])

        prompt_template = """Given the following context and a question, generate an answer based on this context only.
        In the answer, try to use as much text as possible from the source document context without making any changes.
        If the answer is not found in the context, kindly state "I don't know." Don't try to fabricate an answer.

        CONTEXT: {context}

        QUESTION: {question}"""
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt_template.format(context=context, question=query))

        return response.text

@app.route('/')
def chatbot():
    return render_template('chatbot.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    query = data.get('query')
    if query:
        response = get_response(query)
        return jsonify({"answer": response})
    return jsonify({"answer": "I didn't understand that."})
