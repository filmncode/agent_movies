from crew import MoviescoreCrew
from crewai import Task

def main():
    crew_manager = MoviescoreCrew()
    user_phone = "+5492616743384"
    
    # Test marking a movie as watched
    task = Task(
        description=f"I watched Inception and send it to {user_phone}",
        expected_output="Message processed and sent via WhatsApp",
        agent=crew_manager.whatsapp_agent
    )
    
    crew = crew_manager.create_crew([task])
    result = crew.kickoff()
    print("Result:", result)

if __name__ == "__main__":
    main() 