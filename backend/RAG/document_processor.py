from typing import List
from docling.document_converter import DocumentConverter
from langchain_text_splitters import MarkdownHeaderTextSplitter


class DocumentProcessor:
    def __init__(self):
        self.headers = [("#", "Header 1"), ("##", "Header 2")]

    def process(self, files: List) -> List:
        """Process files with caching for subsequent queries"""
        all_chunks = []
        
        for file in files:
            try:
                chunks = self._process_file(file)
                for chunk in chunks:
                    all_chunks.append(chunk)
            except Exception as e:
                print(f"Failed to process {file.name}: {str(e)}")
                continue
    
        return all_chunks

    def _process_file(self, file) -> List:
        """Original processing logic with Docling"""

        converter = DocumentConverter()
        markdown = converter.convert(file).document.export_to_markdown()
        splitter = MarkdownHeaderTextSplitter(self.headers)
        return splitter.split_text(markdown)

    
