import time
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from templates import lake_condition_summary
from functions import upload


def process_lake(lake, params):
    start_time = time.time()
    print(f"Starting processing for {lake}...")
    data = lake_condition_summary(lake)
    if params.get("upload"):
        upload(data, f"aisummary/{lake}/forecast.json", params)
    duration = time.time() - start_time
    print(f"Finished processing for {lake} in {duration:.2f} seconds.")
    return lake

def main(params):
    lakes = ["geneva", "garda", "upperconstance", "greifensee", "mondsee", "bled"]
    max_workers = params.get("parallel", 2)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_lake, lake, params) for lake in lakes]
        for future in as_completed(futures):
            lake = future.result()
            print(f"Completed processing for {lake}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--upload', '-u', help="Upload current value to S3 bucket", action='store_true')
    parser.add_argument('--bucket', '-b', help="S3 bucket", type=str, )
    parser.add_argument('--aws_id', '-i', help="AWS ID", type=str, )
    parser.add_argument('--aws_key', '-k', help="AWS KEY", type=str, )
    parser.add_argument('--parallel', '-p', help="Number of parallel processes", type=int, default=10)
    args = parser.parse_args()
    main(vars(args))
