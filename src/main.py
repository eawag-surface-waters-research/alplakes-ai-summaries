import os
import boto3
import tempfile
import argparse
from templates import lake_condition_summary

def main(params):
    for lake in ["geneva"]:
        data = lake_condition_summary("geneva")
        if params["upload"]:
            bucket_key = params["bucket"].split(".")[0].split("//")[1]
            s3 = boto3.client("s3", aws_access_key_id=params["aws_id"], aws_secret_access_key=params["aws_key"])
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
                temp_filename = temp_file.name
                temp_file.write(data)
            s3.upload_file(temp_filename, bucket_key, "aisummary/{}/forecast.json".format(lake))
            os.remove(temp_filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--upload', '-u', help="Upload current value to S3 bucket", action='store_true')
    parser.add_argument('--bucket', '-b', help="S3 bucket", type=str, )
    parser.add_argument('--aws_id', '-i', help="AWS ID", type=str, )
    parser.add_argument('--aws_key', '-k', help="AWS KEY", type=str, )
    args = parser.parse_args()
    main(vars(args))
