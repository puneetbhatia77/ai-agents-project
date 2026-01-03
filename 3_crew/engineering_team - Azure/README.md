# EngineeringTeam Crew

Welcome to the EngineeringTeam Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

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

**Add your Azure OpenAI credentials into the `.env` file**

Create a `.env` file in the root directory with the following variables:
```bash
AZURE_API_KEY=your_azure_api_key_here
AZURE_API_BASE=https://your-resource-name.openai.azure.com
AZURE_API_VERSION=2024-10-01-preview
```

- Modify `src/engineering_team/config/agents.yaml` to define your agents
- Modify `src/engineering_team/config/tasks.yaml` to define your tasks
- Modify `src/engineering_team/crew.py` to add your own logic, tools and specific args
- Modify `src/engineering_team/main.py` to add custom inputs for your agents and tasks

### Configuration Notes

This project uses **Azure OpenAI** (model: `azure/crew-ai-deployment`) instead of standard OpenAI.

**Docker Note**: Code execution is disabled for backend_engineer and test_engineer agents to avoid Docker dependency. This is configured in `src/engineering_team/crew.py` with `allow_code_execution=False`.

**Gradio UI Standards**: The frontend_engineer agent is configured to use modern Gradio APIs:
- ✅ Uses: `gr.Blocks()`, `gr.Textbox()`, `gr.Number()`, `gr.Button()`, `gr.Tab()`
- ❌ Avoids: `gr.inputs.*` (removed), `gr.Interface` (deprecated), `.style()` method (removed)
- 📋 Default Layout: 4-tab structure for trading/account apps (Account Operations, Shares Operations, Portfolio Summary, Transaction History)

## Running the Project

### 1. Generate Code with CrewAI

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
crewai run
```

This command initializes the engineering_team Crew, assembling the agents and assigning them tasks as defined in your configuration. The agents will generate:
- `output/accounts.py` - Backend class with account management logic
- `output/app.py` - Gradio web UI demonstrating the backend
- `output/test_accounts.py` - Unit tests for the backend
- `output/accounts.py_design.md` - Design documentation

### 2. Run the Generated Application

After CrewAI successfully generates the code, navigate to the output directory and run the Gradio application:

```bash
cd output
uv run --with gradio app.py
```

Or from the root directory:

```bash
uv run --with gradio output/app.py
```

The Gradio interface will launch at `http://127.0.0.1:7860` with a 4-tab layout:
1. **Account Operations** - Deposit and withdraw funds
2. **Shares Operations** - Buy and sell shares
3. **Portfolio Summary** - View portfolio value and profit/loss
4. **Transaction History** - Review all account transactions

## Understanding Your Crew

The engineering_team Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the EngineeringTeam Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
