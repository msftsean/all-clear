"""
Lab 04 - Build All Clear RAG Pipeline
SearchTool: Hybrid search over Azure AI Search

This module provides a SearchTool class that performs hybrid search
(combining keyword and vector search) against an Azure AI Search index of
All Clear incident runbooks, SOPs, and response procedures.

Key Concepts:
- Vector search: Uses embeddings to find semantically similar content
- Keyword search: Traditional BM25-based text matching
- Hybrid search: Combines both approaches using Reciprocal Rank Fusion (RRF)

Azure SDK Documentation:
- SearchClient: https://learn.microsoft.com/en-us/python/api/azure-search-documents/azure.search.documents.searchclient
- VectorizedQuery: https://learn.microsoft.com/en-us/python/api/azure-search-documents/azure.search.documents.models.vectorizedquery
"""

from typing import Any

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery


class SearchTool:
    """
    A tool for performing hybrid search over All Clear incident knowledge.

    Hybrid search combines traditional keyword-based search with
    vector similarity search for improved relevance.
    """

    def __init__(
        self,
        endpoint: str,
        index_name: str,
        credential: AzureKeyCredential,
    ) -> None:
        """
        Initialize the SearchTool.

        Args:
            endpoint: The Azure AI Search service endpoint URL.
            index_name: The name of the search index to query.
            credential: Azure credential for authentication.
        """
        # Store configuration for debugging and client creation
        self.endpoint = endpoint
        self.index_name = index_name
        self.credential = credential

        # Create SearchClient - handles connection pooling and retries automatically
        self.client = SearchClient(
            endpoint=endpoint, index_name=index_name, credential=credential
        )

    async def search(
        self,
        query: str,
        query_vector: list[float],
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Perform hybrid search combining keyword and vector search.

        Args:
            query: The incident-triage text query for keyword search.
            query_vector: The embedding vector for vector search.
            top_k: Number of results to return (default: 5).

        Returns:
            A list of search results, each containing source-record content
            and metadata (id, title, chunk, score).
        """
        # Create VectorizedQuery for semantic search
        vector_query = VectorizedQuery(
            vector=query_vector, k_nearest_neighbors=top_k, fields="content_vector"
        )

        # Perform hybrid search (keyword + vector combined via RRF)
        results = self.client.search(
            search_text=query,
            vector_queries=[vector_query],
            top=top_k,
            select=["id", "title", "snippet", "content", "queue", "category"],
        )

        # Process results into list of dictionaries
        search_results = []
        for result in results:
            search_results.append(
                {
                    "id": result.get("id"),
                    "title": result.get("title"),
                    "snippet": result.get("snippet"),
                    "content": result.get("content"),
                    "queue": result.get("queue"),
                    "category": result.get("category"),
                    "score": result.get("@search.score", 0.0),
                }
            )

        return search_results
