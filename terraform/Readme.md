# Terraform Deployment

This repository contains the Terraform configurations to deploy various components of the IoT & Cloud Computing project, including:

- **MQTT Broker (Mosquitto)**
- **PostgreSQL Database**
- **Backend API (Spring Boot)**
- **Azure Resource Setup**

The goal of this project is to deploy an IoT system with cloud integration using **Azure** and **Terraform**.

## Prerequisites

1. **Terraform**: Make sure you have **Terraform** installed on your local machine. You can install it from [Terraform's website](https://www.terraform.io/downloads).
2. **Azure CLI**: You need the **Azure CLI** to interact with Azure resources. You can install it from [Azure CLI installation](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).
3. **Azure Subscription**: Make sure you have an active Azure subscription for deploying resources.

## How to Use

### 1. **Clone the Repository**

First, clone the repository containing the Terraform files.

```bash
git clone https://github.com/anakataa/IoT-Fire-Detection-and-Safety-System-
cd IoT-Fire-Detection-and-Safety-System-
```

### 2. **Configure Variables**

In the variables.tf file, set the required variables like Azure Region, Resource Group Name, and VM Sizes. Ensure that you have the correct configuration for your environment.

### 3. **Initialize Terraform**

Initialize the Terraform configuration to download necessary providers and modules.

```bash
terraform init
```

### 4. **Apply the Configuration**

To apply the Terraform configuration and create resources in Azure, run:

```bash
terraform plan
terraform apply
```

You will be prompted to confirm the action. Type YES to proceed with the deployment.

### 5. **Access the Deployed Resources**

Once the deployment is complete, Terraform will output information about the deployed resources, including:

- **Public IP of the MQTT Broker**

- **Backend API URL**

- **PostgreSQL connection details**

### 6. **Scripts for Monitoring & Cleanup**

Checks if the current Azure policy allows deploying resources in the selected region.

```bash
check-policy.sh
```

Checks the regions where you can deploy resources based on your subscription.

```bash
check-allowed-regions.sh
```

Fixes any issues related to Git versioning or Terraform-related files.

```bash
fix-git.sh
```

Removes Terraform files from version control (if needed).

```bash
remove-terraform-from-git.sh
```

### 7. **Tear Down the Deployment**

If you want to destroy the deployed resources, use the following command:

```bash
terraform destroy
```

You will be prompted to confirm. Type yes to tear down the resources.
