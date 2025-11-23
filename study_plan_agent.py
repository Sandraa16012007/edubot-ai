from gemini_client import ask_gemini

class StudyPlanAgent:
    def __init__(self, api_key):
        self.api_key = api_key

    def create_plan(self, syllabus, days, difficulty):
        prompt = f"""
You are an academic planning agent that creates structured study schedules.

Input:
- Syllabus/Topics: {syllabus}
- Total study days: {days}
- Difficulty level: {difficulty}

Task:
Create a detailed day-by-day study schedule. Return ONLY valid JSON (no markdown, no code fences).

JSON Structure:
[
  {{
    "day": 1,
    "time_slot": "9:00 AM - 11:00 AM",
    "topic": "Topic Name",
    "description": "Brief description of what will be covered",
    "activities": [
      "Activity 1",
      "Activity 2"
    ],
    "expected_outcome": "What the student should achieve"
  }}
]

Rules:
1. Divide each day into 3-5 study sessions
2. Each session should be 1-2 hours
3. Include breaks
4. Adjust complexity based on difficulty level: {difficulty}
5. Progressive learning: start with basics, build up
6. Return ONLY the JSON array, nothing else

Generate the study plan now:
"""
        return ask_gemini(prompt)