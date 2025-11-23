import os
import json
from datetime import datetime
from typing import List, Dict

class NotesTool:
    """Tool for managing and saving study notes"""
    
    def __init__(self, notes_dir="saved_notes"):
        self.notes_dir = notes_dir
        os.makedirs(notes_dir, exist_ok=True)
    
    def save_notes(self, topic: str, content: str, user_id: str) -> str:
        """Save notes to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{user_id}_{topic.replace(' ', '_')}_{timestamp}.txt"
        filepath = os.path.join(self.notes_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"Topic: {topic}\n")
            f.write(f"Created: {datetime.now().isoformat()}\n")
            f.write("="*50 + "\n\n")
            f.write(content)
        
        return filepath
    
    def load_notes(self, user_id: str, topic: str = None) -> List[Dict[str, str]]:
        """Load saved notes for a user"""
        notes = []
        for filename in os.listdir(self.notes_dir):
            if filename.startswith(user_id):
                if topic and topic.replace(' ', '_') not in filename:
                    continue
                
                filepath = os.path.join(self.notes_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    notes.append({
                        "filename": filename,
                        "content": content
                    })
        
        return notes