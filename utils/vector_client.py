import os
import requests
from openai import OpenAI

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def embed_text(text: str):
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


# ---------------------------------------------------------
# INSERT KNOWLEDGE
# ---------------------------------------------------------
def store_business_knowledge(business_id: str, content: str):
    embedding = embed_text(content)

    payload = {
        "business_id": business_id,
        "content": content,
        "embedding": embedding
    }

    url = f"{SUPABASE_URL}/rest/v1/business_knowledge"
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code >= 300:
        print("Error inserting knowledge:", response.text)

    return response.json()


# ---------------------------------------------------------
# VECTOR SEARCH
# ---------------------------------------------------------
def search_business_knowledge(business_id: str, query: str, limit: int = 5):
    query_embedding = embed_text(query)

    sql = """
        select content,
               1 - (embedding <=> %s) as similarity
        from business_knowledge
        where business_id = %s
        order by embedding <=> %s
        limit %s;
    """

    rpc_payload = {
        "sql": sql,
        "params": [query_embedding, business_id, query_embedding, limit]
    }

    url = f"{SUPABASE_URL}/rest/v1/rpc/exec_sql"
    response = requests.post(url, json=rpc_payload, headers=headers)

    if response.status_code >= 300:
        print("Error running vector search:", response.text)

    return response.json()