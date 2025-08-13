import os
import json
import boto3
import tempfile
import requests
from datetime import datetime, timedelta
from any_llm import completion

def call_llm(model, message):
    response = completion(
        model=model,
        messages=[{"role": "user", "content": message}]
    )
    return response.choices[0].message.content


def call_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise ValueError(f"Unable to access url {url}. Status code: {response.status_code}. Message: {response.text}")


def simstrat_daily_average_forecast(lake):
    start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=6)
    data = call_url(f'https://alplakes-api.eawag.ch/simulations/1d/point/simstrat/{lake}/{start.strftime("%Y%m%d%H%M")}/{end.strftime("%Y%m%d%H%M")}/0?resample=daily&variables=T')
    out = {
        "Date": [x[:10] for x in data["time"]],
        "Temperature (°C)": data["variables"]["T"]["data"]
    }
    return dict_to_markdown_table(out)


def simstrat_last_month(lake):
    end = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    start = end - timedelta(days=30)
    data = call_url(
        f'https://alplakes-api.eawag.ch/simulations/1d/point/simstrat/{lake}/{start.strftime("%Y%m%d%H%M")}/{end.strftime("%Y%m%d%H%M")}/0?resample=daily&variables=T')
    out = {
        "Date": [x[:10] for x in data["time"]],
        "Temperature (°C)": data["variables"]["T"]["data"]
    }
    return dict_to_markdown_table(out)

def simstrat_doy(lake):
    now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = now + timedelta(days=1)
    now_doy = now.timetuple().tm_yday - 1
    data = call_url(f'https://alplakes-api.eawag.ch/simulations/1d/doy/simstrat/{lake}/T/0')
    dt1 = datetime.fromisoformat(data["start_time"])
    dt2 = datetime.fromisoformat(data["end_time"])
    years = dt2.year - dt1.year - ((dt2.month, dt2.day) < (dt1.month, dt1.day))
    data2 = call_url(
        f'https://alplakes-api.eawag.ch/simulations/1d/point/simstrat/{lake}/{now.strftime("%Y%m%d%H%M")}/{tomorrow.strftime("%Y%m%d%H%M")}/0?resample=daily&variables=T')
    out = {
        "": ["Today", f"{years} year mean", f"{years} year min", f"{years} year max"],
        "Temperature (°C)": [
            data2["variables"]["T"]["data"][0],
            data["variables"]["mean"]["data"][now_doy],
            data["variables"]["min"]["data"][now_doy],
            data["variables"]["max"]["data"][now_doy]
        ]
    }
    return dict_to_markdown_table(out)


def dict_to_markdown_table(data_dict):
    if not data_dict:
        return ""
    headers = list(data_dict.keys())
    num_rows = len(next(iter(data_dict.values())))
    for col in data_dict.values():
        if len(col) != num_rows:
            raise ValueError("All columns must have the same number of rows.")
    header_row = " | ".join(headers)
    separator_row = " | ".join(["-" * len(header) for header in headers])
    rows = []
    for i in range(num_rows):
        row = " | ".join(str(data_dict[header][i]) for header in headers)
        rows.append(row)
    table = header_row + "\n" + separator_row + "\n" + "\n".join(rows)
    return table

def upload(data, remote_path, params):
    bucket_key = params["bucket"].split(".")[0].split("//")[1]
    print(f"Uploading response to {bucket_key}")
    s3 = boto3.client("s3", aws_access_key_id=params["aws_id"], aws_secret_access_key=params["aws_key"])
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
        temp_filename = temp_file.name
        temp_file.write(json.dumps(data))
    s3.upload_file(temp_filename, bucket_key, remote_path)
    os.remove(temp_filename)
    print("Completed upload successfully")