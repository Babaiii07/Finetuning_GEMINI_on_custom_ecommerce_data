document.getElementById('send-btn').addEventListener('click', async () => {
    const input = document.getElementById('user-input');
    const userMessage = input.value.trim();
    if (!userMessage) return;

    // Add user message
    addMessage(userMessage, 'user-message');

    // Clear input field
    input.value = '';

    // Fetch response
    const response = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userMessage }),
    });
    const data = await response.json();

    // Add bot response
    addMessage(data.answer, 'bot-message');
});

function addMessage(text, className) {
    const chatBody = document.getElementById('chat-body');
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${className}`;
    bubble.textContent = text;
    chatBody.appendChild(bubble);
    chatBody.scrollTop = chatBody.scrollHeight; // Auto-scroll to the latest message
}
const express = require('express');
const bodyParser = require('body-parser');
const faiss = require('faiss-node');
const { GoogleAuth } = require('google-auth-library');
const fs = require('fs');
const path = require('path');
const csv = require('pandas-js');

// Initialize Express App
const app = express();
app.use(bodyParser.json());
app.use(express.static('public'));

// Configure Google API Key
const apiKey = "AIzaSyANdlRmC_bLlVXuAwTfCOfSwZNFYWy1ZGw";
const auth = new GoogleAuth({ key: apiKey });

// Load FAQ Data
const faqFilePath = path.join(__dirname, 'Ecommerce_FAQs.csv');
const faqData = csv.read_csv(faqFilePath, { encoding: 'utf-8' });

const questions = faqData['prompt'].map(q => q.trim());
const answers = faqData['response'];

// Embed Questions Using Google Generative AI
const embedDocuments = async (texts) => {
    // Simulated embeddings logic; replace with actual API calls if supported
    return texts.map(text => {
        const embedding = new Array(768).fill(0).map(() => Math.random());
        return embedding;
    });
};

(async () => {
    const questionEmbeddings = await embedDocuments(questions);

    // Create FAISS Index
    const embeddingDimension = questionEmbeddings[0].length;
    const faissIndex = new faiss.IndexFlatL2(embeddingDimension);

    // Add Embeddings to the Index
    questionEmbeddings.forEach(embedding => {
        faissIndex.add(embedding);
    });

    // Save FAISS Index to Disk
    fs.writeFileSync('./faiss_index.index', JSON.stringify(faissIndex.serialize()));
    console.log('FAISS index created and saved.');
})();

// Retrieve Answers Based on Query
const getResponse = async (query) => {
    if (query.toLowerCase().includes('hello') || query.toLowerCase().includes('hi')) {
        return "Hello! Welcome to Shoppe.";
    } else {
        const faissIndexPath = './faiss_index.index';

        if (!fs.existsSync(faissIndexPath)) {
            throw new Error('FAISS index file not found. Please run the initialization script first.');
        }

        const serializedIndex = JSON.parse(fs.readFileSync(faissIndexPath));
        const faissIndex = faiss.deserialize(serializedIndex);

        // Embed the Query
        const queryEmbedding = await embedDocuments([query]);
        const k = 5;

        // Search in FAISS
        const results = faissIndex.search(queryEmbedding[0], k);
        const indices = results.labels;
        const relevantQuestions = indices.map(i => questions[i]);
        const relevantAnswers = indices.map(i => answers[i]);

        const context = relevantQuestions.map((q, i) => `Q: ${q}\nA: ${relevantAnswers[i]}`).join('\n');

        // Generate Response Using Context
        return context || "I don't know.";
    }
};

// Define Routes
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'chatbot.html'));
});

app.post('/ask', async (req, res) => {
    const query = req.body.query;

    if (query) {
        const answer = await getResponse(query);
        return res.json({ answer });
    }

    return res.json({ answer: "I didn't understand that." });
});

// Start the Server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
