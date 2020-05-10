## nas : A simple tool to send thanks in Slack  
NAS is an easy way to say thank you on Slack.  
Use stamps and messages to express your gratitude to them.
I use the NAS if the other person does something for me (even if they don't do anything for me) or if I accomplish something amazing.
When you want to praise someone a little, you can send them a NAS by giving them a specific stamp on their message (you can set this stamp as you wish).
In particular, if you want to compliment them with a message, you can send them a public message using the slash command.

You can see the ranking of the NAS received by the entire group, and you can turn the gacha with the NAS you received.
From these, a good cycle of NAS will emerge and the community of group feeling will become even more active.

I hope you'll try using the NAS! Also, I'm waiting for your kind PR.

## Usage  
How to describe a simple image for use.

### nas stamp
Send a specific stamp to the message of the person you want to send the NAS to.  
The other party will see the user you sent and the type of NAS you got.

![image](https://user-images.githubusercontent.com/42530222/81496330-cea64c00-92f1-11ea-97c2-7519fed8b5c7.png)

### nas message
If you want to send a NAS with a message, use NAS MESSAGE.  
When you send what you want to send from the slack command, the thank you message will be published in its entirety.

![image](https://user-images.githubusercontent.com/42530222/81496421-8d626c00-92f2-11ea-91c9-55248a46e1d3.png)

![image](https://user-images.githubusercontent.com/42530222/81496604-b800f480-92f3-11ea-897a-cc152de8b354.png)

## environment
building a service on AWS. The general architecture is shown below.  

![image](https://user-images.githubusercontent.com/42530222/79628003-eb7ab400-8177-11ea-8d33-d60a9fd3eba1.png)

## Install

1. create a Slack App
Feel free to use your name.
[https://api.slack.com/apps](https://api.slack.com/apps)

2. clone this repository

3. Run `make_lambda_zip.sh` on the local machine.

4. create a role for lambda  
Create a new role and attach the following permissions
    - AmazonDynamoDBFullAccess
    - CloudWatchLogsFullAccess
    - AmazonAPIGatewayAdministrator

5. create a Lambda function  
Create a new Lambda function for the nas  
    - python : 3.8  
    - role : Give the role we created in step 4  

6. write the following directly in the lambda function and save it.  
In slack's app, in order to use Event Subscriptions, you need to perform challenge authentication first.
write this code to get it through.  
    ```python
    def lambda_handler(event, context):  
        print(event)  
        if "challenge" in event:  
            return event['challenge']  
    ```


7. Create the APIGateway.
Create an API Gateway and tie it to a Lambda function
    - Type : REST API
    - Endpoint Type : Region
    - Method : post
    - Join Type : lambda function

8. deploy the API Gateway.  
Deploy the API Gateway once to pass the Slack authentication. Please feel free to name your stage.  
Take note of the output deployment URL.

9. set up the Slack app.  
Make the following settings in the slack app you created.  
    **Slack Commands**  
    - /nas  
        - Request URL : API GatewayのデプロイURL
        - Short Description : send message with nas
        - Usage Hint:  /nas @receive_user_name message

    - /nas_st
        - Request URL : API GatewayのデプロイURL
        - Short Description : chack remain nas this week

    - /nas_rank
        - Request URL : API GatewayのデプロイURL
        - Short Description : check nas receive ranking this week.

    - /nas_gacha
        - Request URL : API GatewayのデプロイURL
        - Short DEscription : run nas gacha

    - nas_gacha_status
        - Request URL : API GatewayのデプロイURL
        - Short DEscription : run nas gacha

    - nas_gacha_tickets
        - Request URL : API GatewayのデプロイURL
        - Short DEscription :Check the gacha prizes you've won  

    **OAuth & Permissons**  
    Bot Token Scope
    - chat:write
    - chat:write.public
    - commands
    - user:read

    User Token Scopes
    - chat:write
    - reactions:read
    - user:read

    **Event Subscriptions**  
    Subscribe to events on behalf of users
    - reaction_added

10. The following is defined in the API Gateway integration request.  
    - Mapping template: If no template is defined (recommended)
    - Content-Type : application/json, application/x-www-form-urlencoded
    ```
    #set($allParams = $input.params())
    {
    "body" : $util.urlDecode($input.json('$')),
    "params" : {
    #foreach($type in $allParams.keySet())
        #set($params = $allParams.get($type))
    "$type" : {
        #foreach($paramName in $params.keySet())
        "$paramName" : "$util.escapeJavaScript($params.get($paramName))"
            #if($foreach.hasNext),#end
        #end
    }
        #if($foreach.hasNext),#end
    #end
    },
    "stage-variables" : {
    #foreach($key in $stageVariables.keySet())
    "$key" : "$util.escapeJavaScript($stageVariables.get($key))"
        #if($foreach.hasNext),#end
    #end
    },
    "context" : {
        "account-id" : "$context.identity.accountId",
        "api-id" : "$context.apiId",
        "api-key" : "$context.identity.apiKey",
        "authorizer-principal-id" : "$context.authorizer.principalId",
        "caller" : "$context.identity.caller",
        "cognito-authentication-provider" : "$context.identity.cognitoAuthenticationProvider",
        "cognito-authentication-type" : "$context.identity.cognitoAuthenticationType",
        "cognito-identity-id" : "$context.identity.cognitoIdentityId",
        "cognito-identity-pool-id" : "$context.identity.cognitoIdentityPoolId",
        "http-method" : "$context.httpMethod",
        "stage" : "$context.stage",
        "source-ip" : "$context.identity.sourceIp",
        "user" : "$context.identity.user",
        "user-agent" : "$context.identity.userAgent",
        "user-arn" : "$context.identity.userArn",
        "request-id" : "$context.requestId",
        "resource-id" : "$context.resourceId",
        "resource-path" : "$context.resourcePath"
        }
    }
    ```

11. Deploy the APIGateway again.

12. Create a Dynamo db  
Create the following two.
    - Table Name : NAS
        - Partition key : tip_user_id (string)
        - Sort key : time_stamp (number)  

    - Table name : NAS_GACHA
        - Partition key: user_id (string)

13. Adjusting Slack's environment variables  
Set the following as environment variables
    - NAS_LIMIT : Default 30 (set optionally)
    - SLACK_BOT_USER_ACCESS_TOKEN : Copy and paste from slack
    - SLACK_OAUTH_ACCESS_TOKEN : Copy and paste from slack
    - NAS_GACHA_COST = Default 10 (optional)
    - GACHA_WIN_RATE = 0.1 by default (set optionally)
    - PUBLIC_NAS_CHANNEL_ID : The ID of the Slack channel you want to broadcast the public message on (if not, create a new one)

15. Upload the Lambda function you created to Lambda  
Select upload with zip from the code entry type.  
Upload the file `lambda_function.zip`.What to do then
    - Set the handler of Lambda to `main.lambda_function`.
    - I'm going to give you a one minute timeout.

## Auther
twitter : [@0xb5951](https://twitter.com/0xb5951)  
github : [odrum428](https://github.com/odrum428)

## **COPYRIGHT**
MIT licence - Copyright (C) 2020