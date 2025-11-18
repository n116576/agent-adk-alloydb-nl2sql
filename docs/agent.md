# Deploy the agent using Agent Development Kit (ADK)

1. Go to agent-adk-alloydb-nl2sql/source/agent

```
cd agent-adk-alloydb-nl2sql/source/agent
```

2. Install the SDK package for ToolBox

```
pip install toolbox-core
```

3. Install ADK for Python

```
pip install google-adk
```

4. Start your new agent project:

```
adk create ecommerce_agent
```

**Note:** You will be asked to set up the model and your credentials. I recommend to use your GCP Project details. If you want to use an API Key, check out [Set Up API Key](https://google.github.io/adk-docs/get-started/python/#set-your-api-key)

5. Replace the agent.py:

```
cp agent-adk-alloydb-nl2sql/data/agent.py agent-adk-alloydb-nl2sql/source/agent/ecommerce_agent/agent.py
```

6. Run your Agent with the web interface provided by ADK

```
adk web --port 8000
```

**Note:** You need to execute this command from agent-adk-alloydb-nl2sql/source/agent/ecommerce_agent