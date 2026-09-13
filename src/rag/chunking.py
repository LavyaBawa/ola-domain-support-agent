def fixed_size_chunks(text, chunk_size=500, overlap=100):
    """
    Split text into fixed-size chunks with overlapping characters.
    """
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def sentence_chunks(text):
    """
    Split text into sentence-based chunks.
    """
    sentences = [sentence.strip() for sentence in text.split(".") if sentence.strip()]

    return sentences
