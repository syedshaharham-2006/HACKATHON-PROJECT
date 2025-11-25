# ⌛Real-Time Data Pipeline Architecture

## 🧑‍💻Overview
For the final challenge of my AWS Cloud Data Engineering journey, I designed and implemented an **end-to-end data pipeline**. The goal was to create a scalable, production-ready pipeline that automates the ingestion, processing, and delivery of data from multiple sources.

---

## Prerequisites
Before starting with the architecture, ensure you have the following:

- **AWS Account**: Make sure your AWS account is configured with the necessary permissions to create services like Lambda, S3, Glue, and EventBridge.
- **AWS CLI**: Install and configure the AWS CLI on your local machine for interacting with AWS services from the terminal.
- **IAM Roles**: Ensure IAM roles are properly configured for Lambda, Glue, and EventBridge to interact with other AWS services.
- **API Access**: Obtain API keys for the external data sources:
    - CoinMarketCap Scrape top10 coins for cryptocurrency data.
    - OpenExchangeRates API for currency data.
    - Yahoo Finance yahoo finance python library for stock market data.
- **Snowflake Account**: Set up a Snowflake account for data warehousing.
- **Python 3.x**: Ensure Python 3.x is installed for local development and AWS Lambda functions.
- **AWS Glue and PySpark**: Ensure access to AWS Glue and PySpark for data transformations (refer to AWS Glue documentation for details on setting up PySpark jobs).

---

## 🏗️Architecture Components:
- **Amazon S3**: Used for raw data ingestion. S3 acts as the storage layer where raw data is uploaded before processing.
- **SNS Topic with Filter Policies** → **SQS Queues**: Used to manage and route events for processing. SNS sends notifications to SQS queues based on filter policies, ensuring the right messages are processed.
- **AWS Lambda Functions**: Employed for distributed data processing. Lambda functions are triggered by events from SQS and SNS to process data as it arrives.
- **CoinMarketCap** → **S3**: Automated ingestion of cryptocurrency data into S3. Lambda functions fetch data from the CoinMarketCap API and store it in S3.
- **OpenExchangeRates** → **SQL Server**: Integration for currency data storage. Lambda functions pull currency data from OpenExchangeRates API and store it in SQL Server.
- **Yahoo Finance** → **AWS Glue**: Used for data transformation and loading. Data fetched from Yahoo Finance is transformed into a structured format using AWS Glue.
- **AWS Glue ETL (PySpark)**: Data transformation using PySpark. *(This portion is left empty for implementation details).*
- **Snowflake**: The final data warehouse for analytics. After processing, the data is loaded into Snowflake for analytical purposes.
- **EventBridge**: Scheduled triggers for the pipeline’s tasks. EventBridge manages the execution schedule for Lambda functions and Glue jobs.
- **SQL Server**: Integration for currency data storage. SQL Server is used for storing processed currency data from OpenExchangeRates.

This architecture allowed for automated ingestion from multiple APIs, independent data processing with Lambda, and seamless delivery to **Snowflake**. The system is designed to be scalable and production-ready.

---

Run these commands in EC2 instance to make Lambda layer

# 🛠️AWS Lambda Layer Creation for Python Dependencies

This guide demonstrates how to create an AWS Lambda Layer with Python dependencies 
Run these commands in EC2 instance to make Lambda layer


## Steps to Create the Lambda Layer

### ✅ Step 1: Update EC2 Instance and Install Dependencies
Run the following commands to update your EC2 instance and install the necessary packages:

```bash
sudo yum update -y  
sudo yum install python3 python3-pip zip -y  
```

Verify the Python and Pip versions to ensure they were installed correctly:

```bash
python3 --version  
pip3 --version  
```

### ✅ Step 2: Create Folder Structure for Lambda Layer
Create the directory structure for the Lambda layer:

```bash
mkdir lambda-layer  
cd lambda-layer  
mkdir python  
```

### ✅ Step 3: Install Required Python Libraries
Now, install the required Python libraries (`requests`, `beautifulsoup4`, `lxml`, and `boto3`) into the `python/` directory:

```bash
pip3 install requests -t python/  
pip3 install beautifulsoup4 -t python/  
pip3 install lxml -t python/  
pip3 install boto3 -t python/  
```

### ✅ Step 4: Zip the Layer
Once the dependencies are installed, zip the contents of the `lambda-layer` directory to create the Lambda layer package:

```bash
zip -r9 lambda-layer.zip python  
```

### ✅ Step 5: Configure AWS CLI
Before publishing the layer, configure the AWS CLI with your credentials:

```bash
aws configure  
```

### ✅ Step 6: Publish the Lambda Layer
Publish the Lambda layer to AWS Lambda using the AWS CLI. Run the following command:

```bash
aws lambda publish-layer-version \
  --layer-name web-scraper-layer \
  --description "Layer for requests + BeautifulSoup + lxml + boto3" \
  --zip-file fileb://lambda-layer.zip \
  --compatible-runtimes python3.9 python3.10 python3.11  
```

This will output something like:

```json
"LayerVersionArn": "arn:aws:lambda:us-east-1:ACCOUNT_ID:layer:web-scraper-layer:1"
```

---

# AWS Lambda Layer Creation for OpenExchangerateapi

This guide demonstrates how to create an AWS Lambda Layer that includes the `pymssql` and `requests` Python libraries for use in AWS Lambda functions.

## Steps to Create the Lambda Layer

### ✅ Step 1: Create Folder Structure
First, create the necessary folder structure for the Lambda layer:

```bash
mkdir lambda_layer  
mkdir lambda_layer/python  
```

### ✅ Step 2: Install Dependencies into the Layer
Next, install the required dependencies (`pymssql` and `requests`) into the `lambda_layer/python` directory:

```bash
pip install pymssql -t lambda_layer/python  
pip install requests -t lambda_layer/python  
```

### ✅ Step 3: Zip the Layer
Once the dependencies are installed, zip the contents of the `lambda_layer` directory to create the Lambda layer package:

```bash
cd lambda_layer  
zip -r ../pymssql_layer.zip .  
cd ..  
```
This will create a file named `pymssql_layer.zip`.

### ✅ Step 4: Publish the Layer
Publish the layer to AWS Lambda using the AWS CLI:

```bash
aws lambda publish-layer-version \
  --layer-name pymssql-layer \
  --zip-file fileb://pymssql_layer.zip \
  --compatible-runtimes python3.9 \
  --region us-east-1  
```

This will output something like:

```json
"LayerVersionArn": "arn:aws:lambda:us-east-1:ACCOUNT_ID:layer:pymssql-layer:1"
```

