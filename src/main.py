import argparse
from templates import lake_condition_summary
from functions import upload

def main(params):
    for lake in ["geneva"]:
        data = lake_condition_summary(lake)
        if params["upload"]:
            upload(data, "aisummary/{}/forecast.json".format(lake), params)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--upload', '-u', help="Upload current value to S3 bucket", action='store_true')
    parser.add_argument('--bucket', '-b', help="S3 bucket", type=str, )
    parser.add_argument('--aws_id', '-i', help="AWS ID", type=str, )
    parser.add_argument('--aws_key', '-k', help="AWS KEY", type=str, )
    args = parser.parse_args()
    main(vars(args))
