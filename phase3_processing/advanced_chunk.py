"""
Advanced semantic-aware text chunking for high-quality knowledge base construction.
Implements multiple chunking strategies and content filtering.
"""

import logging
import re
from typing import List, Dict, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Configuration
MIN_CHUNK_SIZE = 100
MAX_CHUNK_SIZE = 2000
QUALITY_THRESHOLD = 0.4


@dataclass
class Chunk:
    """Represents a processed chunk with metadata"""
    text: str
    metadata: Dict[str, any]
    chunk_id: str
    size: int
    
    def is_valid(self) -> bool:
        """Check if chunk meets quality criteria"""
        return len(self.text.strip()) >= MIN_CHUNK_SIZE


class NavigationFilter:
    """Filters out navigation and non-content text"""
    
    # Patterns that indicate navigation/non-content
    NAVIGATION_PATTERNS = [
        r'^\s*\[\s*[A-Za-z\s]+\s*\]\s*\(',  # [Link text]
        r'^\s*\*\s*\[\s*',  # Menu items
        r'logo\s*\)',
        r'javascript:void',
        r'!?\[.*?\]\(.*?\)',  # Images/links only
        r'Previous\s+Next',
        r'View All',
        r'Read More',
    ]
    
    # Keywords indicating low-value content
    LOW_VALUE_KEYWORDS = [
        'javascript', 'void(0)', 'image', 'png', 'jpg', 'svg',
        'icon/', 'storage/images', 'logo'
    ]
    
    @classmethod
    def is_navigation(cls, text: str) -> bool:
        """Check if text is primarily navigation"""
        lower_text = text.lower()
        
        # Check for navigation patterns
        for pattern in cls.NAVIGATION_PATTERNS:
            if re.search(pattern, text):
                return True
        
        # Check for low-value keywords
        keyword_count = sum(1 for kw in cls.LOW_VALUE_KEYWORDS 
                           if kw in lower_text)
        if keyword_count > 2:
            return True
        
        return False
    
    @classmethod
    def filter_text(cls, text: str) -> str:
        """Remove navigation elements from text"""
        # Remove image references
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
        
        # Remove standalone links with no context
        text = re.sub(r'^\s*\[\s*[A-Za-z\s]+\s*\]\s*\([^\)]+\)\s*$', '', text, flags=re.MULTILINE)
        
        # Remove javascript references
        text = re.sub(r'\]\s*\(javascript:[^\)]*\)', ']', text)
        
        # Clean up multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()


class SemanticChunker:
    """Semantic-aware chunking based on document structure"""
    
    def __init__(self):
        self.heading_pattern = re.compile(r'^#+\s+', re.MULTILINE)
        self.paragraph_pattern = re.compile(r'\n\n+')
        
    def chunk_by_semantics(self, text: str, source_url: str = "") -> List[Chunk]:
        """
        Split text into semantic chunks based on document structure.
        Respects headings, paragraphs, and maintains context.
        
        Args:
            text: Full text to chunk
            source_url: Source URL for metadata
            
        Returns:
            List of semantic chunks
        """
        chunks = []
        
        # Split by major sections (headings)
        sections = self._split_by_headings(text)
        
        chunk_id = 0
        for section_title, section_content in sections:
            # Further split large sections by paragraphs
            sub_chunks = self._chunk_section(
                section_content, 
                section_title,
                source_url,
                chunk_id
            )
            chunks.extend(sub_chunks)
            chunk_id += len(sub_chunks)
        
        return chunks
    
    def _split_by_headings(self, text: str) -> List[Tuple[str, str]]:
        """Split text by heading hierarchy"""
        sections = []
        current_heading = "Introduction"
        current_content = []
        
        for line in text.split('\n'):
            match = self.heading_pattern.match(line)
            if match:
                # Save previous section
                if current_content:
                    sections.append((
                        current_heading,
                        '\n'.join(current_content)
                    ))
                # Start new section
                current_heading = line.strip('#').strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Save last section
        if current_content:
            sections.append((current_heading, '\n'.join(current_content)))
        
        return sections
    
    def _chunk_section(self, text: str, section_title: str, 
                      source_url: str, start_id: int) -> List[Chunk]:
        """Chunk a section into manageable pieces"""
        chunks = []
        
        # Split by paragraphs
        paragraphs = self.paragraph_pattern.split(text)
        
        current_chunk = ""
        chunk_count = start_id
        
        for para in paragraphs:
            para = para.strip()
            if not para or len(para) < 20:
                continue
            
            # Add paragraph to current chunk
            if current_chunk:
                test_chunk = current_chunk + "\n\n" + para
            else:
                test_chunk = para
            
            # Check if adding this paragraph exceeds size limit
            if len(test_chunk) <= MAX_CHUNK_SIZE:
                current_chunk = test_chunk
            else:
                # Save current chunk if it's valid size
                if len(current_chunk) >= MIN_CHUNK_SIZE:
                    chunk = Chunk(
                        text=current_chunk,
                        metadata={
                            "section": section_title,
                            "url": source_url,
                            "content_type": "semantic",
                        },
                        chunk_id=f"{source_url}_{chunk_count}",
                        size=len(current_chunk)
                    )
                    if not NavigationFilter.is_navigation(current_chunk):
                        chunks.append(chunk)
                    chunk_count += 1
                
                # Start new chunk with current paragraph
                current_chunk = para
        
        # Save final chunk
        if len(current_chunk) >= MIN_CHUNK_SIZE:
            chunk = Chunk(
                text=current_chunk,
                metadata={
                    "section": section_title,
                    "url": source_url,
                    "content_type": "semantic",
                },
                chunk_id=f"{source_url}_{chunk_count}",
                size=len(current_chunk)
            )
            if not NavigationFilter.is_navigation(current_chunk):
                chunks.append(chunk)
        
        return chunks


