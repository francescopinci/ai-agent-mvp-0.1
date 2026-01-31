"""
RAG Helper for NomaTax
Retrieves relevant tax documents from Pinecone vector database
"""

import os
from dotenv import load_dotenv
from google import genai
from pinecone import Pinecone

load_dotenv()

INDEX_NAME = "nomatax-tax-docs"

def get_rag_context(user_summary, top_k=5):
    """
    Retrieve relevant tax documents based on user's situation.
    
    Args:
        user_summary: String containing user's tax situation summary
        top_k: Number of document chunks to retrieve (default 5)
    
    Returns:
        String with formatted RAG context to add to prompt
    """
    try:
        # Initialize APIs
        client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        index = pc.Index(INDEX_NAME)
        
        # Create embedding from user summary
        result = client.models.embed_content(
            model="models/text-embedding-004",
            contents=user_summary
        )
        query_embedding = [float(x) for x in result.embeddings[0].values]
        
        # Search Pinecone
        results = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
        
        # Format context
        if not results['matches']:
            return ""
        
        context_parts = []
        for i, match in enumerate(results['matches'], 1):
            source = match['metadata']['filename']
            text = match['metadata']['text']
            score = match['score']
            
            context_parts.append(f"**Source {i}: {source}** (relevance: {score:.2f})\n{text}")
        
        rag_context = "\n\n---\n\n".join(context_parts)
        
        return f"""

## 📚 ADDITIONAL REFERENCE DOCUMENTS (Retrieved from Official Tax Sources)

The following excerpts from official US and Italian tax documents are relevant to this case:

{rag_context}

---

"""
    
    except Exception as e:
        print(f"⚠️ RAG retrieval failed: {e}")
        return ""  # Fail gracefully - return empty string if RAG fails


# Example usage:
if __name__ == "__main__":
    # Test with sample user summary
    test_summary = """
    User is moving from US to Italy in 2026.
    US citizen with $120k salary.
    Planning to work remotely for US company.
    Has 1 child under 18.
    """
    
    context = get_rag_context(test_summary)
    print(context)
