Vespa Search Assignment
This project implements a Vespa-based search system with keyword, semantic, and recommendation search capabilities.

Steps
Dataset Preparation: Processed and formatted the data to include doc_id, title, and text, and saved as JSONL for Vespa ingestion.

Schema Configuration: Defined doc.sd schema with fields, BM25 ranking, and tensor embeddings for semantic and recommendation search.

Vespa Deployment Setup: Configured services.xml for document processing and embedding integration; deployed to Vespa Docker container.

Search Implementation:

Keyword Search: Uses BM25 for keyword relevance.
Semantic Search: Embedding-based search for similarity.
Recommendation Search: Finds similar items based on document embeddings.
Testing: Verified output across all search types for relevance and accuracy.
