from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.markdown import Markdown
from ui.formatters import StudyPlanFormatter

class CLIInterface:
    def __init__(self):
        self.console = Console()
        self.formatter = StudyPlanFormatter()
    
    def show_welcome(self):
        welcome_text = """
# 🎓 Study Planner Agent System
        
Your AI-powered study companion that:
- 📅 Creates personalized study plans
- 📝 Generates concise notes
- 🔗 Curates quality resources
- 📊 Tracks your progress
        """
        self.console.print(Panel(Markdown(welcome_text), title="Welcome", border_style="blue"))
    
    def get_user_input(self):
        self.console.print("\n[bold cyan]Let's create your study plan![/bold cyan]\n")
        
        syllabus = self.console.input("[yellow]📚 Enter syllabus/topics:[/yellow] ")
        days = self.console.input("[yellow]📅 Number of days:[/yellow] ")
        difficulty = self.console.input("[yellow]⚡ Difficulty (easy/medium/hard):[/yellow] ")
        
        return syllabus, days, difficulty
    
    def show_processing(self, task_name: str):
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
        ) as progress:
            progress.add_task(description=f"Processing {task_name}...", total=None)
    
    def display_study_plan(self, plan_text: str):
        """Display study plan in beautiful schedule format"""
        self.console.print("\n")
        
        # Parse the plan
        plan_data = self.formatter.parse_study_plan(plan_text)
        
        if not plan_data:
            # Fallback to raw display if parsing fails
            self.console.print(Panel(
                Markdown(self._clean_output(plan_text)),
                title="📅 Your Study Plan",
                border_style="green"
            ))
            return
        
        # Display overview table
        self.console.print(Panel(
            self.formatter.format_as_table(plan_data),
            title="📊 Schedule Overview",
            border_style="cyan"
        ))
        
        # Ask user for detailed view
        show_details = self.console.input(
            "\n[yellow]Show detailed daily breakdown? (yes/no):[/yellow] "
        ).lower() in ['yes', 'y']
        
        if show_details:
            # Display detailed schedule
            self.formatter.format_as_schedule(plan_data, self.console)
        
        # Offer to export
        export = self.console.input(
            "\n[yellow]Export plan to markdown file? (yes/no):[/yellow] "
        ).lower() in ['yes', 'y']
        
        if export:
            markdown_content = self.formatter.format_study_plan_markdown(plan_data)
            filename = "study_plan_export.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            self.console.print(f"[green]✓ Plan exported to {filename}[/green]")
    
    def display_notes(self, notes_text: str):
        self.console.print("\n")
        self.console.print(Panel(
            Markdown(self._clean_output(notes_text)),
            title="📝 Study Notes",
            border_style="blue"
        ))
    
    def display_resources(self, resources_text: str):
        self.console.print("\n")
        self.console.print(Panel(
            Markdown(self._clean_output(resources_text)),
            title="🔗 Learning Resources",
            border_style="magenta"
        ))
    
    def display_session_info(self, session_id: str, notes_file: str):
        info_table = Table(title="📋 Session Information")
        info_table.add_column("Property", style="cyan")
        info_table.add_column("Value", style="green")
        
        info_table.add_row("Session ID", session_id)
        info_table.add_row("Notes Saved", notes_file)
        
        self.console.print("\n")
        self.console.print(info_table)
    
    def display_trace_summary(self, trace_data: dict):
        self.console.print("\n[bold cyan]⚡ Performance Metrics:[/bold cyan]")
        
        metrics_table = Table()
        metrics_table.add_column("Agent", style="cyan")
        metrics_table.add_column("Duration (s)", style="green", justify="right")
        metrics_table.add_column("Status", style="yellow")
        
        for trace in trace_data.get("traces", []):
            status_emoji = "✓" if trace.get("status") == "success" else "✗"
            metrics_table.add_row(
                trace.get("agent", "Unknown"),
                f"{trace.get('duration', 0):.2f}",
                f"{status_emoji} {trace.get('status', 'unknown')}"
            )
        
        self.console.print(metrics_table)
        self.console.print(f"\n[green]Total Duration: {trace_data.get('total_duration', 0):.2f}s[/green]")
    
    def _clean_output(self, text: str) -> str:
        """Clean markdown code fences"""
        if text.startswith("```"):
            text = text.strip("`")
            text = text.replace("json", "", 1).strip()
        return text
    
    def ask_continue(self) -> bool:
        response = self.console.input("\n[yellow]Would you like to refine your plan? (yes/no):[/yellow] ")
        return response.lower() in ['yes', 'y']
    
    def show_progress_menu(self, session_id: str):
        """Show menu for tracking progress"""
        self.console.print("\n[bold cyan]📊 Progress Tracking Menu[/bold cyan]")
        self.console.print("1. Mark topic as complete")
        self.console.print("2. View current progress")
        self.console.print("3. Continue studying")
        self.console.print("4. Exit")
        
        choice = self.console.input("\n[yellow]Choose an option:[/yellow] ")
        return choice