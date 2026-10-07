import random
from typing import Dict, Optional
from engine.retriever import SupportRetriever

CONFIDENCE_THRESHOLD = 0.28  # Below this threshold, prompt ticket escalation

class InternSupportBot:
    """Internship AI Support Assistant with confidence-governed ticket escalation."""

    def __init__(self, faq_path: str = "data/faq_knowledge_base.json"):
        self.retriever = SupportRetriever(faq_path=faq_path)

    def answer_query(
        self,
        query: str,
        llm_provider: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> Dict:
        # 1. Retrieve most relevant FAQ
        matches = self.retriever.retrieve(query, top_k=1)
        best_match, score = matches[0] if matches else (None, 0.0)
        category, priority = self.retriever.infer_category_and_priority(query)

        # 2. Check if query is high-confidence or requires escalation
        is_escalated = score < CONFIDENCE_THRESHOLD

        if is_escalated:
            ticket_id = f"TCK-{random.randint(2000, 9999)}"
            response_text = (
                f"I couldn't locate an exact policy match in our internship knowledge base for your inquiry "
                f"(Confidence: {int(score * 100)}%).\n\n"
                f"To ensure you receive accurate guidance, I have drafted an **Escalation Support Ticket** ({ticket_id}) "
                f"routed to the **{category} Lead** with **{priority} Priority**."
            )
            return {
                "answer": response_text,
                "confidence": score,
                "is_escalated": True,
                "ticket": {
                    "ticket_id": ticket_id,
                    "query": query,
                    "category": category,
                    "priority": priority,
                    "status": "Escalated to Mentor"
                },
                "source_faq": None
            }

        # 3. High confidence: Synthesize Answer
        # If API key provided, refine via LLM
        if api_key and llm_provider in ["Groq", "OpenAI"]:
            try:
                llm_response = self._synthesize_with_llm(query, best_match, llm_provider, api_key)
                return {
                    "answer": llm_response,
                    "confidence": score,
                    "is_escalated": False,
                    "ticket": None,
                    "source_faq": best_match
                }
            except Exception as e:
                print(f"[Warning] LLM call failed: {e}. Falling back to RAG answer.")

        # Grounded RAG Fallback
        response_text = (
            f"{best_match['answer']}\n\n"
            f"*Source Policy Reference:* `{best_match['id']} - {best_match['category']}`"
        )
        return {
            "answer": response_text,
            "confidence": score,
            "is_escalated": False,
            "ticket": None,
            "source_faq": best_match
        }

    def _synthesize_with_llm(self, query: str, context_faq: Dict, provider: str, api_key: str) -> str:
        prompt = f"""
You are the official internee.pk AI Internship Assistant.
Answer the intern's question accurately, concisely, and warmly based ONLY on the verified policy context below.

Policy Context:
- Category: {context_faq['category']}
- Verified Question: {context_faq['question']}
- Official Policy: {context_faq['answer']}

Intern Query: "{query}"

Format: Provide a direct, professional answer and cite the policy section '{context_faq['id']}'.
"""
        if provider == "Groq":
            from groq import Groq
            client = Groq(api_key=api_key)
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            return resp.choices[0].message.content

        elif provider == "OpenAI":
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            return resp.choices[0].message.content
        return context_faq['answer']