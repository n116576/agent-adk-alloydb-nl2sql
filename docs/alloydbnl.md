# Configure Natural Language in AlloyDB
## Enable and install the required extension

Set environment variables:

```
export PROJECT_ID=mtoscano-alloydbnl
export CLUSTER=myalloydbcluster
export DB_PASS=myalloydbpass
export INSTANCE=myalloydbpri
export REGION=us-central1
```

Enable the flag alloydb_ai_nl.enabled for the AlloyDB Instance:

```
gcloud beta alloydb instances update $INSTANCE \
   --database-flags alloydb_ai_nl.enabled=on,password.enforce_complexity=on \
   --region=$REGION \
   --cluster=$CLUSTER \
   --project=$PROJECT_ID \
   --update-mode=FORCE_APPLY
```

Install the alloydb_ai_nl extension, which is the AlloyDB AI natural language support API, run the following query:

```
psql -h 127.0.0.1 -U postgres -d nl2sqldb
```

```
CREATE EXTENSION alloydb_ai_nl cascade;
```

## Create a Natural Language configuration

AlloyDB AI natural language uses nl_config to associate applications to certain schemas, query templates, and model endpoints. nl_config is a configuration that associates an application to schema, templates, and other contexts. A large application can also use different configurations for different parts of the application, as long as you specify the right configuration when a question is sent from that part of the application. You can register an entire schema, or you can register specific schema objects, like tables, views, and columns.

Follow these instructions to create and register a schema for NL:

1. Create a natural language configuration

```
SELECT alloydb_ai_nl.g_create_configuration( 'nla_analysis_cfg' );
```

2. Register tables to the nla_analysis_cfg config

```
SELECT alloydb_ai_nl.g_manage_configuration(
    operation => 'register_table_view',
    configuration_id_in => 'nla_analysis_cfg',
    table_views_in=>'{public.products, public.customers, public.sales}'
);
```

## Add general context to SQL

Context includes any kind of information that you can use to answer an end user question., such as the following:
* Schema structure and relationships
* Summaries and descriptions of columns
* Column values and their semantics
* Rules or statements of business logic specific to the application or domain

Use the automated context generation feature of the AlloyDB AI natural language API to produce context from tables and columns, and apply the context as COMMENTS attached to tables, views, and columns.

1. Create a natural language configuration

```
SELECT alloydb_ai_nl.generate_schema_context(
  'nla_analysis_cfg',
  TRUE
);
```

2. Verify the generated context for the table products:

```
SELECT object_context
FROM alloydb_ai_nl.generated_schema_context_view
WHERE schema_object = 'public.products';
```

Output:

```
The `products` table stores information about various products. It includes the `product_id` as the primary key, a unique identifier for each product. The `name` column provides a descriptive name for the product. The `category` column classifies the product into categories such as Electronics, Apparel, Books, Home Goods, Sports & Outdoors, Toys & Games, Health & Beauty, Automotive, Garden, Pets, Music, Furniture and Groceries. The `price` column stores the price of the product as a numeric value. The `stock_quantity` column indicates the number of units currently in stock. Finally, the `avg_review_score` column represents the average review score for the product, providing an indication of customer satisfaction.
```