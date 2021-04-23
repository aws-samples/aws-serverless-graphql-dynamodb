# aws-serverless-graphql-dynamodb

This project provides a sample code to implement API GW GraphQL API's (sample code uses python grpahql library Graphene) in Lambda function to create and read the record from DynamoDB Table. The sample code also do have a SAM template for easy deployment.

This sample can be used as reference to implement GraphQL API using API GW/Lambda which needs data to be written to and read from DynamoDB.

## Pre-requisites:

1.  You need to have SAM CLI Installed already. Follow the link for details and installation of SAM CLI: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html
2.  Docker

## Steps to setup

1. Clone the repo
2. Build using the command sam build --template template.yaml --use-container
3. Deploy using the command sam deploy --guided

## Example Queries
### Add a new entry
/graphql?query="mutation addnewentry{empData(empEntry: {empId: 1, empName: "abc", empTitle: "architect", empStartDate: "14-Jan-2021" }) {empId empName empTitle empStartDate}}"

### Get all the records of employees
/graphql?query="{allEmpData{empInfo}}"

### Get the record of specific employee using employee id
#### To receive only employee name who belong to provided employee id
/graphql?query="{empDetails(empId: 1) { empName }}"
#### To receive only employee start data who belong to provided employee id
/graphql?query="{empDetails(empId: 1) { empStartDate }}"
#### To receive only employee title who belong to provided employee id
/graphql?query="{empDetails(empId: 1) { empTitle }}"
#### To receive only employee name, title and start date who belong to provided employee id
/graphql?query="{empDetails(empId: 1) { empName empTitle empStartDate }}"

## Cleanup

To delete the deployment created using sam deploy, use the AWS CLI command. Assuming you used the project name for the stack name, you can execute the following command:

```bash
aws cloudformation delete-stack --stack-name aws-serverless-graphql-dynamodb
```
## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
