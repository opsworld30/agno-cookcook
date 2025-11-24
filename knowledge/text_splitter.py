from typing import List


class RecursiveCharacterTextSplitter:
    
    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 80,
        separators: List[str] = None
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", "。", "！", "？", ". ", "! ", "? ", " ", ""]
    
    def split_text(self, text: str) -> List[str]:
        if not text:
            return []
        
        if len(text) <= self.chunk_size:
            return [text]
        
        return self._split_text_recursive(text, self.separators)
    
    def _split_text_recursive(self, text: str, separators: List[str]) -> List[str]:
        final_chunks = []
        
        separator = separators[-1]
        for i, sep in enumerate(separators):
            if sep == "":
                separator = sep
                break
            if sep in text:
                separator = sep
                break
        
        splits = text.split(separator) if separator else list(text)
        
        good_splits = []
        for split in splits:
            if len(split) < self.chunk_size:
                good_splits.append(split)
            else:
                if good_splits:
                    merged_text = self._merge_splits(good_splits, separator)
                    final_chunks.extend(merged_text)
                    good_splits = []
                
                if len(separators) > 1:
                    other_chunks = self._split_text_recursive(split, separators[1:])
                    final_chunks.extend(other_chunks)
                else:
                    final_chunks.append(split)
        
        if good_splits:
            merged_text = self._merge_splits(good_splits, separator)
            final_chunks.extend(merged_text)
        
        return final_chunks
    
    def _merge_splits(self, splits: List[str], separator: str) -> List[str]:
        chunks = []
        current_chunk = []
        current_length = 0
        
        for split in splits:
            split_len = len(split)
            
            if current_length + split_len + len(separator) > self.chunk_size:
                if current_chunk:
                    chunk_text = separator.join(current_chunk)
                    if chunk_text:
                        chunks.append(chunk_text)
                    
                    overlap_start = max(0, len(current_chunk) - 1)
                    current_chunk = current_chunk[overlap_start:]
                    current_length = sum(len(s) for s in current_chunk) + len(separator) * (len(current_chunk) - 1)
            
            current_chunk.append(split)
            current_length += split_len + (len(separator) if current_chunk else 0)
        
        if current_chunk:
            chunk_text = separator.join(current_chunk)
            if chunk_text:
                chunks.append(chunk_text)
        
        return chunks
