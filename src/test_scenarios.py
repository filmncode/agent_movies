from crew import MoviescoreCrew
from crewai import Task

def main():
    crew_manager = MoviescoreCrew()
    user_phone = "+5492616743384"  # Your WhatsApp number
    
    # Test different scenarios
    scenarios = [
        f"Tell me about The Dark Knight and send it to {user_phone}",
        f"I watched Inception and send it to {user_phone}",
        f"Tell me about The Matrix and send it to {user_phone}",
        f"What's the score of Pulp Fiction and send it to {user_phone}",
        f"I watched The Godfather and send it to {user_phone}"
    ]
    
    tasks = [
        Task(
            description=scenario,
            expected_output="Message processed and sent via WhatsApp",
            agent=crew_manager.whatsapp_agent
        )
        for scenario in scenarios
    ]
    
    # Run all scenarios
    crew = crew_manager.create_crew(tasks)
    results = crew.kickoff()
    print("\nAll scenarios completed!")

if __name__ == "__main__":
    main() 