# Adobe India Hackathon - PDF Processing & Semantic Search Application

## Overview

This application is designed for the Adobe India Hackathon Round 1B challenge. It processes PDF documents and implements semantic search functionality to extract relevant sections based on persona and job requirements.

## Features

- **PDF Text Extraction**: Extracts text content from PDF files page by page
- **Vector Database**: Builds a FAISS-based vector database for efficient semantic search
- **Semantic Search**: Uses sentence transformers to find relevant sections based on queries
- **Content Filtering**: Automatically filters out meat-related content
- **Ranking System**: Ranks extracted sections by relevance and importance
- **JSON Output**: Generates structured JSON output with metadata and analysis

## Architecture

### Core Components

1. **PDFProcessor Class**: Main class handling all PDF processing operations
2. **Sentence Transformer**: Uses 'all-MiniLM-L6-v2' model for embeddings
3. **FAISS Index**: High-performance vector similarity search
4. **Text Chunking**: Processes documents into searchable chunks

### Key Methods

- `extract_text_from_pdf()`: Extracts text from PDF files
- `process_documents()`: Processes all PDFs in input directory
- `_build_vector_db()`: Creates FAISS vector database
- `rank_sections()`: Performs semantic search and ranking
- `find_similar_sections()`: Finds similar content sections

## Installation

### Option 1: Docker (Recommended)

#### Prerequisites
- Docker installed on your system
- Docker Compose (usually comes with Docker Desktop)

#### Quick Start with Docker

```bash
# Clone or download the project
# Create required directories
mkdir -p PDFs output

# Add your PDF files to PDFs/ directory
# Configure challenge1b_input.json

# Build and run with Docker Compose
docker-compose up --build
```

For detailed Docker deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

### Option 2: Local Installation

#### Prerequisites

- Python 3.7+
- pip package manager

#### Dependencies

Install the required packages:

```bash
pip install PyPDF2 sentence-transformers numpy faiss-cpu scikit-learn
```

### Required Files Structure

```
project/
├── app.py
├── PDFs/                    # Directory containing PDF files
├── challenge1b_input.json   # Input configuration file
└── challenge1b_output.json  # Output file (generated)
```

## Usage

### Adobe Hackathon Execution (Required Format)

The application is designed to work with Adobe's specific Docker execution format:

#### Build Command:
```bash
docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .
```

#### Run Command:
```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none mysolutionname:somerandomidentifier
```

#### Expected Behavior:
- **Input**: PDF files placed in `/app/input` directory
- **Output**: JSON files generated in `/app/output` directory
- **Format**: For each `filename.pdf`, generates `filename.json`

### Quick Test

1. **Create Test Directories**
   ```bash
   mkdir -p input output
   ```

2. **Add PDF Files**
   ```bash
   # Copy your PDF files to input directory
   cp your_documents/*.pdf input/
   ```

3. **Build and Run**
   ```bash
   # Build the image
   docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .
   
   # Run the container
   docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none mysolutionname:somerandomidentifier
   ```

4. **Check Results**
   ```bash
   # Check generated JSON files
   ls -la output/
   ```

### Windows Testing

Use the provided batch file:
```cmd
test_docker.bat
```

### Linux/Mac Testing

Use the provided shell script:
```bash
chmod +x test_docker.sh
./test_docker.sh
```

### Local Installation

1. **Prepare Input Files**

Create the input JSON file (`challenge1b_input.json`):

```json
{
  "persona": {
    "role": "Your persona description"
  },
  "job_to_be_done": {
    "task": "Your task description"
  }
}
```

2. **Add PDF Documents**

Place your PDF files in the `PDFs/` directory.

3. **Run the Application**

```bash
python app.py
```

### 4. Check Output

The application will generate `challenge1b_output.json` with:

- **Metadata**: Processing information and vector database stats
- **Extracted Sections**: Top 5 relevant sections with rankings
- **Subsection Analysis**: Detailed analysis of each section

## Output Format

The application generates a structured JSON output with:

```json
{
  "metadata": {
    "input_documents": ["document1.pdf", "document2.pdf"],
    "persona": "Persona role",
    "job_to_be_done": "Task description",
    "processing_timestamp": "2024-01-01T12:00:00",
    "vector_db_stats": {
      "num_vectors": 150,
      "embedding_dim": 384
    }
  },
  "extracted_sections": [
    {
      "document": "document1.pdf",
      "section_title": "Section Title",
      "importance_rank": 1,
      "page_number": 5,
      "similarity_score": 0.85
    }
  ],
  "subsection_analysis": [
    {
      "document": "document1.pdf",
      "refined_text": "Extracted text content",
      "page_number": 5,
      "similarity_score": 0.85
    }
  ]
}
```

## Technical Details

### Vector Database

- **Model**: all-MiniLM-L6-v2 (80MB, CPU-optimized)
- **Index Type**: FAISS IndexFlatL2
- **Embedding Dimension**: 384
- **Similarity Metric**: Cosine similarity

### Performance Features

- **Efficient Processing**: Processes multiple PDFs in batch
- **Memory Optimized**: Uses CPU-based sentence transformers
- **Fast Search**: FAISS provides sub-second search times
- **Content Filtering**: Automatically excludes meat-related content

### Error Handling

- Graceful PDF processing errors
- Vector database validation
- Input file validation
- Comprehensive exception handling

## Configuration

### Model Configuration

```python
# Embedding model (80MB, CPU-optimized)
self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
```

### Search Parameters

- **Top K Results**: 5 (configurable)
- **Search Expansion**: 3x for filtering
- **Similarity Threshold**: Automatic based on ranking

## File Structure

```
WIN ADOBE/
├── app.py                                    # Main application file
├── README.md                                 # This documentation
├── DEPLOYMENT.md                             # Docker deployment guide
├── Dockerfile                                # Docker configuration
├── docker-compose.yml                        # Docker Compose setup
├── requirements.txt                          # Python dependencies
├── .dockerignore                             # Docker ignore rules
├── PDFs/                                     # Input PDF directory
├── output/                                   # Output directory
├── challenge1b_input.json                   # Input configuration
├── challenge1b_output.json                  # Generated output
└── 6874faecd848a_Adobe_India_Hackathon_-_Challenge_Doc (1).pdf
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| PyPDF2 | Latest | PDF text extraction |
| sentence-transformers | Latest | Text embeddings |
| numpy | Latest | Numerical operations |
| faiss-cpu | Latest | Vector similarity search |
| scikit-learn | Latest | Cosine similarity |

## Performance Considerations

- **Memory Usage**: ~80MB for embedding model
- **Processing Speed**: ~1-2 seconds per PDF page
- **Search Speed**: Sub-second for typical queries
- **Scalability**: Handles multiple PDFs efficiently

## Troubleshooting

### Common Issues

1. **PDF Reading Errors**: Ensure PDFs are not password-protected
2. **Memory Issues**: Use CPU-only model for large documents
3. **Import Errors**: Install all required dependencies
4. **File Not Found**: Check input directory structure

### Debug Mode

Add debug prints to track processing:

```python
# Add to main() function
print(f"Processing {len(documents)} documents")
print(f"Vector DB size: {len(processor.chunk_references)}")
```

## License

This project is developed for the Adobe India Hackathon Round 1B challenge.

## Contributing

This is a hackathon submission. For questions or issues, refer to the challenge documentation.

---

**Note**: This application is specifically designed for the Adobe India Hackathon challenge requirements and includes features like meat content filtering as per the challenge specifications. #   A d o b e - H a c k a t h o n - R o u n d 1 B  
 