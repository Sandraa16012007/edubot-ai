import logging
import json
from datetime import datetime
from typing import Any, Dict

class AgentLogger:
    """Logging system for agent activities"""
    
    def __init__(self, log_file="logs/agent_activity.log"):
        self.log_file = log_file
        self._setup_logger()
    
    def _setup_logger(self):
        import os
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("StudyPlannerAgent")
    
    def log_agent_start(self, agent_name: str, inputs: Dict[str, Any]):
        """Log when an agent starts processing"""
        self.logger.info(f"[START] {agent_name} | Inputs: {json.dumps(inputs)}")
    
    def log_agent_complete(self, agent_name: str, outputs: Dict[str, Any]):
        """Log when an agent completes"""
        self.logger.info(f"[COMPLETE] {agent_name} | Outputs size: {len(str(outputs))}")
    
    def log_error(self, agent_name: str, error: Exception):
        """Log errors"""
        self.logger.error(f"[ERROR] {agent_name} | {str(error)}")
    
    def log_metric(self, metric_name: str, value: Any):
        """Log performance metrics"""
        self.logger.info(f"[METRIC] {metric_name}: {value}")