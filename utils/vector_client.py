import os
import uuid
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# ---------------------------------------------------------
# FAKE EMBEDDING (no OpenAI required)
# ---------------------------------------------------------
def embed_text(text: str):
    # 1536‑dimensional zero vector (same size as OpenAI embeddings)
    return [0.0] * 1536


# ---------------------------------------------------------
# INSERT KNOWLEDGE
# ---------------------------------------------------------
def store_business_knowledge(business_id: str, content: str):
    embedding = embed_text(content)

    payload = {
        "id": str(uuid.uuid4()),
        "business_id": business_id,
        "content": content,
        "embedding": embedding
    }

    url = f"{SUPABASE_URL}/rest/v1/business_knowledge"
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code >= 300:
        print("Error inserting knowledge:", response.text)
        raise Exception("Failed to insert knowledge")

    return response.json()


# ---------------------------------------------------------
# VECTOR SEARCH (disabled but returns empty list safely)
# ---------------------------------------------------------
def search_business_knowledge(business_id: str, query: str, limit: int = 5):
    # No real vector search without embeddings
    # Return empty results so your app doesn't break
    return []