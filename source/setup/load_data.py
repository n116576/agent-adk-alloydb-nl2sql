import psycopg2
from psycopg2 import Error

def load_db_config():
    """Load database configuration from db_config.params file"""
    db_params = {}
    try:
        with open('db_config.params', 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=')
                    db_params[key.strip()] = value.strip()
        return db_params
    except FileNotFoundError:
        print("Error: db_config.params file not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading config file: {e}")
        sys.exit(1)

def create_database_schema(db_params):
    """
    Creates the database schema for the products, customers and sales
    
    Args:
        db_params (dict): Database connection parameters containing:
            - host
            - database
            - user
            - password
            - port
    """
    try:
        # Establish connection
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Drop existing tables
        cursor.execute("DROP TABLE IF EXISTS customers CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS products CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS sales CASCADE;") 

        # Create tables
        create_tables_query = """
        -- products Table
        CREATE TABLE products (
            product_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            category VARCHAR(50),      -- e.g., 'Electronics', 'Apparel', 'Books'
            price NUMERIC(10, 2) NOT NULL,
            stock_quantity INTEGER,
            avg_review_score NUMERIC(2, 1)
        );

        CREATE TABLE customers (
            customer_id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            city VARCHAR(50),
            join_date DATE
        );

        CREATE TABLE sales (
            sale_id SERIAL PRIMARY KEY,
            product_id INTEGER REFERENCES Products(product_id),
            customer_id INTEGER REFERENCES Customers(customer_id),
            sale_date DATE NOT NULL,
            quantity INTEGER NOT NULL,
            total_sale_amount NUMERIC(10, 2) NOT NULL
        );
        """
        
        # Execute the query
        cursor.execute(create_tables_query)
        print("Database schema created successfully")
        # Commit the changes
        connection.commit()

    except (Exception, Error) as error:
        print(f"Error while creating database schema: {error}")
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection closed")

def load_data_from_csv(db_params):
    """Load data from CSV files into database tables"""
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()
        
        # Define CSV files and corresponding table names in the correct loading order
        csv_files = {
            'products.csv': 'products',  # Load products
            'customers.csv': 'customers',  # Load customers
            'sales.csv': 'sales',  # Load sales
        }

        # Load each CSV file into its table
        for csv_file, table_name in csv_files.items():
            try:
                with open(f'../../data/{csv_file}', 'r') as f:
                    # Skip the header row
                    next(f)
                    # Use copy_expert with CSV format to handle escaped commas
                    copy_sql = f"""
                        COPY {table_name} FROM STDIN WITH 
                        CSV 
                        DELIMITER ',' 
                        NULL '' 
                        QUOTE '"'
                    """
                    cursor.copy_expert(sql=copy_sql, file=f)
                print(f"Data loaded successfully from {csv_file} into {table_name} table")
                connection.commit()
                
            except Exception as e:
                print(f"Error loading {csv_file}: {e}")
                connection.rollback()

    except (Exception, Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}")
    
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection closed")

if __name__ == "__main__":
    db_params = load_db_config()    
    create_database_schema(db_params)
    load_data_from_csv(db_params)