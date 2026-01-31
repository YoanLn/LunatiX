import vertexai
from vertexai.generative_models import GenerativeModel
from vertexai.language_models import TextEmbeddingModel
from typing import Dict, List
import json
from app.core.config import settings


class RAGService:
    """
    Retrieval-Augmented Generation service for insurance chatbot.
    Uses Vertex AI for embeddings and text generation.
    """

    def __init__(self):
        vertexai.init(
            project=settings.GOOGLE_CLOUD_PROJECT,
            location=settings.VERTEX_AI_LOCATION
        )
        self.text_model = GenerativeModel(settings.VERTEX_AI_MODEL_TEXT)
        self.embedding_model = TextEmbeddingModel.from_pretrained(
            settings.VERTEX_AI_EMBEDDING_MODEL
        )

        # Insurance knowledge base (in production, this would be in a vector DB)
        self.knowledge_base = self._load_knowledge_base()

    def _load_knowledge_base(self) -> List[Dict]:
        """
        Load insurance knowledge base.
        In production, this would be stored in a vector database like Vertex AI Vector Search.
        """
        return [
            {
                "topic": "deductible",
                "content": "A deductible is the amount you pay out of pocket before your insurance coverage kicks in. For example, if you have a $500 deductible and a claim for $2000, you pay $500 and insurance pays $1500."
            },
            {
                "topic": "premium",
                "content": "An insurance premium is the amount you pay (usually monthly or annually) to keep your insurance policy active. It's like a membership fee for your coverage."
            },
            {
                "topic": "copay",
                "content": "A copay (or copayment) is a fixed amount you pay for a covered service, typically paid at the time of service. Common for doctor visits and prescriptions."
            },
            {
                "topic": "claim process",
                "content": "The insurance claim process: 1) Submit claim with required documents, 2) Insurance reviews the claim, 3) Documents are verified, 4) Claim is approved or denied, 5) Payment is processed if approved."
            },
            {
                "topic": "coverage",
                "content": "Insurance coverage refers to the protection and benefits your policy provides. Different policies cover different events - read your policy carefully to understand what is and isn't covered."
            },
            {
                "topic": "beneficiary",
                "content": "A beneficiary is the person or entity you designate to receive insurance benefits, typically used in life insurance policies."
            },
            {
                "topic": "exclusion",
                "content": "An exclusion is a condition or circumstance that your insurance policy does not cover. Common exclusions include pre-existing conditions or intentional damage."
            },
            {
                "topic": "claim denial",
                "content": "A claim may be denied if: documents are incomplete, the incident isn't covered by your policy, you missed a filing deadline, or there are inconsistencies in your claim. You can usually appeal a denial."
            },
            {
                "topic": "required documents",
                "content": "Common required documents for claims: proof of identity, incident report (police/medical), receipts or invoices, photos of damage, proof of ownership, and completed claim forms."
            },
            {
                "topic": "claim status",
                "content": "Claim statuses: Submitted (received but not reviewed), Under Review (being processed), Additional Info Required (need more documents), Approved (claim accepted), Rejected (claim denied), Paid (payment processed)."
            }
        ]

    async def generate_response(
        self,
        query: str,
        user_id: str,
        session_id: str
    ) -> Dict:
        """
        Generate a response to user query using RAG.
        1. Find relevant context from knowledge base
        2. Generate response using context + query
        """
        try:
            # Get relevant context
            relevant_docs = await self._retrieve_relevant_context(query)

            # Create prompt with context
            context = "\n\n".join([doc["content"] for doc in relevant_docs])
            sources = [doc["topic"] for doc in relevant_docs]

            prompt = f"""
            You are a helpful insurance assistant. Use the following context to answer the user's question.
            If the context doesn't contain relevant information, provide a general helpful response but mention that the user should contact their insurance provider for specific details about their policy.

            Be friendly, clear, and concise. Explain insurance terms in simple language.

            Context:
            {context}

            User Question: {query}

            Response:
            """

            # Generate response
            response = self.text_model.generate_content(prompt)

            return {
                "response": response.text,
                "sources": json.dumps(sources),
                "sources_list": sources
            }

        except Exception as e:
            return {
                "response": f"I apologize, but I encountered an error processing your question. Please try rephrasing or contact support. Error: {str(e)}",
                "sources": "[]",
                "sources_list": []
            }

    async def _retrieve_relevant_context(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Retrieve relevant documents from knowledge base using semantic similarity.
        In production, this would use a vector database with proper embeddings.
        """
        try:
            # Get query embedding
            query_embedding = self.embedding_model.get_embeddings([query])[0].values

            # Simple keyword matching (in production, use vector similarity)
            query_lower = query.lower()
            relevant_docs = []

            for doc in self.knowledge_base:
                # Simple relevance score based on keyword matching
                score = 0
                if doc["topic"].lower() in query_lower:
                    score += 10

                # Check for related keywords
                keywords = doc["content"].lower().split()
                for word in query_lower.split():
                    if len(word) > 3 and word in keywords:
                        score += 1

                if score > 0:
                    relevant_docs.append((score, doc))

            # Sort by relevance and return top_k
            relevant_docs.sort(reverse=True, key=lambda x: x[0])

            # If no relevant docs found, return some default helpful docs
            if not relevant_docs:
                return self.knowledge_base[:3]

            return [doc for score, doc in relevant_docs[:top_k]]

        except Exception as e:
            # Fallback to returning first few docs
            return self.knowledge_base[:top_k]
