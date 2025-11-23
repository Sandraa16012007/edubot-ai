from gemini_client import ask_gemini

class NotesAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def generate_notes(self, topic):
        prompt = f"""
You are a concise academic notes generator.

TASK:
Create clear, well-structured, exam-focused notes for the topic below in MARKDOWN format.

Topic: {topic}

FORMATTING RULES:
- Use proper markdown headers (##, ###)
- Use bullet points with proper nesting
- Use **bold** for key terms
- Use *italics* for emphasis
- Keep it crisp and structured
- Include formulas if relevant (use code blocks for equations)
- Do NOT add extra topics
- Keep it beginner friendly

Example Structure:
## Topic Name

### Key Concepts
- **Concept 1**: Definition
  - Sub-point 1
  - Sub-point 2
- **Concept 2**: Definition

### Important Points
- Point 1
- Point 2

Return output in proper markdown format (no code fences, just markdown).
"""
        return ask_gemini(prompt)