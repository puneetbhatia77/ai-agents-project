# StockPicker Crew

Welcome to the StockPicker Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

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
## Azure Setup (Azure OpenAI)

If you want to run this project against Azure OpenAI, follow these steps:

- **Create or use an existing Azure OpenAI resource:** create a deployment (for example name it `crew-ai-deployment`) in the Azure portal and note the deployment name and resource endpoint.
- **Set environment variables:** add the following to the project's `.env` file (or export them in your shell):

	- `AZURE_API_BASE`: your resource endpoint, for example `https://<your-resource-name>.openai.azure.com`
	- `AZURE_API_VERSION`: `2024-10-01-preview` (default used in this project)
	- `AZURE_API_KEY`: your Azure OpenAI key

	Example `.env`:

	```env
	AZURE_API_BASE=https://azure-openai-skillup2.openai.azure.com
	AZURE_API_VERSION=2024-10-01-preview
	AZURE_API_KEY=<YOUR_KEY>
	```

- **Ensure a matching deployment name:** the project currently configures the LLM with `model="azure/crew-ai-deployment"` (see `src/financial_researcher/crew.py`). That means your Azure deployment name should match the suffix (for example `crew-ai-deployment`). If your deployment has a different name, either rename your deployment or update `crew.py` to use the correct model/deployment name.

- **Install and run:** create/activate your virtual environment, install the project editable and dependencies, then run the crew:

	```bash
	python -m venv .venv
	.venv\Scripts\activate    # Windows
	pip install -e .
	crewai run
	```

Troubleshooting:

- If you see a 401 error, check the `AZURE_API_KEY` and `AZURE_API_BASE` values.
- If you see a 404 `DeploymentNotFound`, verify the deployment name in the Azure portal and ensure it matches the `model`/deployment configured in `crew.py` or set the correct name in `.env` and code.

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/stock_picker/config/agents.yaml` to define your agents
- Modify `src/stock_picker/config/tasks.yaml` to define your tasks
- Modify `src/stock_picker/crew.py` to add your own logic, tools and specific args
- Modify `src/stock_picker/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the stock_picker Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The stock_picker Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the StockPicker Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
