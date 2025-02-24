from crew import MoviescoreCrew
from crewai import Task

def main():
    # Initialize the crew
    crew_manager = MoviescoreCrew()
    
    # Create tasks for different scenarios
    tasks = [
        Task(
            description="Find information about the movie 'Inception' and its score",
            agent=crew_manager.movie_query_agent,
            expected_output="Movie details including title, score, and brief description"
        ),
        Task(
            description="Find similar movies to 'Inception' with a score of 8.0 or higher",
            agent=crew_manager.movie_query_agent,
            expected_output="List of similar highly-rated movies"
        )
    ]
    
    # Create and run the crew
    crew = crew_manager.create_crew(tasks)
    results = crew.kickoff()
    
    print("Results:")
    print(results)

if __name__ == "__main__":
    main() 