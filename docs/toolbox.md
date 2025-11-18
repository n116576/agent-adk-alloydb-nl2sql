# Deploy MCP Toolbox for Databases

For this project, we'll set up the MCP Toolbox server locally in our Cloud Shell environment

1. In your Cloud Shell Terminal, navigate to the toolbox folder located within your cloned project repository

```
cd agent-adk-alloydb-nl2sql/source/toolbox
```

2. Download the Toolbox binary and grant it execution permissions

```
# see releases page for other versions
export VERSION=0.20.0

curl -O https://storage.googleapis.com/genai-toolbox/v$VERSION/linux/amd64/toolbox

chmod +x toolbox
```

Note: The version 0.20.0 is specified here. For production environments, always verify and use the latest stable release from the Toolbox releases page.

3. In the same directory, you will find a file named tools.yaml. Open this file and update the placeholders of the section source with your own information

4. Start MCP Toobox with this command:

```
nohup ./toolbox --tools-file "tools.yaml" &
```

5. If you open the server in a web preview mode on the cloud, you should be able to see the Toolbox server up and running with all the tools of our application.

The MCP Toolbox Server runs by default on port 5000. Let us use Cloud Shell to test this out.

Click on Web Preview in Cloud Shell, change port and set the port to 5000. This should bring the output: "Hello World"

