"""
Simple but effective chunking system with quality filtering.
Removes navigation noise and creates meaningful chunks.
"""

import re
from typing import List, Dict

class SimpleChunker:
    """Creates semantic chunks and filters low-quality content"""
    
    # Navigation patterns to exclude
    NAV_PATTERNS = [
        r'^\s*\[\s*[A-Za-z\s]+\s*\]\s*\(https?://',  # [Link]()
        r'^\s*\*\s*\[\s*',  # * [Menu
        r'javascript:void',
        r'Read More',
        r'View All',
        r'^\s*\[.*?\]\(.*?\)\s*$',  # Lines that are just links
    ]
    
    def is_navigation(self, text: str) -> bool:
        """Check if text is navigation/menu"""
        lower = text.lower()
        
        # Check for patterns
        for pattern in self.NAV_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        # Check for low-value keywords
        if any(kw in lower for kw in ['javascript', 'png', 'jpg', 'svg', 'logo', 'icon']):
            return True
        
        # Too many links, likely navigation
        link_count = len(re.findall(r'\]\(https?://', text))
        if link_count > 5 and len(text) < 500:
            return True
        
        return False
    
    def score_chunk(self, text: str) -> float:
        """Score chunk quality 0.0-1.0"""
        text = text.strip()
        
        # Minimum content check
        if len(text) < 50:
            return 0.0
        
        # Too long is also bad
        if len(text) > 4000:
            return 0.3
        
        # Count real words (not just links)
        words = re.findall(r'\b\w+\b', text)
        if len(words) < 10:
            return 0.2
        
        # Penalty for too many links
        links = len(re.findall(r'\]\(https?://', text))
        if links > len(words) * 0.4:
            return 0.2
        
        # Good chunk
        return 0.6 + (min(len(words), 400) / 400) * 0.4
    
    def chunk_text(self, text: str) -> List[str]:
        """Chunk text by paragraphs and semantic boundaries"""
        
        # Split by double newlines (paragraphs)
        paragraphs = re.split(r'\n\n+', text)
        
        chunks = []
        current_chunk = ""
        
        for para in paragraphs:
            para = para.strip()
            
            # Skip empty or very short paragraphs
            if not para or len(para) < 30:
                continue
            
            # Skip navigation
            if self.is_navigation(para):
                continue
            
            # Try to add to current chunk
            test = (current_chunk + "\n\n" + para).strip() if current_chunk else para
            
            # If too long, save current and start new
            if len(test) > 2000 and current_chunk:
                if self.score_chunk(current_chunk) >= 0.3:
                    chunks.append(current_chunk)
                current_chunk = para
            else:
                current_chunk = test
        
        # Save final chunk
        if current_chunk and self.score_chunk(current_chunk) >= 0.3:
            chunks.append(current_chunk)
        
        return chunks

def chunk_and_score(text: str) -> List[Dict]:
    """Chunk text and return scored chunks"""
    chunker = SimpleChunker()
    chunks = chunker.chunk_text(text)
    
    result = []
    for chunk in chunks:
        score = chunker.score_chunk(chunk)
        result.append({
            "text": chunk,
            "score": round(score, 2),
            "valid": score >= 0.5
        })
    
    return result
