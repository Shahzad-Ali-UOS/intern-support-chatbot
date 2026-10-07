import json
import os
from typing import Dict, List, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SupportRetriever:
    """NLP Semantic Retrieval Engine over FAQ documents and intent classifier."""

    def __init__(self, faq_path: str = "data/faq_knowledge_base.json"):
        with open(faq_path, "r", encoding="utf-8") as f:
            self.faq_data: List[Dict] = json.load(f)

        # Build corpus by combining question, answer, and keywords for rich representation
        self.corpus = [
            f"{item['question']} {' '.join(item.get('keywords', []))} {item['answer']}"
            for item in self.faq_data
        ]

        self.vectorizer = TfidfVectorizer(token_pattern=r'(?u)\b[\w-]+\b', stop_words='english')
        self.faq_vectors = self.vectorizer.fit_transform(self.corpus)

    def retrieve(self, query: str, top_k: int = 1) -> List[Tuple[Dict, float]]:
        """Returns top matching FAQs with confidence scores (0.0 to 1.0)."""
        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.faq_vectors)[0]

        top_indices = np.argsort(scores)[::-1][:top_k]
        results = []
        for idx in top_indices:
            score = float(scores[idx])
            results.append((self.faq_data[idx], round(score, 3)))
        return results

    def infer_category_and_priority(self, query: str) -> Tuple[str, str]:
        """Infers support ticket category and priority heuristic."""
        q_lower = query.lower()
        
        # Priority rules
        if any(w in q_lower for w in ["cannot login", "locked", "error 500", "urgent", "failed", "crash"]):
            priority = "High"
        elif any(w in q_lower for w in ["deadline", "extension", "certificate", "transfer"]):
            priority = "Medium"
        else:
            priority = "Low"

        # Category detection
        if any(w in q_lower for w in ["submit", "submission", "github", "deadline", "task"]):
            category = "Task Submission"
        elif any(w in q_lower for w in ["certificate", "lor", "completion", "recommendation"]):
            category = "Certification"
        elif any(w in q_lower for w in ["login", "password", "lms", "portal", "account", "access"]):
            category = "Portal & LMS Access"
        else:
            category = "Technical Tracks"

        return category, priority