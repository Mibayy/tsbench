import re
import unicodedata


def slugify(text: str) -> str:
    """Convert a string to a URL-safe slug.
    
    Rules:
    - lowercase
    - spaces and underscores → single dash
    - remove accents (é→e, ü→u, ç→c)
    - remove non-alphanumeric chars (except dashes)
    - strip dashes from start/end
    - collapse consecutive dashes
    """
    # Lowercase
    text = text.lower()
    
    # Handle special characters that NFKD doesn't decompose well
    replacements = {'ł': 'l'}
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Remove accents using NFKD normalization
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # Replace spaces and underscores with dashes
    text = re.sub(r'[ _]+', '-', text)
    
    # Remove non-alphanumeric chars except dashes
    text = re.sub(r'[^a-z0-9\-]', '', text)
    
    # Collapse consecutive dashes
    text = re.sub(r'-+', '-', text)
    
    # Strip dashes from start/end
    text = text.strip('-')
    
    return text
