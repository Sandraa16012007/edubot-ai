import os
from dotenv import load_dotenv
load_dotenv()

from gemini_client import init_gemini
from orchestrator import Orchestrator
from ui.cli_interface import CLIInterface

def main():
    # Initialize
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")
    
    init_gemini(api_key)
    ui = CLIInterface()
    
    # Show welcome screen
    ui.show_welcome()
    
    # Get user input
    syllabus, days, difficulty = ui.get_user_input()
    
    # Get or create user ID
    user_id = input("\n[Optional] Enter your user ID (press Enter for 'student'): ").strip() or "student"
    
    # Create orchestrator
    system = Orchestrator(api_key, user_id=user_id)
    
    # Process with loading indicator
    ui.console.print("\n[bold green]🔄 Generating your personalized study plan...[/bold green]")
    
    try:
        result = system.process(syllabus, days, difficulty)
        
        # Display results with new formatting
        ui.display_study_plan(result["study_plan"])
        ui.display_notes(result["notes"])
        ui.display_resources(result["resources"])
        ui.display_session_info(result["session_id"], result["notes_file"])
        ui.display_trace_summary(result["trace_summary"])
        
        # Progress tracking loop
        while True:
            choice = ui.show_progress_menu(result["session_id"])
            
            if choice == "1":
                topic = ui.console.input("[yellow]Enter topic name to mark complete:[/yellow] ")
                system.mark_progress(result["session_id"], topic)
                ui.console.print(f"[green]✓ Marked '{topic}' as complete![/green]")
            
            elif choice == "2":
                session_data = system.session_manager.load_session(result["session_id"])
                progress = session_data.get("progress", {})
                
                if progress:
                    ui.console.print("\n[bold cyan]Completed Topics:[/bold cyan]")
                    for topic, info in progress.items():
                        ui.console.print(f"  ✓ {topic}")
                else:
                    ui.console.print("[yellow]No topics completed yet![/yellow]")
            
            elif choice == "3":
                ui.console.print("[green]Happy studying! 📚[/green]")
                break
            
            elif choice == "4":
                ui.console.print("[green]Goodbye! Your progress has been saved. 👋[/green]")
                break
            
            else:
                ui.console.print("[red]Invalid choice. Please try again.[/red]")
        
        # Ask if they want to refine
        if ui.ask_continue():
            refinement = ui.console.input("\n[yellow]What would you like to change?[/yellow] ")
            ui.console.print("[cyan]💡 Refinement feature coming in next update![/cyan]")
    
    except Exception as e:
        ui.console.print(f"[red]Error: {str(e)}[/red]")
        ui.console.print("[yellow]Please try again or check your inputs.[/yellow]")

if __name__ == "__main__":
    main()