import re

class ChunkingAgent:
    """
    Splits text into sentence-aware overlapping chunks
    (safe overlap, no word corruption)
    (prevents word-breaking issues like 'ntum', 'rithm')
    """

    def __init__(self, chunk_size=500, overlap=2):
        self.chunk_size = chunk_size
        self.overlap = overlap  # number of sentences, NOT characters

    def chunk(self, text):

        # split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)

        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence_len = len(sentence)

            if current_length + sentence_len <= self.chunk_size:
                current_chunk.append(sentence)
                current_length += sentence_len
            else:
                chunks.append(" ".join(current_chunk))

                # sentence-based overlap (safe)
                current_chunk = current_chunk[-self.overlap:]
                current_chunk.append(sentence)

                current_length = sum(len(s) for s in current_chunk)

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks