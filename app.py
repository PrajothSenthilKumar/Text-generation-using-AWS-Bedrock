import boto3
import botocore.config
import json
from datetime import datetime

def blog_generate_using_bedrock(blogtopic:str) -> str:
    prompt = f"""<s>[INST]Human: write a 200 words blog on the topic {blogtopic}
                          Assistant:[/INST]"""
    try:
        bedrock_rt = boto3.client("bedrock-runtime", region_name = 'ap-south-1', 
                                config = botocore.config.Config(read_timeout = 300, retries = {'max_attempts':3}))
        
        body = json.dumps({
            "prompt": prompt,
            "max_gen_len": 1024,
            "temperature": 0.2,
            "top_p": 0.9
            })

        model_Id = "meta.llama3-8b-instruct-v1:0"
        accept = "application/json"
        contentType = "application/json"
        response = bedrock_rt.invoke_model(
            body = body,
            modelId = model_Id,
            accept = accept,
            contentType = contentType
        )
        response_body = json.loads(response.get("body").read())
        print(response_body)
        blog_details = response_body.get("generation")
        return blog_details
    
    except Exception as e:
        print(f"Error generating the blog:{e}")
        return ""
    
def save_blog_details(s3_key:str, s3_bucket:str, blog_details:str) -> None:
    try:
        s3 = boto3.client('s3')
        s3.put_object(Body=blog_details, Bucket=s3_bucket, Key=s3_key)
        print(f"Blog details saved to s3://{s3_bucket}/{s3_key}")
    except Exception as e:
        print(f"Error saving blog details to S3: {e}")

    return{
        'statusCode': 200,
        'body': json.dumps('Blog Generated Successfully')
    }

def lambda_handler(event, context):
    try:
        event_body = json.loads(event["body"])
        bloggtopic = event_body.get("blog_topic")
    
        generate_blog = blog_generate_using_bedrock(blogtopic = bloggtopic)
    
        if generate_blog:
            current_time = datetime.now().strftime('%H%M%S')
            s3_key = f"blog_output/{current_time}.txt"
            s3_bucket = "awsbedrockexercise1"
            save_blog_details(s3_key, s3_bucket, generate_blog)
            return {
                'statusCode': 200,
                'body': json.dumps('Blog Generated Successfully')
            }
            
        else:
            print(f"No Blog was created")
    except Exception as e:
        print(f"Error in lambda_handler: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }


