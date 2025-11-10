# 🛍️ Vibe Matcher

A smart recommendation app that matches products to your vibe, not just your search terms. Built with Python, Streamlit, and Sentence Transformers.

This app is a prototype submission that fulfills all requirements of the "Vibe Matcher" challenge, including a full web app, testing suite, and project reflection.

### [➡️ Click here to see the live demo!](httpsit-vibematcher-app-py-89x3.streamlit.app)

---

## ✨ Features

* **Vibe-Based Search:** Input abstract feelings like "cozy rainy day" or "cyberpunk street market" to get real product matches.
* **Interactive UI:** A custom-built "Gameboy" terminal interface shows you results in real-time.
* **Clickable Inspiration:** Get started instantly with example vibe buttons.
* **Built-in Evaluation:** A "Test & Evaluation" tab runs automated tests to validate the model's accuracy.
* **Project Documentation:** A "Submission Docs" tab contains the full project reflection and introduction.

---

## 🤖 How It Works

1.  **Embeddings:** At startup, the app uses the `all-mpnet-base-v2` model to convert a list of product descriptions into numerical vectors (embeddings).
2.  **Query:** When you enter a vibe, your query is also converted into a vector.
3.  **Vector Search:** The app uses **Cosine Similarity** to find the product vectors that are "closest" in meaning to your query vector.
4.  **Display:** The top 3 (or more) matches are ranked by their score and displayed in the terminal.

---

## 🛠️ Tech Stack

* **Backend:** Python
* **Frontend:** Streamlit
* **AI/ML:** Sentence Transformers (`all-mpnet-base-v2`)
* **Vector Math:** Scikit-learn (Cosine Similarity)
* **Data:** Pandas

---

## 🚀 How to Run Locally

1.  **Clone the repository:**
    
    git clone [https://github.com/SamparkBhol/vibematcher.git](https://github.com/SamparkBhol/vibematcher.git)
    cd vibematcher

2.  **Create and activate a virtual environment:**
    
    python -m venv venv
    .\venv\Scripts\activate

3.  **Install the requirements:**
    
    pip install -r requirements.txt

4.  **Run the app:**
    
    streamlit run app.py
