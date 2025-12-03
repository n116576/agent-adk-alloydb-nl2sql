# Deploy MCP Toolbox for Databases

For this project, we'll deploy MCP Toolbox server to Cloud Run:

1. In your Cloud Shell Terminal, navigate to the toolbox folder located within your cloned project repository

```
cd agent-adk-alloydb-nl2sql/source/toolbox
```

2. Next, verify that the following Google Cloud services are enabled in the project.

```
gcloud services enable run.googleapis.com \
                       cloudbuild.googleapis.com \
                       artifactregistry.googleapis.com \
                       iam.googleapis.com \
                       secretmanager.googleapis.com
```

3. Let's create a separate service account that will be acting as the identity for the Toolbox service that we will be deploying on Google Cloud Run. We are also ensuring that this service account has the correct roles i.e. ability to access Secret Manager and talk to AlloyDB.

```
gcloud iam service-accounts create toolbox-identity

gcloud projects add-iam-policy-binding $PROJECT_ID \
   --member serviceAccount:toolbox-identity@$PROJECT_ID.iam.gserviceaccount.com \
   --role roles/secretmanager.secretAccessor


gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member='serviceAccount:toolbox-identity@'$PROJECT_ID'.iam.gserviceaccount.com' \
    --role='roles/alloydb.client'


gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member='serviceAccount:toolbox-identity@'$PROJECT_ID'.iam.gserviceaccount.com' \
    --role='roles/serviceusage.serviceUsageConsumer'
```

3. Update the section "source" of the "tools.yaml" file with the information of your own environment:

```
  my-alloydb-source:
    kind: alloydb-postgres
    project: mtoscano-alloydbnl
    region: us-central1
    cluster: myalloydbcluster
    instance: myalloydbpri
    database: nl2sqldb
    user: postgres
    password: myalloydbpass
```

4. Create a new secret and upload the existing "tools.yaml" file:

```
gcloud secrets create tools --data-file=tools.yaml
```

5. Use the latest Container Image for the MCP ToolBox

```
export IMAGE=us-central1-docker.pkg.dev/database-toolbox/toolbox/toolbox:latest
```

6. Finally, deploy your Toolbox server to Cloud Run using the following command. This command will containerize your application, configure the service account, inject the secret, and expose it publicly:

```
gcloud run deploy toolbox \
--image $IMAGE \
--service-account toolbox-identity \
--region us-central1 \
--set-secrets "/app/tools.yaml=tools:latest" \
--args="--tools_file=/app/tools.yaml","--address=0.0.0.0","--port=8080" \
--allow-unauthenticated
```

7. On successful deployment, you should see a message similar to the following:

```
Deploying container to Cloud Run service [toolbox] in project [sports-store-agent-ai] region [us-central1]
OK Deploying... Done.
  OK Creating Revision...
  OK Routing traffic...
  OK Setting IAM Policy...
Done.
Service [toolbox] revision [toolbox-00002-dn2] has been deployed and is serving 100 percent of traffic.
Service URL: https://toolbox-[YOUR_PROJECT_NUMBER].us-central1.run.app
```

8. You can now visit the Service URL listed above in the browser. It should display the "Hello World" message.
