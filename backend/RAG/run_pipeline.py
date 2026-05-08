from typing import List
from RAG.document_processor import DocumentProcessor
from RAG.db_builder import RetrieverBuilder
from RAG.workflow import AgentWorkflow


# Initialize once
processor = DocumentProcessor()

retriever_builder = RetrieverBuilder()

workflow = AgentWorkflow()


def run_pipeline(file_paths: List[str], query: str):
    """
    Execute the document QA pipeline.
    """

    if not query.strip():
        raise ValueError("Question cannot be empty")

    if not file_paths:
        raise ValueError("No documents provided")

    # Process documents
    chunks = processor.process(file_paths)

    # Build retriever
    retriever = retriever_builder.build_hybrid_retriever(
        chunks
    )

    # Run workflow
    result = workflow.full_pipeline(
        question=query,
        retriever=retriever
    )

    return {
        "answer": result["draft_answer"],
        "verification": result["verification_report"]
    }