import os
from supabase import create_client, Client
from openai import OpenAI

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed_text(text: str):
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def store_business_knowledge(business_id: str, content: str):
    embedding = embed_text(content)
    supabase.table("business_knowledge").insert({
        "business_id": business_id,
        "content": content,
        "embedding": embedding
    }).execute()

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

    result = supabase.rpc(
        "exec_sql",
        {
            "sql": sql,
            "params": [query_embedding, business_id, query_embedding, limit]
        }
    ).execute()

    return result.data