# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from graphene import ObjectType, InputObjectType, String, Int, Schema, Field, DateTime, Mutation, JSONString
import boto3

DYNAMO_DB_TABLE_NAME = 'demoempdb'

def getItemFromDynamoDb(tableName, empId, param=None):
    #Code to get the item into dynamo db
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tableName)
    response = table.get_item(Key={'empId': empId})
    print(response['Item'])
    result = response['Item']
    if param:
        result = response['Item'][param]
    print(result)
    return result

def getAllItemsFromDynamoDbTable(tableName):
    results = []
    lastEvaluatedKey = None
    client = boto3.client('dynamodb')
    while True:
        if lastEvaluatedKey:
            response = client.scan(
                TableName=tableName,
                ExclusiveStartKey=last_evaluated_key
            )
        else: 
            response = client.scan(TableName=tableName)
        lastEvaluatedKey = response.get('LastEvaluatedKey')        
        results.extend(response['Items'])       
        if not lastEvaluatedKey:
            break
    return results

class DemoEmployeeParamsInput(InputObjectType):
    empId = Int(required=True)
    empName = String(required=True)
    empTitle = String(required=True)
    empStartDate = String(required=True)

class DemoEmployeeParams(ObjectType):
    class Meta:
        description = 'Employee Parameters'
    empId = Int()
    empName = String()
    empTitle = String()
    empStartDate = String()
    empInfo = JSONString()
   
class CreateEntry(Mutation):
    class Arguments:
        empEntry = DemoEmployeeParamsInput(required=True)

    Output = DemoEmployeeParams
    def mutate(self, info, empEntry):
        #Code to add the item into dynamo db
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(DYNAMO_DB_TABLE_NAME)
        table.put_item(Item=empEntry)
        return DemoEmployeeParams(
            empId = empEntry.empId,
            empName = empEntry.empName,
            empTitle = empEntry.empTitle,
            empStartDate = empEntry.empStartDate
        )

class Mutation(ObjectType):
    empData = CreateEntry.Field()

class Query(ObjectType):
    empDetails = Field(DemoEmployeeParams, empId=Int(required=True))
    allEmpData = Field(DemoEmployeeParams)

    def resolve_allEmpData(root, info):        
        #Query the dynamodb here and get all the records for display
        data = {}
        data['empInfo'] = getAllItemsFromDynamoDbTable(DYNAMO_DB_TABLE_NAME)        
        return data
    
    def resolve_empDetails(root, info, empId):
        data = {}
        data = getItemFromDynamoDb(DYNAMO_DB_TABLE_NAME, empId)
        return data

empSchema = Schema(query=Query, mutation=Mutation)