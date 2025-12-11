# Setup and configure AlloyDB
## Before you begin

From the Google Cloud Console, click the Cloud Shell icon on the top right toolbar:

1. Set your PROJECT_ID environment variable:

```
export PROJECT_ID=<your-project-id>
```

2. Set your gloud project:

```
gcloud config set project $PROJECT_ID
```

3. Enable the necessary APIs:

```
gcloud services enable alloydb.googleapis.com \
                       compute.googleapis.com \
                       cloudresourcemanager.googleapis.com \
                       servicenetworking.googleapis.com \
                       vpcaccess.googleapis.com \
                       aiplatform.googleapis.com
```

## Enable private services access

In this step, we will enable Private Services Access so that AlloyDB is able to connect to your VPC. You should only need to do this once per VPC (per project).

1. Set environment variables:
```
export VPC_NAME=my-vpc
export SUBNET_NAME=my-subnet
export RANGE_NAME=my-allocated-range-default
export DESCRIPTION="peering range for alloydb-service"
```
2. Create VPC Network and subnet:
```
gcloud compute networks create $VPC_NAME \
    --project=$PROJECT_ID \
    --subnet-mode=custom \
    --mtu=1460 \
    --bgp-routing-mode=regional
```
3. Create a subnet:
```
gcloud compute networks subnets create $SUBNET_NAME \
    --project=$PROJECT_ID \
    --range=10.0.0.0/24 \
    --stack-type=IPV4_ONLY \
    --network=$VPC_NAME \
    --region=us-central1
```
4. Create a Firewall rule to allow SSH to the Network:
```
gcloud compute firewall-rules create allow-ssh-$VPC_NAME --network $VPC_NAME --allow tcp:22,tcp:3389,icmp --source-ranges 0.0.0.0/0
```

5. Create an allocated IP address range:
```
gcloud compute addresses create $RANGE_NAME \
    --global \
    --purpose=VPC_PEERING \
    --prefix-length=16 \
    --description="$DESCRIPTION" \
    --network=$VPC_NAME
```

6. Ensure you have your Application Authentication Default (ADC) available for you project
```
gcloud auth application-default login
```

7. Create a private connection:
```
gcloud services vpc-peerings connect \
    --service=servicenetworking.googleapis.com \
    --ranges="$RANGE_NAME" \
    --network=$VPC_NAME
```

## Create a AlloyDB cluster and instance

1. Set environment variables. For security reasons, use a different password for $DB_PASS and note it for future use:
```
export CLUSTER=myalloydbcluster
export DB_PASS=myalloydbpass
export INSTANCE=myalloydbpri
export REGION=us-central1
```

2. Create an AlloyDB cluster:
```
gcloud alloydb clusters create $CLUSTER \
    --password=$DB_PASS\
    --network=$VPC_NAME \
    --region=$REGION \
    --project=$PROJECT_ID
```

3. Create a primary instance:
```
gcloud alloydb instances create $INSTANCE \
    --instance-type=PRIMARY \
    --cpu-count=4 \
    --availability-type=ZONAL \
    --region=$REGION \
    --cluster=$CLUSTER \
    --project=$PROJECT_ID \
    --ssl-mode=ALLOW_UNENCRYPTED_AND_ENCRYPTED
```

4- Enable the database flag password.complexity_enforce=on. It is a requirement to use Public IP
```
gcloud beta alloydb instances update $INSTANCE \
   --database-flags password.enforce_complexity=on \
   --region=$REGION  \
   --cluster=$CLUSTER \
   --project=$PROJECT_ID \
   --update-mode=FORCE_APPLY
```
**Note**: The operation takes around 3 minutes to complete

5. Enable Public IP for the AlloyDB Instance
```
gcloud alloydb instances update $INSTANCE \
    --cluster=$CLUSTER  \
    --region=$REGION  \
    --assign-inbound-public-ip=ASSIGN_IPV4
```
**Note**: The operation takes around 3 minutes to complete

## Set up connection to AlloyDB

To enable psql to connect to your private AlloyDB instance from Cloud Shell, you'll use the AlloyDB Auth Proxy. This utility securely tunnels your connection to the database. (Refer to [AlloyDB Auth Proxy](https://docs.cloud.google.com/alloydb/docs/auth-proxy/connect#install))

1. Install AlloyDB Auth Proxy using the following command:

```
wget https://storage.googleapis.com/alloydb-auth-proxy/v1.13.8/alloydb-auth-proxy.linux.amd64 -O alloydb-auth-proxy
```

2. Make it executable:

```
chmod +x alloydb-auth-proxy
```

3. Run this command in your first Cloud Shell terminal window. The proxy will run in the background and forward connections.

```
nohup ./alloydb-auth-proxy "projects/$PROJECT_ID/locations/us-central1/clusters/$CLUSTER/instances/$INSTANCE" --public-ip &
```

4. Connect to the AlloyDB Instance using psql:

```
psql -h 127.0.0.1 -U postgres
```

5. Create a new database nl2sqldb

```
create database nl2sqldb;
```

## Setup the integration between AlloyDB and Vertex AI

1. Get the Project Number associated with the Project ID
```
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
```

2. Grant Vertex AI permission to the AlloyDB Service Agent
```
gcloud projects add-iam-policy-binding $PROJECT_ID \
--member="serviceAccount:service-$PROJECT_NUMBER@gcp-sa-alloydb.iam.gserviceaccount.com" \
--role="roles/aiplatform.user"
```
**Note**: The permission might need until 1 minute to get applied

## Initialize your data in AlloyDB

1. Go to agent-adk-alloydb-nl2sql/source/setup and edit the db_config_params with your connection string
```
host=127.0.0.1
database=nl2sqldb
user=postgres
password=myalloydbpass
```

2. Load the data to AlloyDB
```
cd agent-adk-alloydb-nl2sql/source/setup
source load_data.sh
```
**Note**: Validate that AlloyDB Auth Proxy is running in a separate window

Output:
```
Database schema created successfully
PostgreSQL connection closed
Data loaded successfully from products.csv into products table
Data loaded successfully from customers.csv into customers table
Data loaded successfully from sales.csv into sales table
PostgreSQL connection closed
```

3. Connect to the AlloyDB Instance to validate the data
```
psql -h 127.0.0.1 -U postgres -d nl2sqldb
select count(*) from products;
 count 
-------
   50
```

