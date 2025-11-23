from gemini_client import ask_gemini

class ResourceAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def fetch_resources(self, study_plan_text):
        prompt = f"""
You are a resource-curation agent.
Given this study plan, produce 2–4 HIGH-QUALITY verified resources per topic in MARKDOWN format.

Rules:
- ONLY include real, verified resources (YouTube channels, official docs, high-quality blogs)
- Format as proper markdown with headers and lists
- Include clickable links [Link Text](URL)
- Add a short 1-line description for each resource
- Group by topic using headers

Study Plan:
{study_plan_text}

Example Format:
## Topic 1: Introduction to Machine Learning

### Video Resources
- [Machine Learning Crash Course](https://youtube.com/watch?v=example) - Comprehensive introduction by Google
- [ML Fundamentals](https://coursera.org/example) - Stanford University course

### Reading Materials
- [ML Basics Guide](https://example.com/ml-guide) - Easy-to-understand beginner guide
- [Official TensorFlow Docs](https://tensorflow.org/tutorials) - Official documentation

Return in markdown format (no code fences).
"""
        return ask_gemini(prompt)