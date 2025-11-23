# 🎓 Study Planner AI - Multi-Agent Study Planning System

An AI-powered study companion that generates personalized study plans, creates concise notes, curates quality resources, and tracks your learning progress.

## 🚀 Features

- **Multi-Agent System**: Coordinated AI agents for planning, note-taking, and resource curation
- **Progress Tracking**: Visual progress indicators with persistent storage
- **Session Management**: Resume your study sessions anytime
- **Smart Notes**: Auto-generated, exam-focused study notes
- **Resource Curation**: Curated learning materials for each topic
- **Performance Metrics**: Real-time observability and tracing

## 🛠️ Technologies

- **Backend**: Python, Flask, Google Gemini AI
- **Frontend**: HTML, CSS, JavaScript
- **Storage**: JSON-based session persistence
- **Observability**: Custom logging and tracing system

## 📦 Installation

### Prerequisites
- Python 3.8+
- Google API Key (Gemini)

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/study-planner-ai.git
cd study-planner-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```
GOOGLE_API_KEY=your_gemini_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
```

4. Run the application:
```bash
python web_app.py
```

5. Open browser to `http://localhost:5000`

## 🎯 Key Concepts Implemented

### 1. Multi-Agent System ✅
- **Sequential Execution**: Orchestrator coordinates 3 LLM-powered agents
- **Parallel Execution**: Agents run simultaneously for faster processing
- Agents: StudyPlanAgent, NotesAgent, ResourceAgent

### 2. Custom Tools ✅
- SearchTool for finding educational resources
- NotesTool for saving and managing study notes

### 3. Sessions & Memory ✅
- Session Management with JSON persistence
- Memory Bank for long-term user preference tracking
- Resume capability for incomplete sessions

### 4. Observability ✅
- Comprehensive logging system
- Execution time tracing
- Performance metrics tracking

## 📸 Screenshots

[Add screenshots here]

## 🎓 Capstone Project

This project demonstrates the application of multi-agent systems, session management, custom tools, and observability patterns for educational technology.

## 🌐 Live Demo

**Deployed Application**: https://study-planner-ai.onrender.com
**GitHub Repository**: https://github.com/YOUR_USERNAME/study-planner-ai

## 🚀 Deployment

This application is deployed on Render.com using:
- Automatic deployments from GitHub main branch
- Environment variables for API key management
- Gunicorn WSGI server for production

### Deployment Architecture
- **Hosting**: Render.com (Free tier)
- **Server**: Gunicorn
- **Storage**: JSON-based file system
- **CI/CD**: Automatic deployment on git push

## 📝 License

MIT License

