import google.generativeai as genai
import pandas as pd
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import numpy as np
import faiss
import os
api_key = "AIzaSyANdlRmC_bLlVXuAwTfCOfSwZNFYWy1ZGw"
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
        print("Hello, Good Day, welcome to shope.")
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

if __name__ == '__main__':
    while True:
        query = input("Enter a question: ")
        print(get_response(query))
