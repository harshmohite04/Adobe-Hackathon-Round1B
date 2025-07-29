import json
import os
from typing import List, Dict, Any
import PyPDF2
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from collections import defaultdict

class PDFProcessor:
    def __init__(self, model_path):
        self.embedding_model = SentenceTransformer(model_path, device='cpu')
        self.vector_db_index = None
        self.chunk_references = []

    def extract_text_from_pdf(self, pdf_path: str) -> Dict[int, str]:
        text_by_page = {}
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num in range(len(reader.pages)):
                    text = reader.pages[page_num].extract_text()
                    if text and text.strip():
                        text_by_page[page_num + 1] = text.strip()
        except Exception as e:
            print(f"Error processing {pdf_path}: {str(e)}")
        return text_by_page

    def _build_vector_db(self, chunks: List[Dict[str, Any]]):
        texts = [chunk['text'] for chunk in chunks]
        embeddings = self.embedding_model.encode(texts)
        embeddings = np.array(embeddings).astype('float32')
        dimension = embeddings.shape[1]
        self.vector_db_index = faiss.IndexFlatL2(dimension)
        self.vector_db_index.add(embeddings)
        self.chunk_references = chunks

    def generate_persona_query(self, persona: str, task: str) -> str:
        persona_queries = {
            "Travel Planner": "best attractions, hotels, and itinerary for group trip",
            "HR Professional": "creating fillable forms, e-signatures, and document workflows",
            "Food Contractor": "vegetarian recipes, buffet planning, and large group meals"
        }
        return f"{persona_queries.get(persona, '')} {task}"

    def rank_sections(self, query: str, k: int = 10) -> List[Dict[str, Any]]:
        if not self.vector_db_index or not self.chunk_references:
            return []
        query_embedding = self.embedding_model.encode(query)
        query_embedding = np.array(query_embedding).astype('float32').reshape(1, -1)
        distances, indices = self.vector_db_index.search(query_embedding, k*2)
        ranked_chunks = []
        seen_content = set()
        for idx, distance in zip(indices[0], distances[0]):
            if idx >= 0:
                chunk = self.chunk_references[idx]
                content_hash = hash(chunk['text'])
                if content_hash not in seen_content:
                    seen_content.add(content_hash)
                    lines = [line.strip() for line in chunk['text'].split('\n') if line.strip()]
                    title = next((line for line in lines if not line.startswith(('•', '-', '·'))), lines[0][:100])
                    ranked_chunks.append({
                        'document': chunk['document'],
                        'page_number': chunk['page_number'],
                        'text': chunk['text'],
                        'title': title,
                        'similarity': float(1 / (1 + distance))
                    })
        return sorted(ranked_chunks, key=lambda x: x['similarity'], reverse=True)[:k]

def process_pdfs(input_dir: str, output_dir: str, model_path: str, config_path: str):
    # Load persona/task config
    if os.path.exists(config_path):
        with open(config_path) as f:
            input_config = json.load(f)
        persona = input_config.get('persona', {}).get('role', 'Software Engineer')
        task = input_config.get('job_to_be_done', {}).get('task', 'Find information about Adobe internship opportunities and requirements')
    else:
        persona = 'Software Engineer'
        task = 'Find information about Adobe internship opportunities and requirements'

    processor = PDFProcessor(model_path)
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            text_by_page = processor.extract_text_from_pdf(pdf_path)
            if not text_by_page:
                continue
            all_chunks = []
            for page_num, text in text_by_page.items():
                all_chunks.append({
                    'document': filename,
                    'page_number': page_num,
                    'text': text
                })
            if all_chunks:
                processor._build_vector_db(all_chunks)
                query = processor.generate_persona_query(persona, task)
                ranked_sections = processor.rank_sections(query)
                output = {
                    "metadata": {
                        "input_documents": [filename],
                        "persona": persona,
                        "job_to_be_done": task
                    },
                    "extracted_sections": [
                        {
                            "document": section['document'],
                            "section_title": section['title'],
                            "importance_rank": i+1,
                            "page_number": section['page_number']
                        }
                        for i, section in enumerate(ranked_sections)
                    ],
                    "subsection_analysis": [
                        {
                            "document": section['document'],
                            "refined_text": section['text'],
                            "page_number": section['page_number']
                        }
                        for section in ranked_sections
                    ]
                }
                output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.json")
                with open(output_path, 'w') as f:
                    json.dump(output, f, indent=2)
                print(f"Processed {filename} -> {output_path}")

if __name__ == "__main__":
    input_dir = "/app/input"
    output_dir = "/app/output"
    model_path = "/app/model/all-MiniLM-L6-v2"
    config_path = os.path.join(input_dir, "config.json")
    process_pdfs(input_dir, output_dir, model_path, config_path)