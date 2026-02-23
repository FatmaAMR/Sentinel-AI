# Vector Storage (ChromaDB)
**Role:** This folder contains the persistent index of our Knowledge Base (ISO/SKF PDFs).
**Architecture:** - It stores "Embeddings" (numerical representations of text).
- **Team Note:** Do not manually edit files in this folder. It is managed by `app/services/rag_service.py`.
- If you add new PDFs to `data/`, you must re-run the indexing script to update this store.