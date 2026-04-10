"""Service to configure Azure AI Search management clients."""

from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient, SearchIndexerClient

from src.config.settings import AISearchSettings


class SearchIndexService:
    """Wrapper for the Azure AI Search index management client."""

    def __init__(self) -> None:
        """Initialize the SearchIndexService with Azure AI Search clients."""
        AISearchSettings.validate()
        credential = AzureKeyCredential(AISearchSettings.get_api_key())
        self._client = SearchIndexClient(
            endpoint=AISearchSettings.get_endpoint(),
            credential=credential,
        )
        self._indexer_client = SearchIndexerClient(
            endpoint=AISearchSettings.get_endpoint(),
            credential=credential,
        )

    def get_client(self) -> SearchIndexClient:
        """Return the SearchIndexClient for index management operations."""
        return self._client

    def get_indexer_client(self) -> SearchIndexerClient:
        """Return the SearchIndexerClient for indexer management operations."""
        return self._indexer_client

    def get_index_name(self) -> str:
        """Return the default index name from settings."""
        return AISearchSettings.get_index_name()
