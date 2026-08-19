# AWS Data Engineering Platform

An end-to-end data engineering project demonstrating modern data ingestion,
data quality, cloud storage, transformation, orchestration, testing and
analytics using Python, AWS S3 and Dagster.

## Project Status

- In development

The core data pipeline, AWS S3 data lake and Dagster orchestration are
currently implemented.

## Architecture

```text
                         ┌──────────────────┐
                         │   Source Orders  │
                         │     CSV File     │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     Dagster      │
                         │   Orchestration  │
                         └────────┬─────────┘
                                  │
                                  ▼
                    ┌─────────────────────────┐
                    │        AWS S3            │
                    │                         │
                    │       Bronze            │
                    │   Raw orders data       │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     Data Validation     │
                    │                         │
                    │ • Duplicate IDs         │
                    │ • Missing customers     │
                    │ • Invalid dates         │
                    │ • Invalid quantities    │
                    │ • Invalid prices        │
                    └────────────┬────────────┘
                                 │
                      ┌──────────┴──────────┐
                      │                     │
                      ▼                     ▼
             ┌────────────────┐    ┌─────────────────┐
             │     Silver     │    │   Quarantine    │
             │  Valid orders  │    │ Invalid records │
             └───────┬────────┘    └─────────────────┘
                     │
                     ▼
             ┌────────────────────┐
             │       Gold         │
             │ Daily Product Sales│
             └────────────────────┘