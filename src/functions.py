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