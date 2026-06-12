"""
Lab 04 - Build All Clear RAG Pipeline
RetrieveAgent: RAG agent that uses SearchTool to answer incident-triage
questions with citations.

This module provides a RetrieveAgent class that implements a Retrieval-Augmented
Generation (RAG) pattern: search for relevant runbooks/SOPs, build context, and
generate a response with citations for ActionAgent.search_knowledge.

RAG Pattern Benefits:
- Grounds LLM responses in actual source records (reduces hallucination)
- Provides traceable citations for verification
- Allows the LLM to answer questions about private/recent data

Azure SDK Documentation:
- AsyncAzureOpenAI: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/switching-endpoints
- Embeddings API: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/embeddings
- Chat Completions: https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/chatgpt
"""

from typing import Any

from openai import AsyncAzureOpenAI

from search_tool import SearchTool


class RetrieveAgent:
    """
    A RAG agent that retrieves relevant incident knowledge and generates
    responses with citations.

    The agent follows the RAG pattern:
    1. Search for relevant runbooks/SOPs using hybrid search
    2. Build a context from the retrieved source records
    3. Generate a response using an LLM with the context
    4. Include citations to source records
    """

    def __init__(
        self,
        search_tool: SearchTool,
        llm_client: AsyncAzureOpenAI,
        model_deployment: str = "gpt-4.1",
    ) -> None:
        """
        Initialize the RetrieveAgent.

        Args:
            search_tool: A SearchTool instance for performing searches.
            llm_client: An AsyncAzureOpenAI client for generating responses.
            model_deployment: The name of the model deployment to use.
        """
        # Store dependencies for use in retrieve() method
        self.search_tool = search_tool
        self.llm_client = llm_client
        self.model_deployment = model_deployment

    async def _get_embedding(self, text: str) -> list[float]:
        """
        Generate an embedding vector for the given text.

        Args:
            text: The text to embed.

        Returns:
            A list of floats representing the embedding vector.
        """
        # Generate embedding using Azure OpenAI embeddings API
        response = await self.llm_client.embeddings.create(
            model="text-embedding-ada-002", input=text
        )
        # Return the embedding vector (1536 dimensions for ada-002)
        return response.data[0].embedding

    def _build_context(self, search_results: list[dict[str, Any]]) -> str:
        """
        Build a context string from search results for the LLM prompt.

        Args:
            search_results: List of search result dictionaries.

        Returns:
            A formatted string containing retrieved context with source records.
        """
        if not search_results:
            return "No relevant context found."

        context_parts = []
        for i, result in enumerate(search_results, start=1):
            title = result.get("title", "Unknown")
            content = result.get("content", "")
            context_parts.append(f"[Source {i}] {title}\n{content}")

        return "\n\n".join(context_parts)

    def _build_prompt(self, query: str, context: str) -> str:
        """
        Build the prompt for the LLM including the context and query.

        Args:
            query: The user's question.
            context: The retrieved context from search results.

        Returns:
            A formatted prompt string for the LLM.
        """
        return f"""Use the following All Clear incident-triage context to answer the question. Include citations using [Source N] format. Constitution Article IV applies: no citation, no claim. If the context doesn't contain enough information to answer, say "I don't know based on the provided context" and escalate uncertainty.

Context:
{context}

Question: {query}

Answer:"""

    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> dict[str, Any]:
        """
        Retrieve relevant source records and generate a response with citations.

        This is the main RAG pipeline method that orchestrates:
        1. Embedding the query
        2. Searching for relevant runbooks/SOPs
        3. Building context from results
        4. Generating a response with the LLM

        Args:
            query: The incident-triage question.
            top_k: Number of documents to retrieve (default: 5).

        Returns:
            A dictionary containing:
            - answer: The generated response with citations
            - sources: List of source records used
            - query: The original query
        """
        # Step 1: Get the embedding for the query
        query_vector = await self._get_embedding(query)

        # Step 2: Search for relevant runbooks/SOPs using hybrid search
        search_results = await self.search_tool.search(
            query=query, query_vector=query_vector, top_k=top_k
        )

        # Step 3: Build context from search results
        context = self._build_context(search_results)

        # Step 4: Build the prompt with context and query
        prompt = self._build_prompt(query, context)

        # Step 5: Generate response using the LLM
        response = await self.llm_client.chat.completions.create(
            model=self.model_deployment,
            messages=[
                {
                    "role": "system",
                    "content": "You support All Clear ActionAgent.search_knowledge. Answer only from provided context and cite every factual claim.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )

        # Step 6: Extract the answer from the LLM response
        answer = response.choices[0].message.content

        # Step 7: Return the result dictionary
        return {
            "answer": answer,
            "sources": search_results,
            "query": query,
        }
