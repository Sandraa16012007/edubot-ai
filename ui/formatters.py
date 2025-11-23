import json
from typing import Dict, List, Any
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich.markdown import Markdown

class StudyPlanFormatter:
    """Formats study plan data into readable output"""
    
    @staticmethod
    def clean_json_output(text: str) -> str:
        """Remove markdown code fences from JSON"""
        if text.startswith("```"):
            text = text.strip("`")
            # Remove language labels
            for lang in ["json", "JSON"]:
                text = text.replace(lang, "", 1)
        return text.strip()
    
    @staticmethod
    def parse_study_plan(plan_text: str) -> List[Dict[str, Any]]:
        """Parse study plan from text to JSON"""
        try:
            clean_text = StudyPlanFormatter.clean_json_output(plan_text)
            plan_data = json.loads(clean_text)
            
            # Handle if it's wrapped in an object
            if isinstance(plan_data, dict) and "plan" in plan_data:
                plan_data = plan_data["plan"]
            
            return plan_data if isinstance(plan_data, list) else [plan_data]
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return []
    
    @staticmethod
    def format_as_schedule(plan_data: List[Dict[str, Any]], console: Console) -> None:
        """Format study plan as a daily schedule"""
        
        if not plan_data:
            console.print("[red]No valid study plan data to display[/red]")
            return
        
        # Group by day
        days = {}
        for session in plan_data:
            day = session.get("day", 1)
            if day not in days:
                days[day] = []
            days[day].append(session)
        
        # Display each day
        for day_num in sorted(days.keys()):
            StudyPlanFormatter._display_day(day_num, days[day_num], console)
    
    @staticmethod
    def _display_day(day_num: int, sessions: List[Dict], console: Console):
        """Display a single day's schedule"""
        
        # Create day header
        day_title = f"📅 Day {day_num} Schedule"
        console.print(f"\n[bold cyan]{day_title}[/bold cyan]")
        console.print("─" * 80)
        
        for idx, session in enumerate(sessions, 1):
            time_slot = session.get("time_slot", "N/A")
            topic = session.get("topic", "Untitled Topic")
            description = session.get("description", "")
            activities = session.get("activities", [])
            outcome = session.get("expected_outcome", "")
            
            # Create session panel
            session_content = []
            
            # Time and Topic
            session_content.append(f"[bold yellow]⏰ {time_slot}[/bold yellow]")
            session_content.append(f"[bold green]📚 {topic}[/bold green]\n")
            
            # Description
            if description:
                session_content.append(f"[italic]{description}[/italic]\n")
            
            # Activities
            if activities:
                session_content.append("[bold cyan]Activities:[/bold cyan]")
                for activity in activities:
                    session_content.append(f"  • {activity}")
                session_content.append("")
            
            # Expected Outcome
            if outcome:
                session_content.append(f"[bold magenta]Expected Outcome:[/bold magenta]")
                session_content.append(f"  ✓ {outcome}")
            
            # Display panel
            panel_content = "\n".join(session_content)
            console.print(Panel(
                panel_content,
                title=f"Session {idx}",
                border_style="blue",
                padding=(1, 2)
            ))
    
    @staticmethod
    def format_as_table(plan_data: List[Dict[str, Any]]) -> Table:
        """Format study plan as a compact table"""
        
        table = Table(title="📅 Study Schedule Overview", show_header=True, header_style="bold cyan")
        table.add_column("Day", style="cyan", width=6)
        table.add_column("Time", style="yellow", width=18)
        table.add_column("Topic", style="green", width=35)
        table.add_column("Duration", style="magenta", width=10)
        
        for session in plan_data:
            day = str(session.get("day", "?"))
            time_slot = session.get("time_slot", "N/A")
            topic = session.get("topic", "Untitled")
            
            # Calculate duration from time slot
            duration = StudyPlanFormatter._calculate_duration(time_slot)
            
            # Truncate long topics
            if len(topic) > 32:
                topic = topic[:32] + "..."
            
            table.add_row(day, time_slot, topic, duration)
        
        return table
    
    @staticmethod
    def _calculate_duration(time_slot: str) -> str:
        """Calculate duration from time slot string"""
        try:
            if " - " in time_slot:
                start, end = time_slot.split(" - ")
                # Simple duration calculation (could be improved)
                return "1-2 hrs"
            return "N/A"
        except:
            return "N/A"
    
    @staticmethod
    def format_study_plan_markdown(plan_data: List[Dict[str, Any]]) -> str:
        """Format as markdown for export"""
        
        markdown = "# 📚 Your Study Plan\n\n"
        
        days = {}
        for session in plan_data:
            day = session.get("day", 1)
            if day not in days:
                days[day] = []
            days[day].append(session)
        
        for day_num in sorted(days.keys()):
            markdown += f"## Day {day_num}\n\n"
            
            for session in days[day_num]:
                time_slot = session.get("time_slot", "N/A")
                topic = session.get("topic", "Untitled")
                description = session.get("description", "")
                activities = session.get("activities", [])
                outcome = session.get("expected_outcome", "")
                
                markdown += f"### {time_slot} - {topic}\n\n"
                
                if description:
                    markdown += f"*{description}*\n\n"
                
                if activities:
                    markdown += "**Activities:**\n"
                    for activity in activities:
                        markdown += f"- {activity}\n"
                    markdown += "\n"
                
                if outcome:
                    markdown += f"**Expected Outcome:** {outcome}\n\n"
                
                markdown += "---\n\n"
        
        return markdown