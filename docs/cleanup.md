# Clean Up Resources

The fastest way to clean up is to delete the entire Google Cloud project. Follow the steps below if you want to keep the project but delete resources created through this demo.

## Deleting AlloyDB Resources

1. Set environment variables:
```
export CLUSTER=myalloydbcluster
export REGION=us-central1
export RANGE_NAME=my-allocated-range-default
```

2. Delete AlloyDB cluster that contains instances:
```
gcloud alloydb clusters delete $CLUSTER \
    --force \
    --region=$REGION \
    --project=$PROJECT_ID
```

3. Delete an allocated IP address range:
```
gcloud compute addresses delete $RANGE_NAME \
    --global
```

## Deleting MCP ToolBox Cloud Run Service

1. Delete MCP ToolBox Cloud Run service deployed:

    ```bash
    gcloud run services delete toolbox
    ```
