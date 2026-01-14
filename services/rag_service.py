from utils.vector_client import search_business_knowledge

def query_business_knowledge(business_id: str, question: str, n_results: int = 3):
    """
    Retrieves the most relevant knowledge chunks for a business using Supabase Vector.
    """
    results = search_business_knowledge(business_id, question, limit=n_results)
    return [row["content"] for row in results]