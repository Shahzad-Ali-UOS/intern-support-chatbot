# data_init.py
import pandas as pd

tickets = [
    {"ticket_id": "TCK-1001", "query": "My task submission link shows invalid URL error on portal", "category": "Task Submission", "priority": "High", "status": "Resolved"},
    {"ticket_id": "TCK-1002", "query": "When will the machine learning certificates be dispatched?", "category": "Certification", "priority": "Medium", "status": "Resolved"},
    {"ticket_id": "TCK-1003", "query": "Forgot password email not arriving in inbox", "category": "Portal & LMS Access", "priority": "High", "status": "Resolved"},
    {"ticket_id": "TCK-1004", "query": "Need help installing PyTorch CUDA version on Windows", "category": "Technical Tracks", "priority": "Low", "status": "Resolved"},
    {"ticket_id": "TCK-1005", "query": "Can I get a 2 day extension for semester final exams?", "category": "Task Submission", "priority": "Medium", "status": "Resolved"},
    {"ticket_id": "TCK-1006", "query": "How to verify certificate ID on national portal?", "category": "Certification", "priority": "Low", "status": "Resolved"},
    {"ticket_id": "TCK-1007", "query": "Want to switch from web dev to machine learning track", "category": "Technical Tracks", "priority": "Medium", "status": "Resolved"},
    {"ticket_id": "TCK-1008", "query": "LMS dashboard displays HTTP 500 error when clicking modules", "category": "Portal & LMS Access", "priority": "High", "status": "Resolved"}
]

df = pd.DataFrame(tickets)
df.to_csv("data/support_tickets.csv", index=False)
print("[SUCCESS] Created data/support_tickets.csv")