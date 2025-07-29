# Approach Explanation

## Overview

This solution is designed for the Adobe India Hackathon Round 1B and implements an intelligent, fully containerized PDF document processing system. The system extracts, semantically analyzes, and ranks relevant sections from PDF documents based on user-defined personas and job requirements, all while meeting strict offline and Docker execution requirements.

## Architecture & Workflow

The core of the solution is a Python application (`app.py`) that leverages the `sentence-transformers` library for semantic search, `PyPDF2` for PDF text extraction, and `faiss-cpu` for efficient vector similarity search. The application is structured to be robust, modular, and easily extensible.

### Input/Output Handling
- **Input:** The application expects all PDF files to be placed in the `/app/input` directory inside the Docker container. Additionally, a `config.json` file can be provided in the same directory to specify the persona and job/task for semantic ranking. If `config.json` is absent, sensible defaults are used.
- **Output:** For each input PDF, the system generates a corresponding JSON file in `/app/output`, containing the most relevant sections and a detailed analysis, following the required output schema.

### Semantic Processing
- **Text Extraction:** Each PDF is processed page by page, extracting text content using `PyPDF2`.
- **Embedding & Ranking:** Extracted text chunks are embedded using the `all-MiniLM-L6-v2` model from `sentence-transformers`. These embeddings are indexed with FAISS for fast similarity search. A query is generated based on the persona and job/task, and the most relevant sections are ranked using cosine similarity.
- **Output Generation:** The top-ranked sections and their metadata are compiled into a structured JSON output for each PDF.

## Offline Model Handling
To ensure the solution works fully offline (as required by the hackathon), the `all-MiniLM-L6-v2` model is pre-downloaded and included in the Docker image at build time. The application loads the model from a local path (`/app/model/all-MiniLM-L6-v2`), guaranteeing no network calls are made at runtime.

## Dockerization & Portability
The solution is packaged in a Docker container based on the official Python 3.9-slim image, explicitly targeting the AMD64 architecture. All dependencies are installed via `req.txt`, and the pre-downloaded model is copied into the image. The container is configured to run in a fully isolated, offline environment, processing all PDFs from `/app/input` and writing results to `/app/output`.

## Compliance with Requirements
- **Offline Execution:** No internet access is required at runtime; all models and dependencies are bundled in the image.
- **AMD64 Compatibility:** The Dockerfile explicitly sets the platform to `linux/amd64`.
- **Input/Output Contract:** The container processes all PDFs in `/app/input` and writes a JSON for each to `/app/output`.
- **Resource Efficiency:** The selected model is lightweight (<200MB) and CPU-optimized, ensuring fast and memory-efficient processing.

## Conclusion
This approach ensures robust, reproducible, and portable PDF semantic analysis, fully aligned with the hackathon’s technical and operational constraints. The modular design allows for easy extension to new personas, tasks, or document types, and the strict offline/Docker compliance guarantees seamless deployment in controlled environments. 