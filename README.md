# 💬 AI Intern Support Chatbot & Ticket Escalation Cockpit

An intelligent natural language processing (NLP) and retrieval-augmented generation (RAG) support platform designed for internship programs. The system automates real-time query resolution using verified FAQ knowledge bases, evaluates semantic retrieval confidence, and automatically dispatches structured support escalation tickets when queries require human mentor intervention.

---

## 📌 Key Capabilities

- **NLP Semantic Retrieval (RAG):** Uses TF-IDF vectorization and cosine similarity over policy documents to provide grounded, source-cited responses (tasks, deadlines, LMS access, certificates, track policies).
- **Confidence-Governed Escalation:** Automatically calculates retrieval relevance scores. Queries scoring below the threshold are routed into structured escalation tickets with categorized priority ratings (`High`, `Medium`, `Low`).
- **Dual-Engine Response Generation:**
  - **Cloud LLM Support:** Direct integration with **Groq (LLaMA 3.3)** or **OpenAI (GPT-4o-mini)** for contextual natural dialogue.
  - **Zero-Cost Offline Mode:** Native deterministic RAG response synthesis that works out of the box without requiring API keys.
- **Executive Support Cockpit:** Dark-mode UI with live SLA tracking, automated ticket queue drawers, and Plotly historical ticket category analytics.
- **Audit & Ticket Export:** Export active escalation queues to CSV for mentor review.

---

## 🛠 Tech Stack

- **Language:** Python 3.10+
- **NLP & Retrieval:** Scikit-Learn (`TfidfVectorizer`, `cosine_similarity`)
- **LLM Integrations:** `groq`, `openai`
- **Dashboard & Analytics:** Streamlit, Plotly (`express`, `graph_objects`)
- **Data Engineering:** Pandas, NumPy, JSON

---

## 📂 Repository Structure

```text
intern_support_chatbot/
├── data/
│   ├── faq_knowledge_base.json  # Structured FAQ policies and category tags
│   └── support_tickets.csv      # Historical support ticket dataset
├── engine/
│   ├── __init__.py
│   ├── retriever.py             # NLP semantic search & intent classifier
│   └── bot_engine.py            # RAG synthesis & ticket escalation engine
├── app.py                       # Interactive Streamlit support cockpit
├── data_init.py                 # Data seeding script
├── test_bot.py                  # Headless verification script
├── requirements.txt             # Project dependencies
└── README.md                    # Documentation