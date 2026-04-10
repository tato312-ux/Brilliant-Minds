"""Provisioning helpers for the multimodal-ready rag-v3 pipeline.

rag-v3 extends rag-v2 with extra fields that can later store image references,
captions, and section/source metadata. The first version intentionally keeps
the text ingestion path stable so the team can activate multimodal evidence in
small steps.
"""

from azure.search.documents.indexes.models import (
    AzureOpenAIEmbeddingSkill,
    ChatCompletionSkill,
    CommonModelParameters,
    DocumentIntelligenceLayoutSkill,
    DocumentIntelligenceLayoutSkillChunkingProperties,
    DocumentIntelligenceLayoutSkillChunkingUnit,
    DocumentIntelligenceLayoutSkillExtractionOptions,
    DocumentIntelligenceLayoutSkillOutputFormat,
    DocumentIntelligenceLayoutSkillOutputMode,
    FieldMapping,
    HnswAlgorithmConfiguration,
    IndexProjectionMode,
    IndexingParameters,
    InputFieldMappingEntry,
    OutputFieldMappingEntry,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SearchIndexer,
    SearchIndexerDataContainer,
    SearchIndexerDataSourceConnection,
    SearchIndexerIndexProjection,
    SearchIndexerIndexProjectionSelector,
    SearchIndexerIndexProjectionsParameters,
    SearchIndexerKnowledgeStore,
    SearchIndexerKnowledgeStoreFileProjectionSelector,
    SearchIndexerKnowledgeStoreProjection,
    SearchIndexerSkillset,
    SearchableField,
    SemanticConfiguration,
    SemanticField,
    SemanticPrioritizedFields,
    SemanticSearch,
    SimpleField,
    VectorSearch,
    VectorSearchProfile,
)

from src.config.settings import (
    BlobStorageSettings,
    LayoutRagSettings,
    OpenAISettings,
    RagV3Settings,
    AzureOpenAISettings
)
from src.services.search.search_index_service import SearchIndexService


