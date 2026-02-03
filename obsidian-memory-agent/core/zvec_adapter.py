import os
import json
import random
import math
from datetime import datetime
from pathlib import Path

# Try to import zvec, otherwise use mock
try:
    import zvec
    ZVEC_AVAILABLE = True
except ImportError:
    ZVEC_AVAILABLE = False

class EmbeddingService:
    """Service to generate embeddings from text."""
    
    def __init__(self, dimension=128):
        self.dimension = dimension
    
    def embed(self, text):
        """
        Generate embedding for text.
        In a real scenario, this would call OpenAI or a local model.
        Here we generate a deterministic "fake" embedding based on hash for demo purposes.
        """
        # Simple deterministic hash-based embedding for demo
        seed = sum(ord(c) for c in text)
        random.seed(seed)
        vector = [random.uniform(-1.0, 1.0) for _ in range(self.dimension)]
        
        # Normalize
        norm = math.sqrt(sum(x*x for x in vector))
        if norm > 0:
            vector = [x/norm for x in vector]
            
        return vector

class ZvecAdapter:
    """Adapter for Zvec vector database."""
    
    def __init__(self, db_path, collection_name="memory_core"):
        self.db_path = db_path
        self.collection_name = collection_name
        self.dimension = 128  # Demo dimension
        self.embedding_service = EmbeddingService(self.dimension)
        self.collection = None
        
        self._initialize_db()
        
    def _initialize_db(self):
        """Initialize Zvec collection or mock structure."""
        if ZVEC_AVAILABLE:
            try:
                # Define schema
                schema = zvec.CollectionSchema(
                    name=self.collection_name,
                    vectors=zvec.VectorSchema("embedding", zvec.DataType.VECTOR_FP32, self.dimension),
                )
                # Create or open
                self.collection = zvec.create_and_open(path=self.db_path, schema=schema)
                print(f"[ZvecAdapter] Zvec database initialized at {self.db_path}")
            except Exception as e:
                print(f"[ZvecAdapter] Error initializing Zvec: {e}. Falling back to Mock.")
                self.collection = MockCollection(self.db_path)
        else:
            print("[ZvecAdapter] Zvec library not found. Using Mock implementation.")
            self.collection = MockCollection(self.db_path)
            
    def add_memory(self, doc_id, text, metadata=None):
        """Add a memory item to the database."""
        vector = self.embedding_service.embed(text)
        
        if metadata is None:
            metadata = {}
            
        # Ensure metadata contains the text content for retrieval
        metadata['content'] = text
        metadata['timestamp'] = datetime.now().isoformat()
        
        if ZVEC_AVAILABLE and not isinstance(self.collection, MockCollection):
            try:
                # Zvec insert
                self.collection.insert([
                    zvec.Doc(id=doc_id, vectors={"embedding": vector}, fields=metadata)
                ])
                return True
            except Exception as e:
                print(f"[ZvecAdapter] Insert failed: {e}")
                return False
        else:
            # Mock insert
            self.collection.insert(doc_id, vector, metadata)
            return True
            
    def search(self, query_text, top_k=5):
        """Search for relevant memories."""
        query_vector = self.embedding_service.embed(query_text)
        
        results = []
        if ZVEC_AVAILABLE and not isinstance(self.collection, MockCollection):
            try:
                # Zvec query
                matches = self.collection.query(
                    zvec.VectorQuery("embedding", vector=query_vector),
                    topk=top_k
                )
                # Parse results
                # Assuming matches is a list of objects with id, score, fields
                for match in matches:
                    # Depending on Zvec API version, access might vary
                    # Here assuming dict-like or object access
                    res = {
                        'id': match.id,
                        'score': match.score,
                        'content': match.fields.get('content', ''),
                        'metadata': match.fields
                    }
                    results.append(res)
            except Exception as e:
                print(f"[ZvecAdapter] Query failed: {e}")
                return []
        else:
            # Mock query
            results = self.collection.query(query_vector, top_k)
            
        return results

class MockCollection:
    """Mock implementation of a vector collection using simple list."""
    
    def __init__(self, path):
        self.path = Path(path)
        self.data_file = self.path / "mock_data.json"
        self.items = []
        self._load()
        
    def _load(self):
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.items = json.load(f)
            except:
                self.items = []
                
    def _save(self):
        if not self.path.exists():
            self.path.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=2)
            
    def insert(self, doc_id, vector, metadata):
        # Remove existing if any
        self.items = [item for item in self.items if item['id'] != doc_id]
        
        self.items.append({
            'id': doc_id,
            'vector': vector,
            'metadata': metadata
        })
        self._save()
        
    def query(self, query_vector, top_k):
        # Calculate cosine similarity
        scored_items = []
        for item in self.items:
            vec = item['vector']
            score = self._cosine_similarity(query_vector, vec)
            scored_items.append({
                'id': item['id'],
                'score': score,
                'content': item['metadata'].get('content', ''),
                'metadata': item['metadata']
            })
            
        # Sort by score desc
        scored_items.sort(key=lambda x: x['score'], reverse=True)
        return scored_items[:top_k]
        
    def _cosine_similarity(self, v1, v2):
        dot_product = sum(a*b for a, b in zip(v1, v2))
        norm_a = math.sqrt(sum(a*a for a in v1))
        norm_b = math.sqrt(sum(b*b for b in v2))
        if norm_a == 0 or norm_b == 0:
            return 0
        return dot_product / (norm_a * norm_b)
