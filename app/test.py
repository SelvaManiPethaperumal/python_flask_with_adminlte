from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Initialize model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to embed a single text
def embed_text(text):
    return model.encode([text])

# Example text
text = 'i love indian'

# Embed the text
text_embedding = embed_text(text)

# Dummy data: Example precomputed embeddings (for demonstration purposes)
# In a real scenario, you would load these from your precomputed FAISS index.
precomputed_texts = ['I love India', 'I enjoy Indian food', 'I dislike Indian music', 'I adore Indian culture']
precomputed_embeddings = embed_text(precomputed_texts)

# Initialize FAISS index with precomputed embeddings
dimension = precomputed_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(precomputed_embeddings))

# Search for similar texts in the FAISS index
k = 2  # Number of nearest neighbors
D, I = index.search(np.array(text_embedding), k)

# Print the similarity results
print("Input Text:")
print(text)
print("\nSimilar Texts:")
for idx, dist in zip(I[0], D[0]):
    print(f"Text: {precomputed_texts[idx]}, Distance: {dist}")
