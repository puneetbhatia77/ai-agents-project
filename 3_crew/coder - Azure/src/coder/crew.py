from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os


@CrewBase
class Coder():
    """Coder crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # One click install for Docker Desktop:
    #https://docs.docker.com/desktop/

    def __init__(self):
        # Initialize Azure OpenAI LLM when the class is instantiated
        # Read values from environment variables set in main.py
        self.azure_llm = LLM(
            model="azure/crew-ai-deployment",
            api_key=os.getenv("AZURE_API_KEY"),
            base_url=os.getenv("AZURE_API_BASE"),
            api_version=os.getenv("AZURE_API_VERSION", "2024-10-01-preview")
        )
        super().__init__()

    @agent
    def coder(self) -> Agent:
        return Agent(
            config=self.agents_config['coder'],
            verbose=True,
            llm=self.azure_llm,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=30, 
            max_retry_limit=3 
    )


    @task
    def coding_task(self) -> Task:
        return Task(
            config=self.tasks_config['coding_task'],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the Coder crew"""


        return Crew(
            agents=self.agents, 
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
