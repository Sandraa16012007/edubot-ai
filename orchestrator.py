from study_plan_agent import StudyPlanAgent
from notes_agent import NotesAgent
from resource_agent import ResourceAgent
from session_manager import SessionManager
from memory import MemoryBank
from tools.search_tool import SearchTool
from tools.notes_tool import NotesTool
from observability.logger import AgentLogger
from observability.tracer import AgentTracer

class Orchestrator:
    def __init__(self, api_key, user_id="default_user"):
        # Agents
        self.plan_agent = StudyPlanAgent(api_key)
        self.notes_agent = NotesAgent(api_key)
        self.resource_agent = ResourceAgent(api_key)
        
        # Session & Memory
        self.session_manager = SessionManager()
        self.memory_bank = MemoryBank()
        self.user_id = user_id
        
        # Tools
        self.search_tool = SearchTool()
        self.notes_tool = NotesTool()
        
        # Observability
        self.logger = AgentLogger()
        self.tracer = AgentTracer()
    
    def process(self, syllabus, days, difficulty, session_id=None):
        """Enhanced processing with session management"""
        
        # Create or load session
        if session_id is None:
            session_id = self.session_manager.create_session(self.user_id)
            self.logger.log_agent_start("Orchestrator", {
                "session_id": session_id,
                "syllabus": syllabus,
                "days": days
            })
        
        # Execute agents with tracing
        @self.tracer.trace_agent("StudyPlanAgent")
        def generate_plan():
            return self.plan_agent.create_plan(syllabus, days, difficulty)
        
        @self.tracer.trace_agent("NotesAgent")
        def generate_notes():
            return self.notes_agent.generate_notes(syllabus)
        
        @self.tracer.trace_agent("ResourceAgent")
        def fetch_resources():
            return self.resource_agent.fetch_resources(syllabus)
        
        # Generate content
        plan = generate_plan()
        notes = generate_notes()
        resources = fetch_resources()
        
        # Parse study plan to store as structured data
        from ui.formatters import StudyPlanFormatter
        formatter = StudyPlanFormatter()
        parsed_plan = formatter.parse_study_plan(plan)
        
        # Save to session (store both raw and parsed)
        self.session_manager.update_session(session_id, {
            "study_plan": parsed_plan,  # Store as list instead of string
            "study_plan_raw": plan,     # Keep original for reference
            "notes": notes,
            "resources": resources,
            "syllabus": syllabus,
            "days": days,
            "difficulty": difficulty
        })
        
        # Save notes to file
        notes_file = self.notes_tool.save_notes(
            topic=syllabus,
            content=notes,
            user_id=self.user_id
        )
        
        # Update memory bank
        self.memory_bank.add_learning_preference(self.user_id, {
            "difficulty": difficulty,
            "topic": syllabus
        })
        
        # Log completion
        self.logger.log_agent_complete("Orchestrator", {
            "session_id": session_id,
            "notes_saved": notes_file
        })
        
        return {
            "session_id": session_id,
            "study_plan": plan,  # Return raw for backward compatibility
            "notes": notes,
            "resources": resources,
            "notes_file": notes_file,
            "trace_summary": self.tracer.get_trace_summary()
        }
    
    def mark_progress(self, session_id: str, topic: str):
        """Mark a topic as complete"""
        self.session_manager.mark_topic_complete(session_id, topic)
        self.memory_bank.add_completed_topic(self.user_id, topic, "completed")
        self.logger.log_metric("topic_completed", topic)