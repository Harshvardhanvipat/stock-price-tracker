# Deploying Stock Price Tracker to AWS

This guide explains how to deploy your application to AWS Lambda using the AWS Serverless Application Model (SAM).

## Prerequisites

1.  **AWS Account**: You need an active AWS account.
2.  **AWS CLI**: Installed and configured with your credentials (`aws configure`).
3.  **AWS SAM CLI**: Installed on your machine.
    -   [Install SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

## Deployment Steps

1.  **Build the Application**
    This prepares the deployment package.
    ```bash
    sam build
    ```

2.  **Deploy to AWS**
    This creates the resources (Lambda, DynamoDB, API Gateway) in your AWS account.
    ```bash
    sam deploy --guided
    ```
    
    **Follow the prompts:**
    -   **Stack Name**: `stock-tracker`
    -   **AWS Region**: Choose one close to you (e.g., `us-east-1` or `ap-southeast-2`).
    -   **Confirm changes before deploy**: `Y`
    -   **Allow SAM CLI IAM role creation**: `Y`
    -   **Disable rollback**: `N`
    -   **StockTrackerFunction may not have authorization defined, Is this okay?**: `Y` (This makes the API public).
    -   **Save arguments to configuration file**: `Y`

3.  **Access the App**
    After deployment succeeds, SAM will output the `StockTrackerApi` URL (e.g., `https://xyz.execute-api.us-east-1.amazonaws.com/`).
    Open this URL in your browser.

## Cost Management (Free Tier)

-   **DynamoDB**: The template uses `ProvisionedThroughput` of 1 RCU/1 WCU, which is well within the 25 RCU/WCU Free Tier limit.
-   **Lambda**: The 5-minute schedule runs ~8,640 times/month. With 128MB memory and short execution time, this is negligible against the 400,000 GB-seconds free tier.
-   **Clean Up**: To delete all resources and stop incurring any potential costs:
    ```bash
    sam delete
    ```

## Troubleshooting

-   **Logs**: View logs for your Lambda functions in the AWS Console under **CloudWatch > Log groups**.
-   **500 Errors**: Check CloudWatch logs for Python exceptions (e.g., missing dependencies or permission issues).
