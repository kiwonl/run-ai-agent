# AI Agent Infrastructure Setup

## Overview

This project provides a comprehensive setup for deploying a sophisticated AI agent on Google Cloud. The agent is designed to be a "Zoo Tour Guide," capable of answering questions about animals in a fictional zoo. It leverages a custom-built MCP (Multi-turn Conversation Platform) server for zoo-specific data and Wikipedia for general knowledge. The entire infrastructure is managed using Terraform, and the agent is deployed on Cloud Run.

## Features

- **AI Agent:** A conversational AI agent built with the Google ADK (Agent Development Kit).
- **MCP Server:** A custom MCP server built with FastAPI that provides data about the zoo's animals. This server is deployed on Cloud Run and is only accessible from within the project's VPC.
- **Terraform Automation:** The entire Google Cloud infrastructure is provisioned using Terraform.
- **Cloud Run Deployment:** Both the AI agent and the MCP server are deployed as serverless applications on Cloud Run.
- **Secure Communication:** The agent communicates securely with the MCP server using ID tokens.

## Architecture

The project consists of three main components:

1.  **Zoo MCP Server:** A Python server that exposes a set of tools for querying information about the zoo's animals. This server is deployed on Cloud Run and is only accessible from within the project's VPC.
2.  **AI Agent:** A Python application that uses the Google ADK to create a multi-agent system. The agent can reason about when to use the MCP server for zoo-specific data and when to use Wikipedia for general knowledge. The agent is also deployed on Cloud Run.
3.  **Terraform:** A set of Terraform scripts that define and provision all the necessary Google Cloud resources, including the VPC, subnets, service accounts, and API enablement.

## Getting Started

### Prerequisites

- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
- [Python 3.10+](https://www.python.org/downloads/)

### Installation

1.  **Set up environment variables:**

    ```bash
    export PROJECT_ID=<your-gcp-project-id>
    export REGION=us-central1
    ```

2.  **Update `terraform.tfvars`:**

    ```bash
    cd terraform
    sed -i \
    -e "s/your-gcp-project-id/$PROJECT_ID/"
    -e "s/your-region/$REGION/"
    terraform.tfvars
    ```

3.  **Initialize and apply Terraform:**

    ```bash
    terraform init
    terraform plan
    terraform apply
    ```

    Take note of the outputs, especially the `service_account_email`.

### Deployment

1.  **Deploy the Zoo MCP Server:**

    ```bash
    cd ..
    gcloud run deploy zoo-mcp-server \
        --source ./zoo-mcp-server/ \
        --region ${REGION} \
        --service-account <your-service-account-email> \
        --no-allow-unauthenticated \
        --network=<your-vpc-name> \
        --subnet=<your-subnet-name> \
        --vpc-egress=all-traffic
    ```

2. Update .env file
    ``` bash
    echo -e "\nMCP_SERVER_URL=https://zoo-mcp-server-${PROJECT_NUMBER}.${REGION}.run.app/mcp/" >> .env
    ```

2.  **Install the Google ADK:**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install google-adk
    ```

3.  **Deploy the AI Agent:**

    ```bash
    adk deploy cloud_run \
      --project=${PROJECT_ID} \
      --region=${REGION} \
      --service_name=zoo-tour-guide \
      --with_ui \
      .

    gcloud run services update zoo-tour-guide \
      --region=${REGION} \
      --service-account <your-service-account-email> \
      --network=<your-vpc-name> \
      --subnet=<your-subnet-name>  \
      --vpc-egress=all-traffic
    ```

## Usage

Once the AI agent is deployed, you can interact with it through the UI provided by the `adk deploy` command. The URL for the UI will be printed in the console after the deployment is complete.

## References

- [MCP Server Codelab](https://codelabs.developers.google.com/codelabs/cloud-run/how-to-deploy-a-secure-mcp-server-on-cloud-run?hl=ko#6)
- [AI Agent Codelab](https://codelabs.developers.google.com/codelabs/cloud-run/use-mcp-server-on-cloud-run-with-an-adk-agent?hl=ko#0)