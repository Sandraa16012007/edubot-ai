import time
from functools import wraps
from typing import Callable

class AgentTracer:
    """Trace agent execution times and flow"""
    
    def __init__(self):
        self.traces = []
    
    def trace_agent(self, agent_name: str):
        """Decorator to trace agent execution"""
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                
                trace_data = {
                    "agent": agent_name,
                    "function": func.__name__,
                    "start_time": start_time,
                    "status": "running"
                }
                
                try:
                    result = func(*args, **kwargs)
                    trace_data["status"] = "success"
                    trace_data["end_time"] = time.time()
                    trace_data["duration"] = trace_data["end_time"] - start_time
                    return result
                except Exception as e:
                    trace_data["status"] = "failed"
                    trace_data["error"] = str(e)
                    trace_data["end_time"] = time.time()
                    trace_data["duration"] = trace_data["end_time"] - start_time
                    raise
                finally:
                    self.traces.append(trace_data)
            
            return wrapper
        return decorator
    
    def get_trace_summary(self):
        """Get summary of all traces"""
        total_duration = sum(t.get("duration", 0) for t in self.traces)
        return {
            "total_traces": len(self.traces),
            "total_duration": total_duration,
            "traces": self.traces
        }