# src/financial_researcher/crew.py
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
import os

@CrewBase
class ResearchCrew():
    """Research crew for comprehensive topic analysis and reporting"""

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
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            llm=self.azure_llm,
            verbose=True,
            tools=[SerperDevTool()]
        )

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst'],
            llm=self.azure_llm,
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task']
        )

    @task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['analysis_task']
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