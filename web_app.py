from flask import Flask, render_template, request, jsonify, session
import os
from dotenv import load_dotenv
from datetime import datetime
import json
import markdown2
import glob

load_dotenv()

from gemini_client import init_gemini
from orchestrator import Orchestrator
from ui.formatters import StudyPlanFormatter

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "your-secret-key-here")

# Initialize Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables.")
init_gemini(api_key)

def clean_and_format_markdown(text):
    """Clean and convert text to HTML with markdown"""
    if text.startswith("```"):
        text = text.strip("`")
        text = text.replace("json", "", 1).replace("markdown", "", 1).strip()
    
    html = markdown2.markdown(text, extras=[
        "fenced-code-blocks",
        "tables",
        "break-on-newline",
        "cuddled-lists",
        "code-friendly",
        "header-ids"
    ])
    
    return html

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_plan():
    """Generate study plan"""
    try:
        data = request.json
        syllabus = data.get('syllabus')
        days = data.get('days')
        difficulty = data.get('difficulty')
        user_id = data.get('user_id', 'web_user')
        
        if not all([syllabus, days, difficulty]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        orchestrator = Orchestrator(api_key, user_id=user_id)
        result = orchestrator.process(syllabus, days, difficulty)
        
        formatter = StudyPlanFormatter()
        plan_data = formatter.parse_study_plan(result["study_plan"])
        
        notes_html = clean_and_format_markdown(result["notes"])
        resources_html = clean_and_format_markdown(result["resources"])
        
        return jsonify({
            'success': True,
            'session_id': result['session_id'],
            'study_plan': plan_data,
            'notes': notes_html,
            'resources': resources_html,
            'notes_file': result['notes_file'],
            'trace_summary': result['trace_summary']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/progress/<session_id>', methods=['POST'])
def mark_progress(session_id):
    """Mark topic as complete"""
    try:
        data = request.json
        topic = data.get('topic')
        user_id = data.get('user_id', 'web_user')
        action = data.get('action', 'complete')  # 'complete' or 'uncomplete'
        
        orchestrator = Orchestrator(api_key, user_id=user_id)
        
        if action == 'complete':
            orchestrator.mark_progress(session_id, topic)
        else:
            # Unmark progress
            session_data = orchestrator.session_manager.load_session(session_id)
            if 'progress' in session_data and topic in session_data['progress']:
                del session_data['progress'][topic]
                orchestrator.session_manager.update_session(session_id, {'progress': session_data['progress']})
        
        # Get updated session to return stats
        updated_session = orchestrator.session_manager.load_session(session_id)
        progress = updated_session.get('progress', {})
        
        # Parse study plan to get total topics
        formatter = StudyPlanFormatter()
        plan_data = formatter.parse_study_plan(updated_session.get('study_plan', '[]'))
        total_topics = len(plan_data)
        completed_count = len(progress)
        completion_percentage = round((completed_count / total_topics) * 100) if total_topics > 0 else 0
        
        return jsonify({
            'success': True,
            'message': f'Marked {topic} as {"complete" if action == "complete" else "incomplete"}',
            'stats': {
                'completed_count': completed_count,
                'total_topics': total_topics,
                'completion_percentage': completion_percentage
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/session/<session_id>', methods=['GET'])
def get_session(session_id):
    """Get session data"""
    try:
        user_id = request.args.get('user_id', 'web_user')
        orchestrator = Orchestrator(api_key, user_id=user_id)
        session_data = orchestrator.session_manager.load_session(session_id)
        
        # Format notes and resources if they exist
        if session_data.get('notes'):
            session_data['notes'] = clean_and_format_markdown(session_data['notes'])
        if session_data.get('resources'):
            session_data['resources'] = clean_and_format_markdown(session_data['resources'])
        
        return jsonify({
            'success': True,
            'session': session_data
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sessions/list/<user_id>', methods=['GET'])
def list_user_sessions(user_id):
    """List all sessions for a user"""
    try:
        sessions_dir = "sessions"
        user_sessions = []
        
        # Find all session files for this user
        pattern = os.path.join(sessions_dir, f"{user_id}_*.json")
        session_files = glob.glob(pattern)
        
        for filepath in session_files:
            try:
                with open(filepath, 'r') as f:
                    session_data = json.load(f)
                    
                    # Parse study plan to get accurate topic count
                    study_plan = session_data.get('study_plan', [])
                    
                    # If study_plan is a string (JSON), parse it
                    if isinstance(study_plan, str):
                        try:
                            formatter = StudyPlanFormatter()
                            study_plan = formatter.parse_study_plan(study_plan)
                        except:
                            study_plan = []
                    
                    # Ensure it's a list
                    if not isinstance(study_plan, list):
                        study_plan = []
                    
                    total_topics = len(study_plan)
                    
                    # Extract key info
                    session_info = {
                        'session_id': session_data.get('session_id'),
                        'created_at': session_data.get('created_at'),
                        'last_updated': session_data.get('last_updated', session_data.get('created_at')),
                        'syllabus': session_data.get('syllabus', 'N/A'),
                        'days': session_data.get('days', 'N/A'),
                        'difficulty': session_data.get('difficulty', 'N/A'),
                        'progress': session_data.get('progress', {}),
                        'total_topics': total_topics
                    }
                    
                    # Calculate completion stats
                    completed_count = len(session_info['progress'])
                    session_info['completed_count'] = completed_count
                    session_info['completion_percentage'] = (
                        round((completed_count / session_info['total_topics']) * 100) 
                        if session_info['total_topics'] > 0 else 0
                    )
                    
                    user_sessions.append(session_info)
            except Exception as e:
                print(f"Error reading session file {filepath}: {e}")
                continue
        
        # Sort by last updated (most recent first)
        user_sessions.sort(key=lambda x: x.get('last_updated', ''), reverse=True)
        
        return jsonify({
            'success': True,
            'sessions': user_sessions,
            'count': len(user_sessions)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # For local development
    # app.run(debug=True, port=5000)
    
    # For production
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)