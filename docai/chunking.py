import re
from collections.abc import Callable

from pydantic import BaseModel, computed_field

from docai.models import Chunk, Document, DocumentMetaData, MetaData, PartitionedDocument


def _get_n_tokens(text: str) -> int:
    text = text.strip()
    if text:
        return 1 + text.count(" ")
    else:
        return 0


class Chunker(BaseModel):
    """Chunker class for splitting and merging documents based on token count and specified separators."""

    chunk_size: int
    chunk_overlap: int = 0
    separators: tuple[str, ...] = ("\n\n", "\n", ".", " ", "")
    get_n_tokens: Callable[[str], int] = _get_n_tokens

    @computed_field  # type: ignore[prop-decorator]
    def split_size(self) -> int:
        """Maximum tokens for each split."""
        return self.chunk_overlap if self.chunk_overlap > 0 else self.chunk_size

    def _split_document(self, document: PartitionedDocument) -> list[Chunk]:
        """Split chunks partitioned document so each chunk is smaller than split_size."""
        for chunk in document.chunks:
            # Check if chunk needs to be split.
            chunk.n_tokens = self.get_n_tokens(chunk.content)
            chunk.chunked = chunk.n_tokens < self.split_size
        split_chunks = []
        for chunk in document.chunks:
            current_chunks = [chunk]
            # Recursively iterate over separators until chunk has been chunked
            for separator in self.separators:
                if all(i.chunked for i in current_chunks):
                    break
                else:
                    current_chunks = self._split_chunks(current_chunks, separator)
            split_chunks.extend(current_chunks)
        return split_chunks

    def _split_chunks(self, chunks: list[Chunk], separator: str) -> list[Chunk]:
        """Split chunks using separator if chunk is not chunked."""
        split_chunks = []
        for chunk in chunks:
            if chunk.chunked:
                split_chunks.append(chunk)
            else:
                if chunk.table:
                    chunk.chunked = True
                    split_chunks.append(chunk)
                else:
                    split_chunks.extend(self._split_chunk(chunk, separator))
        return split_chunks

    def _split_chunk(
        self,
        chunk: Chunk,
        separator: str,
    ) -> list[Chunk]:
        """Split chunk using separator."""
        _splits = re.split(f"({re.escape(separator)})", chunk.content)
        # Add separator to chunks
        splits = [_splits[i] + _splits[i + 1] for i in range(0, len(_splits) - 1, 2)]
        if len(_splits) % 2 == 0 and _splits[-1:]:
            splits += _splits[-1:]
        splits = splits + [_splits[-1]]
        # Construct chunk object and measure tokens
        split_chunks = []
        for i in splits:
            n_tokens = self.get_n_tokens(i)
            split_chunks.append(Chunk(content=i, n_tokens=n_tokens, chunked=self.split_size >= n_tokens))
        return split_chunks

    def _create_document(
        self,
        chunks: list[Chunk],
        token_count: int,
        overlap_token_count: int,
        overlap_start: int | None,
        metadata: MetaData,
    ) -> Document:
        # TODO: Reconsider how we join texts, Avoid: Sentence 1Sentence 2
        merged_content = " ".join(chunk.content for chunk in chunks)
        n_tokens = token_count + overlap_token_count
        merge = Document(
            content=merged_content,
            metadata=DocumentMetaData(
                filename=metadata.filename,
                sheet_name=metadata.sheet_name,
                estimated_tokens=n_tokens,
                overlap_start=overlap_start,
            ),
        )
        return merge

    def _merge_chunks(self, chunks: list[Chunk], metadata: MetaData) -> list[Document]:
        documents = []
        current_merge = []
        token_count = 0
        overlap_token_count = 0
        overlap_start = None
        for chunk in chunks:
            if token_count + chunk.n_tokens < self.chunk_size:
                current_merge.append(chunk)
                token_count += chunk.n_tokens
            elif overlap_token_count + chunk.n_tokens < self.chunk_overlap:
                if overlap_start is None:
                    # Count the number of characters before we start overlap
                    overlap_start = sum(len(chunk.content) for chunk in current_merge)
                current_merge.append(chunk)
                overlap_token_count += chunk.n_tokens
            else:
                # Merge current_merge into single Chunk before appending
                document = self._create_document(
                    current_merge, token_count, overlap_token_count, overlap_start, metadata
                )
                documents.append(document)
                # Start a new chunk
                current_merge = [chunk]
                token_count = chunk.n_tokens
                overlap_token_count = 0
                overlap_start = None
        # Merge the last current_merge into a single Chunk before appending
        document = self._create_document(
            current_merge, token_count, overlap_token_count, overlap_start, metadata
        )
        documents.append(document)
        return documents

    def create_documents(self, partitioned_documents: list[PartitionedDocument]) -> list[Document]:
        """Create documents."""
        documents = []
        for pd in partitioned_documents:
            splits = self._split_document(pd)
            documents.extend(self._merge_chunks(splits, metadata=pd.metadata))
        return documents
