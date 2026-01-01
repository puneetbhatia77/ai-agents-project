# AzureCrew Crew

Welcome to the AzureCrew Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/azure_crew/config/agents.yaml` to define your agents
- Modify `src/azure_crew/config/tasks.yaml` to define your tasks
- Modify `src/azure_crew/crew.py` to add your own logic, tools and specific args
- Modify `src/azure_crew/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the azure-crew Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The azure-crew Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the AzureCrew Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.

## Azure Setup (required)

Follow these steps to connect the crew to Azure OpenAI (recommended production setup):

1. Create an Azure OpenAI resource in the Azure portal and deploy a model (example deployment name used in this repo: `crew-ai-deployment`).

2. Note your resource endpoint (example): `https://azure-openai-skillup1.openai.azure.com/` and your API key.

3. Use the supported API version for this project: `2024-10-01-preview`.

4. Add the following variables to the repository `.env` file (root of `azure_crew`):

```
AZURE_API_BASE=https://<your-resource-name>.openai.azure.com/
AZURE_API_KEY=<your-azure-openai-key>
AZURE_API_VERSION=2024-10-01-preview
```

Replace `<your-resource-name>` and `<your-azure-openai-key>` with your actual values. Do NOT commit the `.env` file to source control.

5. Ensure `src/azure_crew/crew.py` initializes an LLM from environment variables and passes it to agents. Example (already present in this repo):

```
from crewai import LLM
import os

self.azure_llm = LLM(
	model="azure/crew-ai-deployment",
	api_key=os.getenv("AZURE_API_KEY"),
	base_url=os.getenv("AZURE_API_BASE"),
	api_version=os.getenv("AZURE_API_VERSION", "2024-10-01-preview")
)

# and pass to agents:
Agent(config=..., llm=self.azure_llm, verbose=True)
```

6. Install dependencies and run the crew from the `azure_crew` folder root:

```powershell
# from project root (azure_crew)
crewai install
crewai run
```

7. Troubleshooting:
- If you receive authentication errors (401), confirm `AZURE_API_KEY` and `AZURE_API_BASE` are correct and that the API version matches `2024-10-01-preview`.
- If the agents fail to run or show an unconfigured LLM, open `src/azure_crew/crew.py` and make sure each `Agent(...)` call includes `llm=self.azure_llm`.