class RagV3Provisioner:
    """Creates a rag-v3 index with visual-ready fields over the rag-v2 base."""

    def __init__(self) -> None:
        BlobStorageSettings.validate()
        self._service = SearchIndexService()

    def _build_datasource(self) -> SearchIndexerDataSourceConnection:
        return SearchIndexerDataSourceConnection(
            name=RagV3Settings.DATASOURCE_NAME,
            type="azureblob",
            connection_string=BlobStorageSettings.CONNECTION_STRING or "",
            container=SearchIndexerDataContainer(name=BlobStorageSettings.AZURE_STORAGE_CONTAINER or ""),
        )

    def _build_index(self) -> SearchIndex:
        fields = [
            SearchableField(
                name="chunk_id",
                key=True,
                filterable=True,
                sortable=True,
                analyzer_name="keyword",
            ),
            SimpleField(
                name="parent_id",
                type=SearchFieldDataType.String,
                filterable=True,
                sortable=True,
            ),
            SimpleField(
                name="document_title",
                type=SearchFieldDataType.String,
                filterable=True,
                sortable=True,
            ),
            SimpleField(
                name="metadata_storage_path",
                type=SearchFieldDataType.String,
                filterable=True,
                sortable=True,
            ),
            SimpleField(
                name="page_number",
                type=SearchFieldDataType.Int32,
                filterable=True,
                sortable=True,
            ),
            SearchableField(name="content", type=SearchFieldDataType.String),
            SearchableField(name="layout_text", type=SearchFieldDataType.String),
            SearchableField(name="image_caption", type=SearchFieldDataType.String),
            SimpleField(
                name="image_path",
                type=SearchFieldDataType.String,
                filterable=True,
            ),
            SimpleField(
                name="source_kind",
                type=SearchFieldDataType.String,
                filterable=True,
            ),
            SimpleField(
                name="section_kind",
                type=SearchFieldDataType.String,
                filterable=True,
            ),
            SearchField(
                name="content_vector",
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True,
                vector_search_dimensions=RagV3Settings.embedding_dimensions(),
                vector_search_profile_name="rag-v3-profile",
            ),
        ]

        return SearchIndex(
            name=RagV3Settings.INDEX_NAME,
            fields=fields,
            vector_search=VectorSearch(
                algorithms=[HnswAlgorithmConfiguration(name="rag-v3-hnsw")],
                profiles=[
                    VectorSearchProfile(
                        name="rag-v3-profile",
                        algorithm_configuration_name="rag-v3-hnsw",
                    )
                ],
            ),
            semantic_search=SemanticSearch(
                default_configuration_name="rag-v3-semantic",
                configurations=[
                    SemanticConfiguration(
                        name="rag-v3-semantic",
                        prioritized_fields=SemanticPrioritizedFields(
                            title_field=SemanticField(field_name="document_title"),
                            content_fields=[SemanticField(field_name="content")],
                        ),
                    )
                ],
            ),
        )

    def _build_image_index(self) -> SearchIndex:
        fields = [
            SearchableField(
                name="image_chunk_id",
                key=True,
                filterable=True,
                sortable=True,
                analyzer_name="keyword",
            ),
            SimpleField(
                name="parent_id",
                type=SearchFieldDataType.String,
                filterable=True,
                sortable=True,
            ),
            SimpleField(
                name="document_title",
                type=SearchFieldDataType.String,
                filterable=True,
                sortable=True,
            ),
            SimpleField(
                name="metadata_storage_path",
                type=SearchFieldDataType.String,
                filterable=True,
                sortable=True,
            ),
            SimpleField(
                name="page_number",
                type=SearchFieldDataType.Int32,
                filterable=True,
                sortable=True,
            ),
            SearchableField(name="content", type=SearchFieldDataType.String),
            SearchableField(name="layout_text", type=SearchFieldDataType.String),
            SearchableField(name="image_caption", type=SearchFieldDataType.String),
            SimpleField(
                name="image_path",
                type=SearchFieldDataType.String,
                filterable=True,
            ),
            SimpleField(
                name="source_kind",
                type=SearchFieldDataType.String,
                filterable=True,
            ),
            SimpleField(
                name="section_kind",
                type=SearchFieldDataType.String,
                filterable=True,
            ),
            SearchField(
                name="image_vector",
                type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                searchable=True,
                vector_search_dimensions=RagV3Settings.embedding_dimensions(),
                vector_search_profile_name="rag-v3-image-profile",
            ),
        ]

        return SearchIndex(
            name=RagV3Settings.IMAGE_INDEX_NAME,
            fields=fields,
            vector_search=VectorSearch(
                algorithms=[HnswAlgorithmConfiguration(name="rag-v3-image-hnsw")],
                profiles=[
                    VectorSearchProfile(
                        name="rag-v3-image-profile",
                        algorithm_configuration_name="rag-v3-image-hnsw",
                    )
                ],
            ),
            semantic_search=SemanticSearch(
                default_configuration_name="rag-v3-image-semantic",
                configurations=[
                    SemanticConfiguration(
                        name="rag-v3-image-semantic",
                        prioritized_fields=SemanticPrioritizedFields(
                            title_field=SemanticField(field_name="document_title"),
                            content_fields=[SemanticField(field_name="image_caption")],
                        ),
                    )
                ],
            ),
        )

    def _build_skillset(self) -> SearchIndexerSkillset:
        layout_outputs = [
            OutputFieldMappingEntry(name="text_sections", target_name="text_sections"),
        ]
        extraction_options = [DocumentIntelligenceLayoutSkillExtractionOptions.LOCATION_METADATA]
        if LayoutRagSettings.ENABLE_IMAGE_REFERENCES:
            extraction_options.append(DocumentIntelligenceLayoutSkillExtractionOptions.IMAGES)
            layout_outputs.append(
                OutputFieldMappingEntry(name="normalized_images", target_name="normalized_images")
            )

        skills = [
            DocumentIntelligenceLayoutSkill(
                name="rag-v3-layout-skill",
                description="Layout extraction for rag-v3 with multimodal-ready outputs",
                context="/document",
                output_format=DocumentIntelligenceLayoutSkillOutputFormat.TEXT,
                output_mode=DocumentIntelligenceLayoutSkillOutputMode.ONE_TO_MANY,
                markdown_header_depth=None,
                extraction_options=extraction_options,
                chunking_properties=DocumentIntelligenceLayoutSkillChunkingProperties(
                    unit=DocumentIntelligenceLayoutSkillChunkingUnit.CHARACTERS,
                    maximum_length=LayoutRagSettings.MAX_CHUNK_LENGTH,
                    overlap_length=LayoutRagSettings.OVERLAP_LENGTH,
                ),
                inputs=[InputFieldMappingEntry(name="file_data", source="/document/file_data")],
                outputs=layout_outputs,
            ),
            AzureOpenAIEmbeddingSkill(
                name="rag-v3-embedding-skill",
                description="Embeddings for each rag-v3 layout chunk",
                context="/document/text_sections/*",
                resource_url=OpenAISettings.ENDPOINT,
                deployment_name=OpenAISettings.EMBEDDING_DEPLOYMENT,
                api_key=OpenAISettings.API_KEY,
                model_name=OpenAISettings.EMBEDDING_MODEL,
                dimensions=RagV3Settings.embedding_dimensions(),
                inputs=[
                    InputFieldMappingEntry(
                        name="text",
                        source="/document/text_sections/*/content",
                    )
                ],
                outputs=[
                    OutputFieldMappingEntry(
                        name="embedding",
                        target_name="content_vector",
                    )
                ],
            ),
        ]

        if LayoutRagSettings.ENABLE_IMAGE_REFERENCES:
            skills.insert(
                1,
                ChatCompletionSkill(
                    name="rag-v3-image-caption-skill",
                    description="Generates concise captions for extracted document images",
                    context="/document/normalized_images/*",
                    uri=AzureOpenAISettings.chat_completions_uri(AzureOpenAISettings.get_deployment_name()), # REVIEW: Is this the right deployment?
                    api_key=AzureOpenAISettings.get_api_key(),
                    common_model_parameters=CommonModelParameters(
                        temperature=0.2,
                        max_tokens=180,
                    ),
                    inputs=[
                        InputFieldMappingEntry(
                            name="systemMessage",
                            source=(
                                "='Describe this document image in a calm, concise way. Focus on "
                                "charts, formulas, tables, labels, and the main takeaway. Return "
                                "plain text only.'"
                            ),
                        ),
                        InputFieldMappingEntry(
                            name="userMessage",
                            source=(
                                "='Create an accessible caption for this extracted document image. "
                                "Mention if it appears to be a chart, table, formula, or diagram.'"
                            ),
                        ),
                        InputFieldMappingEntry(
                            name="image",
                            source="/document/normalized_images/*/data",
                        ),
                    ],
                    outputs=[
                        OutputFieldMappingEntry(
                            name="response",
                            target_name="image_caption",
                        )
                    ],
                ),
            )
            skills.append(
                AzureOpenAIEmbeddingSkill(
                    name="rag-v3-image-embedding-skill",
                    description="Embeddings for each rag-v3 image caption",
                    context="/document/normalized_images/*",
                    resource_url=OpenAISettings.ENDPOINT,
                    deployment_name=OpenAISettings.EMBEDDING_DEPLOYMENT,
                    api_key=OpenAISettings.API_KEY,
                    model_name=OpenAISettings.EMBEDDING_MODEL,
                    dimensions=RagV3Settings.embedding_dimensions(),
                    inputs=[
                        InputFieldMappingEntry(
                            name="text",
                            source="/document/normalized_images/*/image_caption",
                        )
                    ],
                    outputs=[
                        OutputFieldMappingEntry(
                            name="embedding",
                            target_name="image_vector",
                        )
                    ],
                )
            )

        knowledge_store = None
        if LayoutRagSettings.ENABLE_IMAGE_REFERENCES:
            knowledge_store = SearchIndexerKnowledgeStore(
                storage_connection_string=BlobStorageSettings.CONNECTION_STRING or "",
                projections=[
                    SearchIndexerKnowledgeStoreProjection(
                        files=[
                            SearchIndexerKnowledgeStoreFileProjectionSelector(
                                storage_container=BlobStorageSettings.AZURE_STORAGE_CONTAINER,
                                source="/document/normalized_images/*",
                            )
                        ]
                    )
                ],
            )

        return SearchIndexerSkillset(
            name=RagV3Settings.SKILLSET_NAME,
            description="rag-v3 multimodal-ready pipeline built on top of rag-v2",
            skills=skills,
            knowledge_store=knowledge_store,
            index_projection=SearchIndexerIndexProjection(
                selectors=[
                    SearchIndexerIndexProjectionSelector(
                        target_index_name=RagV3Settings.INDEX_NAME,
                        parent_key_field_name="parent_id",
                        source_context="/document/text_sections/*",
                        mappings=[
                            InputFieldMappingEntry(
                                name="document_title",
                                source="/document/metadata_storage_name",
                            ),
                            InputFieldMappingEntry(
                                name="metadata_storage_path",
                                source="/document/metadata_storage_path",
                            ),
                            InputFieldMappingEntry(
                                name="content",
                                source="/document/text_sections/*/content",
                            ),
                            InputFieldMappingEntry(
                                name="layout_text",
                                source="/document/text_sections/*/content",
                            ),
                            InputFieldMappingEntry(
                                name="content_vector",
                                source="/document/text_sections/*/content_vector",
                            ),
                        ],
                    ),
                    SearchIndexerIndexProjectionSelector(
                        target_index_name=RagV3Settings.IMAGE_INDEX_NAME,
                        parent_key_field_name="parent_id",
                        source_context="/document/normalized_images/*",
                        mappings=[
                            InputFieldMappingEntry(
                                name="document_title",
                                source="/document/metadata_storage_name",
                            ),
                            InputFieldMappingEntry(
                                name="metadata_storage_path",
                                source="/document/metadata_storage_path",
                            ),
                            InputFieldMappingEntry(
                                name="content",
                                source="/document/normalized_images/*/image_caption",
                            ),
                            InputFieldMappingEntry(
                                name="image_vector",
                                source="/document/normalized_images/*/image_vector",
                            ),
                            InputFieldMappingEntry(
                                name="layout_text",
                                source="/document/normalized_images/*/image_caption",
                            ),
                            InputFieldMappingEntry(
                                name="image_caption",
                                source="/document/normalized_images/*/image_caption",
                            ),
                            InputFieldMappingEntry(
                                name="image_path",
                                source="/document/normalized_images/*/imagePath",
                            ),
                        ],
                    ),
                ],
                parameters=SearchIndexerIndexProjectionsParameters(
                    projection_mode=IndexProjectionMode.SKIP_INDEXING_PARENT_DOCUMENTS
                ),
            ),
        )

    def _build_indexer(self) -> SearchIndexer:
        return SearchIndexer(
            name=RagV3Settings.INDEXER_NAME,
            data_source_name=RagV3Settings.DATASOURCE_NAME,
            target_index_name=RagV3Settings.INDEX_NAME,
            skillset_name=RagV3Settings.SKILLSET_NAME,
            parameters=IndexingParameters(
                max_failed_items=25,
                max_failed_items_per_batch=10,
                configuration={"allowSkillsetToReadFileData": True},
            ),
            field_mappings=[
                FieldMapping(
                    source_field_name="metadata_storage_name",
                    target_field_name="document_title",
                )
            ],
        )

    def provision(self) -> None:
        index_client = self._service.get_client()
        indexer_client = self._service.get_indexer_client()

        indexer_client.create_or_update_data_source_connection(self._build_datasource())
        index_client.create_or_update_index(self._build_index())
        if LayoutRagSettings.ENABLE_IMAGE_REFERENCES:
            index_client.create_or_update_index(self._build_image_index())
        indexer_client.create_or_update_skillset(self._build_skillset())
        indexer_client.create_or_update_indexer(self._build_indexer())

    def run_indexer(self) -> None:
        self._service.get_indexer_client().run_indexer(RagV3Settings.INDEXER_NAME)
