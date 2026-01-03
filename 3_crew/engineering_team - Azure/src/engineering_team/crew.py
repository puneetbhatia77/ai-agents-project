from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os


@CrewBase
class EngineeringTeam():
    """EngineeringTeam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

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
    def engineering_lead(self) -> Agent:
        return Agent(
            config=self.agents_config['engineering_lead'],
            llm=self.azure_llm,
            verbose=True,
        )

    @agent
    def backend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer'],
            llm=self.azure_llm,
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=500, 
            max_retry_limit=3 
        )
    
    @agent
    def frontend_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer'],
            llm=self.azure_llm,
            verbose=True,
        )
    
    @agent
    def test_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['test_engineer'],
            llm=self.azure_llm,
            verbose=True,
            allow_code_execution=True,
            code_execution_mode="safe",  # Uses Docker for safety
            max_execution_time=500, 
            max_retry_limit=3 
        )

    @task
    def design_task(self) -> Task:
        return Task(
            config=self.tasks_config['design_task']
        )

    @task
    def code_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_task'],
        )

    @task
    def frontend_task(self) -> Task:
        return Task(
            config=self.tasks_config['frontend_task'],
        )

    @task
    def test_task(self) -> Task:
        return Task(
            config=self.tasks_config['test_task'],
        )   

    @crew
    def crew(self) -> Crew:
        """Creates the research crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )