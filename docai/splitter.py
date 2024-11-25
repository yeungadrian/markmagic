import re

from docai.document import Document, MetaData


def _char_len(text: str) -> int:
    return len(text.split(" "))


def _split_chunk(separator: str, doc: Document) -> list[Document]:
    _splits = re.split(f"({re.escape(separator)})", doc.content)
    splits = [_splits[i] + _splits[i + 1] for i in range(0, len(_splits) - 1, 2)]
    if len(_splits) % 2 == 0:
        splits += _splits[-1:]
    splits = splits + [_splits[-1]]

    split_docs = []
    for i in splits:
        _doc = Document(content=i, metadata=MetaData(filename="asd", tokens=_char_len(i)))
        split_docs.append(_doc)

    return split_docs


def _chunk_docs(docs: list[Document], separator: str, overlap: int) -> list[Document]:
    split_docs = []

    for doc in docs:
        if doc.metadata.table:
            split_docs.append(doc)
        else:
            if doc.metadata.tokens > overlap:
                if separator in doc.content:
                    # TODO: Update token counts for new chunk
                    new_chunks = _split_chunk(separator, doc)
                    print(new_chunks)
                    split_docs = split_docs + new_chunks
                else:
                    split_docs.append(doc)
            else:
                split_docs.append(doc)

    # Check do we need to split more.

    return split_docs


def _split_docs(docs: list[Document], separators: tuple[str], overlap: int) -> list[Document]:
    for doc in docs:
        doc.metadata.tokens = _char_len(doc.content)

    for separator in separators:
        if all([doc.metadata.tokens <= overlap]):
            break
        print(f"separator: {separator}")
        docs = _chunk_docs(docs, separator, overlap)
    return docs


def _merge_docs(chunk_size: int, overlap: int, docs: list[Document]) -> list[list[Document]]:
    merged_docs = []
    current_doc = []
    tokens = 0
    overlap_tokens = 0
    for doc in docs:
        if tokens + doc.metadata.tokens < chunk_size:
            current_doc.append(doc)
            tokens += doc.metadata.tokens
        elif overlap_tokens + doc.metadata.tokens < overlap:
            current_doc.append(doc)
            overlap_tokens += doc.metadata.tokens
        else:
            merged_docs.append(current_doc)
            # Start a new chunk
            tokens = 0
            overlap_tokens = 0
            current_doc = []
            current_doc.append(doc)
            tokens += doc.metadata.tokens
    merged_docs.append(current_doc)
    return merged_docs
