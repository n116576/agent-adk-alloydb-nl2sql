# Natural Language to SQL with AlloyDB

This repository showcases a demo focused on Natural Language (NL) to SQL interaction with an AlloyDB database. An intelligent agent, built with the Agent Development Kit (ADK), leverages MCP Toolbox to automatically translate user questions into SQL queries, enabling effortless data exploration for an imaginary e-commerce scenario.

## Project Overview

The central purpose of this project is to demonstrate and utilize the power of Natural Language to SQL (NL2SQL) conversion. This capability allows anyone to derive insights from complex e-commerce data without possessing SQL expertise.

Key Demonstrations
* **Enabling Conversational Querying**: Allowing users to query and explore data using plain English, not technical SQL syntax.

* **Intelligent Agent Development**: Using the ADK to define an agent that can interpret the semantic meaning of natural language queries.

* **Seamless Database Integration**: Connecting the agent to a high-performance, PostgreSQL-compatible AlloyDB instance.

* **E-commerce Application**: Showcasing a practical context where users can ask complex questions about products, orders, customers, etc.

## Architecture

The solution comprises the following key components:
*   **AlloyDB:** The high-performance, fully managed PostgreSQL-compatible database storing the e-commerce data. It exposes the AlloyDB Natural Language API, which is the specific feature responsible for intelligently generating the correct SQL query from the NL input.
*   **MCP Toolbox:** It uses its native tool alloydb-nl-ai to communicate with AlloyDB, sending the user's NL question and managing the SQL generation and execution process.
*   **Agent Development Kit (ADK):** Defines the conversational interface. It receives the user's Natural Language question and passes it to the NL2SQL engine via the MCP Toolbox.
*   **E-commerce Database Schema:** An imaginary database schema representing typical e-commerce entities like products, orders, customers, etc.

## Deployment guide

Follow these steps to set up and run the NL2SQL agent demo. 

All commands and setup steps are designed to be executed from the Google Cloud Shell Terminal.

### Before you begin

First, launch a Cloud Shell Terminal session and clone the repository:
```
git clone https://github.com/GoogleCloudPlatform/agent-adk-alloydb-nl2sql.git
```

### Setting Up your Database

Set up and configure your AlloyDB instance with the e-commerce schema:

[Setting up your Database](docs/alloydb.md)

### Configure Natural Language to SQL

Configure the Natural Language to SQL features and context within AlloyDB:

[Configure NL in AlloyDB](docs/alloydbnl.md)

### Deploying MCP ToolBox

Follow these instructions to run MCP Toolbox for Database to Cloud Run:

[Deploy MCP Toolbox](docs/toolbox.md)

### Deploy your Agent

Follow these instructions to deploy the agent using ADK:

[Deploy your Agent](docs/agent.md)

### Run your Agent

You're ready to chat! Once deployed, start by asking questions around your E-commerce Data from the adk web interface launched in the previous step:

- What is the current price of the 'Wireless Mouse'?

- Show me all products in the 'Electronics' category that have a review score higher than 4.5.

- What is the total revenue generated from all sales of 'Apparel' since the start of the year?

- Which product category has the lowest average selling price?

- List the names of all customers who purchased a product priced over 50 dollars in the last month.

- Which city had the highest total sales amount in the month of October?

- What are the top 5 most sold products by total quantity in the last quarter?

### Clean Up your resources

Follow the instructions to tear down all deployed resources:

[Clean Up your resources](docs/cleanup.md)
