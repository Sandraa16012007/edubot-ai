import json
import os
from datetime import datetime
from typing import Dict, Any, List

class SessionManager:
    """Manages user sessions and study progress"""
    
    def __init__(self, session_dir="sessions"):
        self.session_dir = session_dir
        os.makedirs(session_dir, exist_ok=True)
    
    def create_session(self, user_id: str) -> str:
        """Create a new study session"""
        session_id = f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "study_plan": None,
            "progress": {},
            "notes_history": [],
            "refinements": []
        }
        self._save_session(session_id, session_data)
        return session_id
    
    def load_session(self, session_id: str) -> Dict[str, Any]:
        """Load existing session"""
        filepath = os.path.join(self.session_dir, f"{session_id}.json")
        if not os.path.exists(filepath):
            raise ValueError(f"Session {session_id} not found")
        
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def update_session(self, session_id: str, updates: Dict[str, Any]):
        """Update session data"""
        session_data = self.load_session(session_id)
        session_data.update(updates)
        session_data["last_updated"] = datetime.now().isoformat()
        self._save_session(session_id, session_data)
    
    def _save_session(self, session_id: str, data: Dict[str, Any]):
        """Save session to disk"""
        filepath = os.path.join(self.session_dir, f"{session_id}.json")
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def mark_topic_complete(self, session_id: str, topic: str):
        """Track completed topics"""
        session_data = self.load_session(session_id)
        if "progress" not in session_data:
            session_data["progress"] = {}
        
        session_data["progress"][topic] = {
            "completed": True,
            "completed_at": datetime.now().isoformat()
        }
        self._save_session(session_id, session_data)