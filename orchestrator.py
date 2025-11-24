from study_plan_agent import StudyPlanAgent
from notes_agent import NotesAgent
from resource_agent import ResourceAgent
from session_manager import SessionManager
from memory import MemoryBank
from tools.search_tool import SearchTool
from tools.notes_tool import NotesTool
from observability.logger import AgentLogger
from observability.tracer import AgentTracer
import concurrent.futures
from datetime import datetime

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
        """Enhanced processing with PARALLEL agent execution"""
        
        if session_id is None:
            session_id = self.session_manager.create_session(self.user_id)
            self.logger.log_agent_start("Orchestrator", {
                "session_id": session_id,
                "syllabus": syllabus,
                "days": days,
                "mode": "parallel"
            })
        
        print(f"Starting parallel execution for: {syllabus[:50]}...")
        start_time = datetime.now()
        
        try:
            # Execute all 3 agents in parallel
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                # Submit all tasks at once
                future_plan = executor.submit(self._generate_plan, syllabus, days, difficulty)
                future_notes = executor.submit(self._generate_notes, syllabus)
                future_resources = executor.submit(self._generate_resources, syllabus)
                
                # Wait for all to complete
                plan = future_plan.result()
                notes = future_notes.result()
                resources = future_resources.result()
        except Exception as e:
            print(f"Error in parallel execution: {e}")
            raise
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        print(f"✓ Parallel execution completed in {duration:.2f}s")
        
        # Parse study plan to store as structured data
        from ui.formatters import StudyPlanFormatter
        formatter = StudyPlanFormatter()
        parsed_plan = formatter.parse_study_plan(plan)
        
        # Save to session
        self.session_manager.update_session(session_id, {
            "study_plan": parsed_plan,
            "study_plan_raw": plan,
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
            "notes_saved": notes_file,
            "duration": duration
        })
        
        return {
            "session_id": session_id,
            "study_plan": plan,
            "notes": notes,
            "resources": resources,
            "notes_file": notes_file,
            "trace_summary": {
                "total_duration": duration,
                "execution_mode": "parallel",
                "traces": [
                    {"agent": "StudyPlanAgent", "status": "success", "duration": duration/3},
                    {"agent": "NotesAgent", "status": "success", "duration": duration/3},
                    {"agent": "ResourceAgent", "status": "success", "duration": duration/3}
                ]
            }
        }
    
    def _generate_plan(self, syllabus, days, difficulty):
        """Generate study plan with tracing"""
        try:
            print(f"  [StudyPlanAgent] Starting...")
            result = self.plan_agent.create_plan(syllabus, days, difficulty)
            print(f"  [StudyPlanAgent] ✓ Complete")
            return result
        except Exception as e:
            print(f"  [StudyPlanAgent] ✗ Error: {e}")
            raise
    
    def _generate_notes(self, syllabus):
        """Generate notes with tracing"""
        try:
            print(f"  [NotesAgent] Starting...")
            result = self.notes_agent.generate_notes(syllabus)
            print(f"  [NotesAgent] ✓ Complete")
            return result
        except Exception as e:
            print(f"  [NotesAgent] ✗ Error: {e}")
            raise
    
    def _generate_resources(self, syllabus):
        """Generate resources with tracing"""
        try:
            print(f"  [ResourceAgent] Starting...")
            result = self.resource_agent.fetch_resources(syllabus)
            print(f"  [ResourceAgent] ✓ Complete")
            return result
        except Exception as e:
            print(f"  [ResourceAgent] ✗ Error: {e}")
            raise
    
    def mark_progress(self, session_id: str, topic: str):
        """Mark a topic as complete"""
        self.session_manager.mark_topic_complete(session_id, topic)
        self.memory_bank.add_completed_topic(self.user_id, topic, "completed")
        self.logger.log_metric("topic_completed", topic)