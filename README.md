# AlloyDB NL with Agent Development Kit (ADK) and MCP Toolbox

This repository showcases a demo of Natural Language (NL) interaction with an AlloyDB database using an Agent built with the Agent Development Kit (ADK). The agent leverages the MCP Toolbox to connect to the database and facilitate data exploration for an imaginary e-commerce scenario.

## Project Overview

The goal of this project is to demonstrate how to:

*   **Develop an intelligent agent** using ADK that can understand natural language queries.
*   **Connect the agent to an AlloyDB database** using the MCP Toolbox.
*   **Enable natural language interaction** with your database, allowing users to query and explore data without writing SQL.
*   **Showcase a practical application** in an e-commerce context, where users can ask questions about products, orders, customers, etc.

## Architecture

The solution comprises the following key components:

*   **Agent Development Kit (ADK):** Used to define the agent's capabilities, tools, and interaction flows.
*   **AlloyDB:** The high-performance, fully managed PostgreSQL-compatible database storing the e-commerce data.
*   **MCP Toolbox:** A set of utilities and connectors that bridge the ADK agent with the AlloyDB instance. This component handles SQL generation and execution based on the agent's understanding of natural language queries.
*   **E-commerce Database Schema:** An imaginary database schema representing typical e-commerce entities like products, orders, customers, etc.

```mermaid
graph TD
    User[User] -->|Natural Language Query| ADK_Agent[ADK Agent]
    ADK_Agent -->|Tool Call (e.g., "query_database")| MCP_Toolbox[MCP Toolbox]
    MCP_Toolbox -->|SQL Query| AlloyDB[AlloyDB Database]
    AlloyDB -->|SQL Results| MCP_Toolbox
    MCP_Toolbox -->|Formatted Data| ADK_Agent
    ADK_Agent -->|Natural Language Response| User
## Deploying

### Before you begin

Clone this repo:

```
git clone https://github.com/GoogleCloudPlatform/agent-adk-alloydb-nl2sql.git
```

### Setting Up your Database

Follow these instructions to set up and configure the database:

[Setting up your Database](docs/alloydb.md)

### Configure Natural Language to SQL

Follow these instructions to configure NL in AlloyDB

[Configure NL in AlloyDB](docs/alloydbnl.md)

### Deploying MCP ToolBox

### Deploy your Agent

### Run your Agent

### Clean Up your resources