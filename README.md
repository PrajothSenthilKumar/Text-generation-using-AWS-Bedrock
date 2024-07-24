**Text Generation using AWS Bedrock**

**Before implementing the below, in the terminal create a virtual environment "conda create -p venv python==3.12" and activate the environment by "conda activate '.....\venv'".**

**Request the required model access from the bedrock console in AWS. In our case it is meta llama3.**

**1) Lambda function logic to invoke the Bedrock Foundation Model. Whenever my api-gateway captures any post event and the context, it triggers the Lambda function by hitting the lambda-handler() first.**

![LamdaScreenshot](https://github.com/user-attachments/assets/4a289164-25b1-4f1d-aa0e-f94962463da4)

![LambdaScreenshot1](https://github.com/user-attachments/assets/680b695a-65fa-49a2-9b1e-ccc50e14b712)

**2) The lambda function wants the most recent version of boto3, so --> "pip install boto3 -t python/". This command will install the required package in the folder named "python". Now compress this folder and make a zip file "boto3-layer.zip".**
   
**In the Lambda function, go to layers --> Add a layer. Now upload the .zip file and choose runtimes  --> python 3.10, 3.11, 3.12. Create the layer. Now add that layer to the lambda function.**

![LamdaLayer](https://github.com/user-attachments/assets/0425fdad-d76e-4012-bdeb-1df7bd89d235)

**3) Create the Api gateway, so it can trigger the Lambda function. After creating it, inside Api gateway, create routes for the created api as,
         1) Request Type --> Post
         2) /blog-generation, and create route.**

![LambdaRoute](https://github.com/user-attachments/assets/42c185a1-7c34-4008-8fd1-b6660d8a2583)


   **After that select the created route "POST" and attach integration by,
         1) select "create and attach and integration"
         2) integration type --> Lambda function (select our Lambda function) and create.**

![LambdaIntegration](https://github.com/user-attachments/assets/35c61691-35e2-42f9-9b65-b2a1beca7b41)

    Finally, create the stages for the created API in the Api gateway by,
         1) Create --> stages
         2) Name = dev, and create the stage. Inside this "dev" environment click "deploy" in order to deploy this entire URL that I have to use to interact with my Lambda function.
         
![LambdaStage](https://github.com/user-attachments/assets/2a3f50e6-a942-42ed-89aa-1b88d0aa327a)


**4) Add the necessary permission to invoke the bedrock model by attaching the required permissions to the role attached to the Lambda function. To do that,
         1) In Lambda --> Configuration --> Select the role
         2) Attach the policy --> administrator access**

![LambdaIAM](https://github.com/user-attachments/assets/c8681c1f-166b-4097-8730-23034a96ae84)


**5) Now create an S3 bucket with the bucket name specified in the app.py**

![S3Screenshot](https://github.com/user-attachments/assets/9c9f645d-b29a-4205-bfc6-05b5e25deea6)

**6) Finally open the Postman application. Create a new file and select "post" request. Then paste the URL(which was on the stages page that we deployed earlier) along with it add our created route as /blog-generation at the end of the URL.**

**Inside the Body of Postman add this,**

    {
      "blog_topic" : "........." (any topic you want inside the quotes)
    }

**This "blog_topic" variable we have specified inside the lambda_handler. Specify the same variable name over here in the body of Post request.**

**and click send**

**7) We would receive output as "Blog Generated Successfully"**

**To view it go to Lambda --> Monitor --> Cloudwatch Logs**

![CloudWatch1](https://github.com/user-attachments/assets/c90a3377-1952-4aeb-badd-f675574dd4a5)

![CloudWatch2](https://github.com/user-attachments/assets/311674d8-1dca-4212-8ae0-915bdae5c61f)

**And finally, the blog generated is saved successfully in S3**

![S3Output](https://github.com/user-attachments/assets/72fc92e6-5fa2-4033-a518-0754e2fae9cf)

