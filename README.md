# AWS Data Engineering Platform

An end-to-end data engineering platform demonstrating modern data engineering practices using Python, AWS, data quality validation, orchestration, AI/LLMs, testing, CI/CD, and infrastructure as code.

## Project Status

🚧 In development

The core data pipeline, orchestration, automated data quality checks, AI analysis, and CI/CD pipeline are currently implemented. Infrastructure as code and further cloud integration are being developed.

## Architecture

```text
                    Source Orders
                         │
                         ▼
                 ┌───────────────┐
                 │    Dagster    │
                 │ Orchestration │
                 └───────┬───────┘
                         │
                         ▼
                ┌─────────────────┐
                │  Bronze / S3    │
                │   Raw Orders    │
                └────────┬────────┘
                         │
                         ▼
                ┌─────────────────┐
                │ Data Validation │
                │  + Quality      │
                │     Checks      │
                └──────┬─────┬────┘
                       │     │
                 Valid │     │ Invalid
                       ▼     ▼
              ┌──────────┐  ┌─────────────┐
              │ Silver   │  │ Quarantine  │
              │   / S3   │  │    / S3     │
              └────┬─────┘  └──────┬──────┘
                   │               │
                   ▼               ▼
              ┌──────────┐   ┌─────────────┐
              │   Gold   │   │   Bedrock   │
              │   / S3   │   │ AI Analysis │
              └──────────┘   └──────┬──────┘
                                    │
                                    ▼
                             Quality Report
```

## Technologies

### Data Engineering

* Python 3.12
* Pandas
* AWS S3
* Data validation and transformation
* Bronze / Silver / Gold architecture

### Orchestration

* Dagster
* Dagster assets
* Dagster asset checks
* Scheduled pipeline execution

### AI

* Amazon Bedrock
* Amazon Nova Lite
* AI-assisted data quality analysis
* Automated quality recommendations

### Testing & CI/CD

* Pytest
* GitHub Actions
* Automated test execution on push and pull request

### Infrastructure

* Terraform
* AWS IAM
* AWS S3

## Pipeline

The pipeline processes order data through three primary data layers.

### Bronze

Raw source data is uploaded to Amazon S3 using date-based partitioning:

```text
bronze/orders/
└── ingestion_date=YYYY-MM-DD/
    └── orders.csv
```

### Silver

Orders are validated and separated into:

```text
silver/orders/orders_valid.csv
quarantine/orders/orders_invalid.csv
```

Validation currently checks for:

* Duplicate order IDs
* Missing customer IDs
* Invalid quantities
* Invalid order dates
* Missing unit prices

### Gold

Validated orders are transformed into an analytical sales dataset:

```text
gold/sales/daily_product_sales.csv
```

The dataset contains:

* Order date
* Product ID
* Total orders
* Total quantity
* Total sales

## Data Quality

Dagster asset checks are used to verify the Silver dataset.

Current checks include:

* No validation errors
* Unique order IDs
* Positive quantities
* Valid unit prices

Invalid source records are quarantined rather than silently discarded.

## AI Data Quality Analysis

Amazon Bedrock is integrated into the data quality workflow.

The deterministic Python validation layer identifies data-quality problems, while the AI layer provides human-readable analysis and recommendations.

This separation keeps the pipeline deterministic while using AI where it adds value.

Example:

```text
Invalid records
      │
      ▼
Validation rules
      │
      ▼
Quality issues
      │
      ▼
Amazon Bedrock
      │
      ▼
Recommendations
      │
      ▼
Data quality report
```

## Testing

The project uses Pytest for automated testing.

Tests currently cover:

* Bronze ingestion
* Data validation
* Silver transformations
* Gold transformations
* AI quality analysis
* AI quality reporting

GitHub Actions automatically runs the test suite on pushes and pull requests.

## Infrastructure as Code

Terraform is being introduced to manage the AWS infrastructure used by the project.

The existing S3 data lake will be brought under Terraform management rather than recreated.

Planned infrastructure includes:

```text
terraform/
├── main.tf
├── variables.tf
├── outputs.tf
└── README.md
```

## Project Structure

```text
aws-data-engineering-platform/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── config/
│   └── config.yaml
│
├── data/
│   └── sample/
│
├── src/
│   ├── ai/
│   │   ├── bedrock_client.py
│   │   ├── quality_analyzer.py
│   │   ├── quality_report.py
│   │   └── ...
│   │
│   ├── dagster_project/
│   │   └── definitions.py
│   │
│   ├── gold/
│   │   └── build_gold.py
│   │
│   ├── ingestion/
│   │   └── ingest_orders.py
│   │
│   ├── pipeline/
│   │   └── run_pipeline.py
│   │
│   ├── utils/
│   │   ├── config.py
│   │   ├── logging_config.py
│   │   └── s3.py
│   │
│   └── validation/
│       ├── order_validation.py
│       └── run_validation.py
│
├── tests/
├── requirements.txt
└── README.md
```

## Key Engineering Practices Demonstrated

This project is designed to demonstrate practical data engineering skills including:

* Python application development
* ETL/ELT pipeline design
* Cloud object storage
* Data lake architecture
* Data quality engineering
* Data validation and quarantine
* Pipeline orchestration
* Automated testing
* CI/CD
* AI/LLM integration
* Infrastructure as code
* AWS IAM and security
* Reproducible infrastructure

## Future Improvements

Planned improvements include:

* Terraform-managed AWS infrastructure
* Improved IAM policies and least-privilege access
* Additional data sources
* More comprehensive data quality checks
* Production-style configuration management
* Monitoring and alerting
* Data visualisation
* Additional AWS services
* Improved AI-generated data quality reporting

## Project Goals

The goal of this project is to demonstrate the design and implementation of a realistic cloud-based data engineering platform while applying software engineering principles such as testing, automation, orchestration, infrastructure as code, and maintainable Python development.
