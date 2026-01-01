from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from typing import List
from .tools.push_tool import PushNotificationTool
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
import os

# Map Azure env vars to OpenAI-style env vars at import time so
# downstream embedding libraries (which check `OPENAI_API_KEY`) can
# pick up Azure credentials automatically when present.
if os.getenv("AZURE_API_KEY") and not os.getenv("OPENAI_API_KEY"):
    os.environ.setdefault("OPENAI_API_TYPE", "azure")
    os.environ.setdefault("OPENAI_API_BASE", os.getenv("AZURE_API_BASE", ""))
    os.environ.setdefault("OPENAI_API_KEY", os.getenv("AZURE_API_KEY", ""))
    os.environ.setdefault("OPENAI_API_VERSION", os.getenv("AZURE_API_VERSION", "2024-10-01-preview"))

class TrendingCompany(BaseModel):
    """ A company that is in the news and attracting attention """
    name: str = Field(description="Company name")
    ticker: str = Field(description="Stock ticker symbol")
    reason: str = Field(description="Reason this company is trending in the news")

class TrendingCompanyList(BaseModel):
    """ List of multiple trending companies that are in the news """
    companies: List[TrendingCompany] = Field(description="List of companies trending in the news")

class TrendingCompanyResearch(BaseModel):
    """ Detailed research on a company """
    name: str = Field(description="Company name")
    market_position: str = Field(description="Current market position and competitive analysis")
    future_outlook: str = Field(description="Future outlook and growth prospects")
    investment_potential: str = Field(description="Investment potential and suitability for investment")

class TrendingCompanyResearchList(BaseModel):
    """ A list of detailed research on all the companies """
    research_list: List[TrendingCompanyResearch] = Field(description="Comprehensive research on all trending companies")


@CrewBase
class StockPicker():
    """StockPicker crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        # Initialize Azure OpenAI LLM when the class is instantiated
        # Read values from environment variables set in main.py
        # Diagnostic output to help debug 404 Resource not found errors
        deployment = os.getenv("AZURE_LLM_DEPLOYMENT", "crew-ai-deployment")
        print("[DEBUG] AZURE_API_BASE=", os.getenv("AZURE_API_BASE"))
        print("[DEBUG] AZURE_API_VERSION=", os.getenv("AZURE_API_VERSION"))
        print("[DEBUG] AZURE_LLM_DEPLOYMENT=", deployment)
        masked_key = None
        if os.getenv("AZURE_API_KEY"):
            masked_key = os.getenv("AZURE_API_KEY")[:6] + "..." + os.getenv("AZURE_API_KEY")[-6:]
        print("[DEBUG] AZURE_API_KEY=", masked_key)

        # Use plain deployment name (no provider prefix) which Azure/OpenAI SDKs expect
        self.azure_llm = LLM(
            model=deployment,
            api_key=os.getenv("AZURE_API_KEY"),
            base_url=os.getenv("AZURE_API_BASE"),
            api_version=os.getenv("AZURE_API_VERSION", "2024-10-01-preview")
        )
        super().__init__()

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(config=self.agents_config['trending_company_finder'],
                     llm=self.azure_llm,
                     tools=[SerperDevTool()], memory=True)
    
    @agent
    def financial_researcher(self) -> Agent:
        return Agent(config=self.agents_config['financial_researcher'], 
                     llm=self.azure_llm,
                     tools=[SerperDevTool()])

    @agent
    def stock_picker(self) -> Agent:
        return Agent(config=self.agents_config['stock_picker'], 
                    llm=self.azure_llm,
                     tools=[PushNotificationTool()], memory=True)
    
    @task
    def find_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['find_trending_companies'],
            output_pydantic=TrendingCompanyList,
        )

    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['research_trending_companies'],
            output_pydantic=TrendingCompanyResearchList,
        )

    @task
    def pick_best_company(self) -> Task:
        return Task(
            config=self.tasks_config['pick_best_company'],
        )
    



    @crew
    def crew(self) -> Crew:
        """Creates the StockPicker crew"""
        # If Azure credentials are provided, map them to the environment
        # variables expected by downstream embedding libraries (OpenAI-style).
        # This lets the Chroma/embedding configurator use Azure embeddings
        # without requiring the user to also set `OPENAI_API_KEY`.
        if os.getenv("AZURE_API_KEY") and not os.getenv("OPENAI_API_KEY"):
            os.environ.setdefault("OPENAI_API_TYPE", "azure")
            os.environ.setdefault("OPENAI_API_BASE", os.getenv("AZURE_API_BASE", ""))
            os.environ.setdefault("OPENAI_API_KEY", os.getenv("AZURE_API_KEY", ""))
            os.environ.setdefault("OPENAI_API_VERSION", os.getenv("AZURE_API_VERSION", "2024-10-01-preview"))

        manager = Agent(
            config=self.agents_config['manager'],
            llm=self.azure_llm,
            allow_delegation=True
        )
            
        # Build explicit Azure embedder config so RAGStorage does not
        # depend on environment variable detection order (OPENAI_API_KEY).
        azure_embed_config = {
            "provider": "azure",
            "config": {
                "model": os.getenv("AZURE_EMBED_MODEL", "text-embedding-3-small"),
                "api_key": os.getenv("AZURE_API_KEY"),
                "api_base": os.getenv("AZURE_API_BASE"),
                "api_version": os.getenv("AZURE_API_VERSION", "2024-10-01-preview"),
            }
        }

        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
            memory=True,
            # Long-term memory for persistent storage across sessions
            long_term_memory = LongTermMemory(
                storage=LTMSQLiteStorage(
                    db_path="./memory/long_term_memory_storage.db"
                )
            ),
            # Short-term memory for current context using RAG
            short_term_memory = ShortTermMemory(
                storage = RAGStorage(
                        embedder_config=azure_embed_config,
                        type="short_term",
                        path="./memory/"
                    )
                ),            # Entity memory for tracking key information about entities
            entity_memory = EntityMemory(
                storage=RAGStorage(
                    embedder_config=azure_embed_config,
                    type="short_term",
                    path="./memory/"
                )
            ),
        )        