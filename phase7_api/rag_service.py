"""
RAG (Retrieval Augmented Generation) Service for the Aloysius Chatbot.
Orchestrates the retrieval and generation pipeline with quality checks.
"""

import logging
from typing import Tuple, List
from phase6_rag.embed_query import embed_query
from phase6_rag.retrieve_context import retrieve_context
from phase6_rag.gemini_llm import get_llm
from config.config import config

logger = logging.getLogger(__name__)

# System prompt for the RAG pipeline
SYSTEM_PROMPT = """
You are an official AI Assistant for St. Aloysius University.

Answer the user's question ONLY using the provided context.
Do not use external knowledge or assumptions.

IMPORTANT:
- If the answer is not present in the context, clearly say:
  "I do not have this information from the official website."
- Be accurate, professional, and helpful.

FORMATTING GUIDELINES:
- Respond naturally, like a knowledgeable human assistant.
- Use short paragraphs for explanations.
- Use bullet points only when listing multiple items.
- Add headings only if they improve clarity.
- Do not force structure or templates.
- Do not write everything as a single paragraph.

The response should look clean and readable, similar to ChatGPT.
"""





def run_rag(question: str) -> Tuple[str, List[str], float]:
    """
    Execute the RAG pipeline with quality assurance.
    
    Args:
        question: User's question/query
        
    Returns:
        Tuple of (answer, sources, confidence_score)
    """
    try:
        logger.info(f"RAG pipeline started for question: {question}")
        
        # Step 1: Embed the query
        logger.debug("Embedding query...")
        query_embedding = embed_query(question)
        
        # Step 2: Retrieve relevant context
        logger.debug("Retrieving context...")
        context_chunks, metadatas = retrieve_context(
            query_embedding, 
            top_k=config.rag.top_k_results
        )
        
        # Verify we have context
        if not context_chunks or len(context_chunks) == 0:
            logger.warning(f"No relevant context found for question: {question}")
            return (
                "I don't have relevant information in the knowledge base to answer this question. "
                "Please contact the university directly or visit staloysius.edu.in",
                [],
                0.0
            )
        
        # Step 3: Generate answer using Gemini
        logger.debug("Generating response with Gemini...")
        llm = get_llm()
        
        answer = llm.generate_with_context(
            query=question,
            context=context_chunks,
            system_instruction=SYSTEM_PROMPT,
            temperature=0.7,
        )
        
        # Step 4: Extract unique sources
        sources = list(set(
            meta.get("url", "unknown")
            for meta in metadatas
            if meta.get("url")
        ))
        
        # Step 5: Calculate confidence score
        confidence = calculate_confidence(context_chunks, metadatas)
        
        logger.info(
            f"RAG pipeline completed - Confidence: {confidence:.2f}, "
            f"Sources: {len(sources)}"
        )
        
        return answer, sources, confidence
        
    except Exception as e:
        logger.error(f"Error in RAG pipeline: {e}", exc_info=True)
        raise


def calculate_confidence(chunks: List[str], metadatas: List[dict]) -> float:
    """
    Calculate confidence score based on retrieval quality.
    
    Args:
        chunks: Retrieved context chunks
        metadatas: Metadata for chunks
        
    Returns:
        Confidence score between 0.0 and 1.0
    """
    if not chunks:
        return 0.0
    
    confidence = 0.5  # Base confidence
    
    # Increase confidence based on number of relevant chunks
    if len(chunks) >= config.rag.top_k_results:
        confidence += 0.2
    
    # Check metadata completeness
    complete_metadata = sum(
        1 for meta in metadatas 
        if meta.get("url") and meta.get("section")
    )
    metadata_score = complete_metadata / max(len(metadatas), 1)
    confidence += metadata_score * 0.3
    
    # Clamp to [0, 1]
    return min(1.0, max(0.0, confidence))