class DuplicateRemover:
    """Removes duplicate and near-duplicate chunks"""
    
    @staticmethod
    def remove_duplicates(chunks: List[Chunk]) -> List[Chunk]:
        """Remove exact and near-duplicate chunks"""
        seen_texts = set()
        unique_chunks = []
        
        for chunk in chunks:
            # Create a normalized version for comparison
            normalized = ' '.join(chunk.text.split()).lower()
            
            # Use hash for fast duplicate detection
            text_hash = hash(normalized)
            
            if text_hash not in seen_texts:
                seen_texts.add(text_hash)
                unique_chunks.append(chunk)
            else:
                logger.debug(f"Removed duplicate chunk: {chunk.chunk_id}")
        
        return unique_chunks


class ChunkQualityScorer:
    """Scores chunk quality for filtering"""
    
    @staticmethod
    def score_chunk(chunk: Chunk) -> float:
        """
        Score chunk quality from 0.0 to 1.0.
        Higher score = better quality chunk.
        """
        score = 0.5  # Base score
        
        # Penalize if too small
        if chunk.size < config.chunking.min_chunk_size:
            score -= 0.3
        
        # Reward proper size
        if config.chunking.min_chunk_size <= chunk.size <= config.chunking.max_chunk_size:
            score += 0.2
        
        # Penalize high navigation content
        if NavigationFilter.is_navigation(chunk.text):
            score -= 0.5
        
        # Reward having metadata
        if chunk.metadata.get("section"):
            score += 0.1
        
        # Penalize broken text (incomplete sentences)
        if chunk.text.endswith(('tps://', 'http', '...')):
            score -= 0.2
        
        return max(0.0, min(1.0, score))  # Clamp to [0, 1]


def chunk_text_advanced(text: str, source_url: str = "") -> List[Chunk]:
    """
    Main function to chunk text with advanced strategy.
    
    Args:
        text: Full text to chunk
        source_url: Source URL for reference
        
    Returns:
        List of high-quality chunks
    """
    logger.info(f"Starting advanced chunking for: {source_url}")
    
    # Step 1: Filter navigation content
    if config.chunking.filter_navigation:
        text = NavigationFilter.filter_text(text)
    
    # Step 2: Semantic chunking
    chunker = SemanticChunker()
    chunks = chunker.chunk_by_semantics(text, source_url)
    
    # Step 3: Remove duplicates
    if config.chunking.remove_duplicates:
        chunks = DuplicateRemover.remove_duplicates(chunks)
    
    # Step 4: Quality filtering
    scorer = ChunkQualityScorer()
    filtered_chunks = []
    
    for chunk in chunks:
        quality_score = scorer.score_chunk(chunk)
        chunk.metadata["quality_score"] = quality_score
        
        if quality_score >= 0.4:  # Quality threshold
            filtered_chunks.append(chunk)
    
    logger.info(
        f"Chunking complete: {len(chunks)} semantic chunks → "
        f"{len(filtered_chunks)} high-quality chunks"
    )
    
    return filtered_chunks
