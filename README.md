# E-Commerce FAQ AI Chatbot 🤖🛒

**E-Commerce FAQ AI Chatbot** is an advanced AI-based solution designed to enhance user experience by providing accurate and instant answers to frequently asked questions about your e-commerce platform. It uses Google Generative AI and FAISS for efficient question-answering and contextual responses.

---

## 🚀 Features

- **AI-Powered Responses:** Uses Google Generative AI (Gemini-1.5) to deliver accurate and contextually relevant answers.
- **Custom FAQ Support:** Handles a wide range of FAQs tailored to your e-commerce platform.
- **Efficient Search:** Integrates FAISS (Facebook AI Similarity Search) for quick and precise retrieval of relevant responses.
- **Scalable Architecture:** Designed to accommodate large datasets of questions and answers.
- **Friendly Interface:** User-friendly chatbot interface powered by Flask for seamless interactions.

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**
- **Google Generative AI API Key** (sign up at [Google Cloud Generative AI](https://cloud.google.com/generative-ai))
- Required Python Libraries:
  - `Flask`
  - `google-generativeai`
  - `pandas`
  - `numpy`
  - `faiss`
  - `langchain-google-genai`

---

## 📦 Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Babaiii07/Finetuning_GEMINI_on_custom_ecommerce_data
   cd Finetuning_GEMINI_on_custom_ecommerce_data

Install Dependencies:

pip install -r requirements.txt
Prepare Your Data:

Create a CSV file named Ecommerce_FAQs.csv with two columns: prompt (questions) and response (answers).
Place it in the project root directory.
Set Up Environment Variables:

Add your Google Generative AI API key in the script:
python
api_key = "your-gemini-api-key"
Run the Application:


python wsgi.py
Access the Chatbot:

Open your browser and visit: http://127.0.0.1:5000/.

📝 Usage
1. User Interaction:
Open the chatbot interface.
Ask questions about your e-commerce platform, such as:
"What is the return policy?"
"How can I track my order?"
"What payment methods do you accept?"
Receive accurate and contextually relevant answers instantly.
2. How It Works:
Embedding Questions: The questions in your FAQ dataset are embedded using GoogleGenerativeAIEmbeddings.
FAISS Indexing: A FAISS index is created to efficiently search for the most relevant questions.
Contextual Answering: Using the Gemini model, the bot generates an accurate response based on the retrieved context.
🛠️ Project Architecture
FAISS Indexing:

Creates an index of embedded questions for efficient similarity search.
Facilitates quick retrieval of relevant FAQs.
Google Generative AI:

Generates human-like answers based on the FAQ context and user queries.
Flask Web Interface:

Provides an intuitive interface for user interaction with the chatbot.
Data Pipeline:

Loads the FAQ dataset (Ecommerce_FAQs.csv).
Embeds questions and creates a persistent FAISS index for retrieval.


🌟 Example FAQs
Question	                    Answer
What is your return policy?	You can return items within 30 days of purchase.
How can I track my order?	Use the tracking ID sent to your email to track your order.
What payment methods do you accept?	We accept credit cards, PayPal, and bank transfers.


🤝 Contributing
Contributions are welcome! If you'd like to add features or improve the project:

Fork the repository.
Create a new branch: git checkout -b feature/YourFeatureName.
Commit your changes: git commit -m 'Add some feature'.
Push to the branch: git push origin feature/YourFeatureName.
Open a pull request.
🙏 Acknowledgements
FAISS
Google Generative AI
Flask
LangChain
