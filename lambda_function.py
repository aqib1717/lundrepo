import os
import boto3
from PIL import Image
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the source bucket and key from the S3 event
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    source_key = event['Records'][0]['s3']['object']['key']

    # Get the file extension of the uploaded image
    file_extension = os.path.splitext(source_key)[1][1:].lower()

    # Define the desired format for the converted image
    desired_format = 'png'  # Convert to PNG format

    # Define the output path and filename for the converted image
    output_key = 'converted/' + os.path.splitext(source_key)[0] + '.' + desired_format

    try:
        # Download the image from the source bucket
        response = s3.get_object(Bucket=source_bucket, Key=source_key)
        image = Image.open(response['Body'])

        # Convert the image to the desired format if it is not already PNG
        if file_extension != 'png':
            output = image.convert('RGBA')  # Convert to RGBA before saving as PNG
            output_buffer = io.BytesIO()
            output.save(output_buffer, format='png')
            output_buffer.seek(0)

            # Upload the converted image to the destination bucket
            s3.put_object(Body=output_buffer, Bucket='convertedimagebucket1', Key=output_key)

            return {
                'statusCode': 200,
                'body': 'Image conversion successful'
            }
        else:
            return {
                'statusCode': 400,
                'body': 'Image format not supported. Only non-PNG images are allowed.'
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': 'Image conversion failed: ' + str(e)
        }
