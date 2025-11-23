import json
import os
from typing import List, Dict, Any

class MemoryBank:
    """Long-term memory for user preferences and learning patterns"""
    
    def __init__(self, memory_file="sessions/memory_bank.json"):
        self.memory_file = memory_file
        self._ensure_memory_file()
    
    def _ensure_memory_file(self):
        """Create memory file if it doesn't exist"""
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, 'w') as f:
                json.dump({}, f)
    
    def add_learning_preference(self, user_id: str, preference: Dict[str, Any]):
        """Store user learning preferences"""
        memory = self._load_memory()
        
        if user_id not in memory:
            memory[user_id] = {
                "preferences": [],
                "completed_topics": [],
                "difficulty_history": []
            }
        
        memory[user_id]["preferences"].append(preference)
        self._save_memory(memory)
    
    def get_user_history(self, user_id: str) -> Dict[str, Any]:
        """Retrieve user's learning history"""
        memory = self._load_memory()
        return memory.get(user_id, {})
    
    def add_completed_topic(self, user_id: str, topic: str, performance: str):
        """Track completed topics"""
        memory = self._load_memory()
        
        if user_id not in memory:
            memory[user_id] = {"completed_topics": []}
        
        memory[user_id]["completed_topics"].append({
            "topic": topic,
            "performance": performance,
            "completed_at": json.dumps({"time": "now"})  # simplified
        })
        self._save_memory(memory)
    
    def _load_memory(self) -> Dict[str, Any]:
        with open(self.memory_file, 'r') as f:
            return json.load(f)
    
    def _save_memory(self, memory: Dict[str, Any]):
        with open(self.memory_file, 'w') as f:
            json.dump(memory, f, indent=2)