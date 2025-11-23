document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('study-form');
    const loading = document.getElementById('loading');
    const inputSection = document.getElementById('input-section');
    const resultsSection = document.getElementById('results-section');
    const historySection = document.getElementById('history-section');
    const userSection = document.getElementById('user-section');
    const generateBtn = document.getElementById('generate-btn');
    
    let currentSessionId = null;
    let currentUserId = 'web_user';
    let studyPlanData = [];

    // Load history button
    document.getElementById('load-history-btn').addEventListener('click', function() {
        const userId = document.getElementById('user-id-check').value.trim();
        if (userId) {
            currentUserId = userId;
            document.getElementById('user-id').value = userId;
            loadUserSessions(userId);
        } else {
            alert('Please enter your name to view your study history');
        }
    });

    // New session button
    document.getElementById('new-session-btn').addEventListener('click', function() {
        historySection.classList.add('hidden');
        inputSection.classList.remove('hidden');
        resultsSection.classList.add('hidden');
    });

    // Back to sessions button
    document.getElementById('back-to-sessions-btn').addEventListener('click', function() {
        resultsSection.classList.add('hidden');
        
        if (currentUserId) {
            loadUserSessions(currentUserId);
        } else {
            historySection.classList.add('hidden');
            userSection.classList.remove('hidden');
        }
    });

    async function loadUserSessions(userId) {
        try {
            historySection.classList.remove('hidden');
            userSection.classList.add('hidden');
            inputSection.classList.add('hidden');
            resultsSection.classList.add('hidden');
            
            document.getElementById('sessions-list').innerHTML = `
                <div class="loading-history">
                    <div class="spinner"></div>
                    <p>Loading your sessions...</p>
                </div>
            `;
            
            const response = await fetch(`/sessions/list/${userId}`);
            const data = await response.json();

            if (data.success && data.sessions.length > 0) {
                displaySessions(data.sessions);
            } else {
                document.getElementById('sessions-list').innerHTML = `
                    <div class="empty-sessions">
                        <i class="fas fa-inbox"></i>
                        <h3>No Previous Sessions Found</h3>
                        <p>Start your first study session below!</p>
                    </div>
                `;
                setTimeout(() => {
                    historySection.classList.add('hidden');
                    inputSection.classList.remove('hidden');
                }, 2000);
            }
        } catch (error) {
            console.error('Error loading sessions:', error);
            alert('Failed to load your sessions. Please try again.');
            historySection.classList.add('hidden');
            userSection.classList.remove('hidden');
        }
    }

    function displaySessions(sessions) {
        const sessionsList = document.getElementById('sessions-list');
        
        let html = '';
        sessions.forEach(session => {
            const date = new Date(session.created_at);
            const formattedDate = date.toLocaleDateString('en-US', { 
                month: 'short', 
                day: 'numeric', 
                year: 'numeric' 
            });
            
            html += `
                <div class="session-card-item" data-session-id="${session.session_id}">
                    <div class="session-header">
                        <div>
                            <div class="session-title">${session.syllabus}</div>
                            <div class="session-date">
                                <i class="fas fa-calendar"></i> ${formattedDate}
                            </div>
                        </div>
                        <div class="session-badge">${session.difficulty}</div>
                    </div>
                    
                    <div class="session-details">
                        <div class="session-detail">
                            <i class="fas fa-book"></i>
                            <span>${session.total_topics} topics</span>
                        </div>
                        <div class="session-detail">
                            <i class="fas fa-calendar-check"></i>
                            <span>${session.days} days</span>
                        </div>
                    </div>
                    
                    <div class="session-progress-bar">
                        <div class="session-progress-fill" style="width: ${session.completion_percentage}%"></div>
                    </div>
                    
                    <div class="session-footer">
                        <div class="session-progress-text">
                            <i class="fas fa-check-circle"></i>
                            ${session.completed_count}/${session.total_topics} completed (${session.completion_percentage}%)
                        </div>
                        <button class="session-resume-btn" onclick="event.stopPropagation()">
                            <i class="fas fa-play"></i> Resume
                        </button>
                    </div>
                </div>
            `;
        });
        
        sessionsList.innerHTML = html;
        
        // Add click handlers
        document.querySelectorAll('.session-card-item').forEach(card => {
            card.addEventListener('click', function() {
                const sessionId = this.dataset.sessionId;
                resumeSession(sessionId);
            });
            
            const resumeBtn = card.querySelector('.session-resume-btn');
            resumeBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                const sessionId = card.dataset.sessionId;
                resumeSession(sessionId);
            });
        });
    }

    async function resumeSession(sessionId) {
        try {
            loading.classList.remove('hidden');
            historySection.classList.add('hidden');
            inputSection.classList.add('hidden');
            userSection.classList.add('hidden');
            
            const response = await fetch(`/session/${sessionId}?user_id=${currentUserId}`);
            const data = await response.json();

            if (data.success) {
                const session = data.session;
                currentSessionId = sessionId;
                
                const formatter = { parse_study_plan: parseStudyPlan };
                studyPlanData = formatter.parse_study_plan(session.study_plan);
                
                displayResults({
                    session_id: sessionId,
                    study_plan: studyPlanData,
                    notes: session.notes || '',
                    resources: session.resources || '',
                    notes_file: session.notes_file || 'N/A',
                    trace_summary: { traces: [], total_duration: 0 }
                });
                
                initializeProgressTracking(studyPlanData, session.progress || {});
                
                loading.classList.add('hidden');
                resultsSection.classList.remove('hidden');
                resultsSection.scrollIntoView({ behavior: 'smooth' });
            }
        } catch (error) {
            console.error('Error resuming session:', error);
            alert('Failed to load session. Please try again.');
            loading.classList.add('hidden');
            historySection.classList.remove('hidden');
        }
    }

    function parseStudyPlan(planText) {
        try {
            if (typeof planText === 'object') return planText;
            
            let clean = planText;
            if (clean.startsWith('```')) {
                clean = clean.replace(/```json?/g, '').replace(/```/g, '').trim();
            }
            
            const parsed = JSON.parse(clean);
            return Array.isArray(parsed) ? parsed : [parsed];
        } catch (e) {
            console.error('Error parsing study plan:', e);
            return [];
        }
    }

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        currentUserId = document.getElementById('user-id').value || 'web_user';
        const syllabus = document.getElementById('syllabus').value;
        const days = document.getElementById('days').value;
        const difficulty = document.getElementById('difficulty').value;

        loading.classList.remove('hidden');
        inputSection.classList.add('hidden');
        userSection.classList.add('hidden');
        historySection.classList.add('hidden');
        resultsSection.classList.add('hidden');
        generateBtn.disabled = true;

        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: currentUserId,
                    syllabus: syllabus,
                    days: days,
                    difficulty: difficulty
                })
            });

            const data = await response.json();

            if (data.success) {
                currentSessionId = data.session_id;
                studyPlanData = data.study_plan;
                
                displayResults(data);
                initializeProgressTracking(data.study_plan);
                
                loading.classList.add('hidden');
                resultsSection.classList.remove('hidden');
                resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            } else {
                throw new Error(data.error || 'Failed to generate plan');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to generate study plan: ' + error.message);
            
            loading.classList.add('hidden');
            inputSection.classList.remove('hidden');
        } finally {
            generateBtn.disabled = false;
        }
    });

    function displayResults(data) {
        document.getElementById('session-id-display').textContent = data.session_id;
        document.getElementById('notes-file-display').textContent = data.notes_file;
        displayStudyPlan(data.study_plan);
        document.getElementById('notes-content').innerHTML = data.notes;
        document.getElementById('resources-content').innerHTML = data.resources;
        displayMetrics(data.trace_summary);
    }

    function displayStudyPlan(planData) {
        if (!planData || planData.length === 0) {
            document.getElementById('plan-overview').innerHTML = '<p>No plan data available</p>';
            return;
        }

        let tableHTML = `
            <table>
                <thead>
                    <tr>
                        <th><i class="fas fa-calendar"></i> Day</th>
                        <th><i class="fas fa-clock"></i> Time</th>
                        <th><i class="fas fa-book"></i> Topic</th>
                        <th><i class="fas fa-hourglass-half"></i> Duration</th>
                    </tr>
                </thead>
                <tbody>
        `;

        planData.forEach(session => {
            tableHTML += `
                <tr>
                    <td><strong>${session.day}</strong></td>
                    <td>${session.time_slot}</td>
                    <td>${session.topic}</td>
                    <td><span style="color: var(--success-color);">1-2 hrs</span></td>
                </tr>
            `;
        });

        tableHTML += '</tbody></table>';
        document.getElementById('plan-overview').innerHTML = tableHTML;

        const detailedHTML = displayDetailedSchedule(planData);
        document.getElementById('detailed-schedule').innerHTML = detailedHTML;
    }

    function displayDetailedSchedule(planData) {
        const days = {};
        planData.forEach(session => {
            const day = session.day;
            if (!days[day]) days[day] = [];
            days[day].push(session);
        });

        let html = '<div style="margin-top: 30px;">';

        Object.keys(days).sort((a, b) => a - b).forEach(dayNum => {
            html += `
                <div class="day-schedule">
                    <div class="day-header">
                        <i class="fas fa-calendar-day"></i> Day ${dayNum} Schedule
                    </div>
            `;

            days[dayNum].forEach((session) => {
                html += `
                    <div class="session-card">
                        <div class="session-time">
                            <i class="fas fa-clock"></i> ${session.time_slot}
                        </div>
                        <div class="session-topic">
                            <i class="fas fa-book-open"></i> ${session.topic}
                        </div>
                        ${session.description ? `<div class="session-description">${session.description}</div>` : ''}
                        ${session.activities && session.activities.length > 0 ? `
                            <div class="session-activities">
                                <h4><i class="fas fa-tasks"></i> Activities:</h4>
                                <ul>
                                    ${session.activities.map(activity => `<li>${activity}</li>`).join('')}
                                </ul>
                            </div>
                        ` : ''}
                        ${session.expected_outcome ? `
                            <div class="session-outcome">
                                <strong><i class="fas fa-check-circle"></i> Expected Outcome:</strong><br>
                                ${session.expected_outcome}
                            </div>
                        ` : ''}
                    </div>
                `;
            });

            html += '</div>';
        });

        html += '</div>';
        return html;
    }

    function displayMetrics(traceData) {
        if (!traceData || !traceData.traces) {
            document.getElementById('metrics-content').innerHTML = '<p>No metrics available</p>';
            return;
        }

        let html = '<div class="metrics-grid">';

        traceData.traces.forEach(trace => {
            const statusClass = trace.status === 'success' ? 'success' : 'failed';
            const statusIcon = trace.status === 'success' ? 'fa-check-circle' : 'fa-times-circle';
            
            html += `
                <div class="metric-item">
                    <div>
                        <div class="metric-label">
                            <i class="fas fa-robot"></i> ${trace.agent}
                        </div>
                        <span class="metric-status ${statusClass}">
                            <i class="fas ${statusIcon}"></i> ${trace.status}
                        </span>
                    </div>
                    <div class="metric-value">
                        ${trace.duration ? trace.duration.toFixed(2) : '0.00'}s
                    </div>
                </div>
            `;
        });

        html += '</div>';
        html += `
            <div style="margin-top: 20px; text-align: center; padding: 15px; background: var(--light); border-radius: 8px;">
                <strong style="font-size: 1.1rem;">
                    <i class="fas fa-stopwatch"></i> Total Processing Time:
                </strong> 
                <span style="color: var(--success-color); font-size: 1.3rem; font-weight: 700;">
                    ${traceData.total_duration.toFixed(2)}s
                </span>
            </div>
        `;

        document.getElementById('metrics-content').innerHTML = html;
    }

    function initializeProgressTracking(planData, existingProgress = {}) {
        if (!planData || planData.length === 0) return;

        const checklistContainer = document.getElementById('topics-checklist');
        let html = '';

        planData.forEach((session, index) => {
            const isCompleted = existingProgress.hasOwnProperty(session.topic);
            const completedClass = isCompleted ? 'completed' : '';
            
            html += `
                <div class="topic-item ${completedClass}" data-topic="${session.topic}" data-index="${index}">
                    <div class="topic-checkbox">
                        <i class="fas fa-check"></i>
                    </div>
                    <div class="topic-info">
                        <div class="topic-title">${session.topic}</div>
                        <div class="topic-time">
                            <i class="fas fa-clock"></i> ${session.time_slot}
                        </div>
                    </div>
                    <div class="topic-day-badge">Day ${session.day}</div>
                </div>
            `;
        });

        checklistContainer.innerHTML = html;

        document.querySelectorAll('.topic-item').forEach(item => {
            item.addEventListener('click', function() {
                toggleTopicCompletion(this);
            });
        });

        updateProgressStats();
    }

    async function toggleTopicCompletion(topicElement) {
        const topic = topicElement.dataset.topic;
        const isCompleted = topicElement.classList.contains('completed');

        try {
            if (!isCompleted) {
                topicElement.classList.add('completed');
                showCelebration();
                
                const response = await fetch(`/progress/${currentSessionId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        user_id: currentUserId,
                        topic: topic,
                        action: 'complete'
                    })
                });
                
                const data = await response.json();
                if (data.success && data.stats) {
                    console.log('Progress saved:', data.stats);
                }
            } else {
                topicElement.classList.remove('completed');
                
                await fetch(`/progress/${currentSessionId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        user_id: currentUserId,
                        topic: topic,
                        action: 'uncomplete'
                    })
                });
            }
        } catch (error) {
            console.error('Error updating progress:', error);
            if (!isCompleted) {
                topicElement.classList.remove('completed');
            } else {
                topicElement.classList.add('completed');
            }
        }

        updateProgressStats();
    }

    function updateProgressStats() {
        const allTopics = document.querySelectorAll('.topic-item');
        const completedTopics = document.querySelectorAll('.topic-item.completed');
        
        const total = allTopics.length;
        const completed = completedTopics.length;
        const remaining = total - completed;
        const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;

        document.getElementById('completed-count').textContent = completed;
        document.getElementById('remaining-count').textContent = remaining;
        document.getElementById('progress-percentage').textContent = percentage + '%';

        const progressBarFill = document.getElementById('progress-bar-fill');
        progressBarFill.style.width = percentage + '%';
        progressBarFill.textContent = percentage > 10 ? percentage + '%' : '';

        if (completed === total && total > 0) {
            showCompletionCelebration();
        }
    }

    function showCelebration() {
        const celebration = document.createElement('div');
        celebration.className = 'celebration';
        celebration.innerHTML = '🎉';
        document.body.appendChild(celebration);

        setTimeout(() => {
            celebration.remove();
        }, 1000);
    }

    function showCompletionCelebration() {
        const celebration = document.createElement('div');
        celebration.className = 'celebration';
        celebration.innerHTML = '🎊 All Done! 🎊';
        celebration.style.fontSize = '3rem';
        document.body.appendChild(celebration);

        setTimeout(() => {
            celebration.remove();
            alert('🎉 Congratulations! You\'ve completed your entire study plan!');
        }, 1500);
    }

    document.getElementById('refresh-progress-btn').addEventListener('click', function() {
        updateProgressStats();
        
        const btn = this;
        const icon = btn.querySelector('i');
        icon.style.animation = 'spin 1s linear';
        
        setTimeout(() => {
            icon.style.animation = '';
        }, 1000);
    });

    document.getElementById('export-btn').addEventListener('click', function() {
        const sessionId = document.getElementById('session-id-display').textContent;
        
        const planContent = document.getElementById('detailed-schedule').innerText;
        const notesContent = document.getElementById('notes-content').innerText;
        const resourcesContent = document.getElementById('resources-content').innerText;
        
        let markdown = '# Study Plan Export\n\n';
        markdown += `**Session ID:** ${sessionId}\n\n`;
        markdown += '---\n\n';
        markdown += '## Study Plan\n\n';
        markdown += planContent + '\n\n';
        markdown += '## Study Notes\n\n';
        markdown += notesContent + '\n\n';
        markdown += '## Learning Resources\n\n';
        markdown += resourcesContent + '\n\n';
        
        const blob = new Blob([markdown], { type: 'text/markdown' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `study_plan_${sessionId}.md`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        const exportBtn = document.getElementById('export-btn');
        const originalText = exportBtn.innerHTML;
        exportBtn.innerHTML = '<i class="fas fa-check"></i> Exported!';
        exportBtn.style.background = 'var(--success-color)';
        
        setTimeout(() => {
            exportBtn.innerHTML = originalText;
            exportBtn.style.background = '';
        }, 2000);
    });
});