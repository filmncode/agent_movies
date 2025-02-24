from crewai.project import task
from crewai import Task

@task
def query_movie(self, movie_title: str) -> Task:
    """Query information about a movie"""
    return Task(
        description=f"Find information about the movie '{movie_title}' and its score",
        agent=self.movie_query_agent,
        expected_output="Movie details including title, score, and brief description"
    ) 