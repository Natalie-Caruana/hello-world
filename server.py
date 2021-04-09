import click #create command line interface
from flask import Flask
import ibm_boto3
from ibm_botocore.client import Config, ClientError
import logging

PORT = 8000
#MESSAGE = "Hello, world Natalie!\n"


def create_app(cos_client,bucket_name):
    app = Flask(__name__)

    @app.route("/")
    def app_put_object_to_bucket():
        cos_client.Bucket(bucket_name).upload_file('error_log.log', 'error_log1.log')

    app.run(debug=True, host="0.0.0.0", port=PORT)

#@app.route("/")
#def root():
#    result = MESSAGE.encode("utf-8")
#    return result

@click.command()
@click.option('-x', '--cos-instance-id', help='COS instance ID')
@click.option('-e', '--cos-endpoint', help='COS endpoint URL')
@click.option('-k', '--api-key', help='IAM API key')
def start_app(cos_instance_id,cos_endpoint,api_key):

    if not cos_endpoint:
        logging.error('No valid COS endpoint specified')
        return -1


    if not api_key:
        logging.error('No IAM API key found')
        return -1

    destination_bucket = 'natalie-get-started-bucket'

    if not cos_instance_id:
        logging.error('No COS instance ID found')
        return -1


    cos_client = ibm_boto3.resource("s3",
                             ibm_api_key_id=api_key,
                             ibm_service_instance_id=cos_instance_id,
                             config=Config(signature_version="oauth"),
                             endpoint_url='https://s3.eu-de.cloud-object-storage.appdomain.cloud'
                             )
    create_app(cos_client,destination_bucket)


if __name__ == "__main__":
    start_app()
