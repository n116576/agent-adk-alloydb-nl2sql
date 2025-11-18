from google.adk.agents.llm_agent import Agent
from toolbox_core import ToolboxSyncClient

toolbox = ToolboxSyncClient("http://127.0.0.1:5000")

# Load a specific set of tools
tools = toolbox.load_toolset('my-toolset')

root_agent = Agent(
    model='gemini-2.5-flash',
    name='ecommerce_data_agent',
    description='An expert assistant for retrieving and analyzing data from the e-commerce database (Products, Customers, and Sales tables)',
    instruction='Your sole purpose is to serve as an intermediary between the user and the database tool. For every user query that requires data retrieval or analysis (e.g., pricing, counting, summarizing, or filtering), you MUST use the ecommerce_data_query tool. Do not generate or invent data. If a query is successfully executed, summarize the results clearly and concisely to the user.',
    tools=tools
)