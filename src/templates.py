from datetime import datetime
from functions import call_llm, simstrat_daily_average_forecast, simstrat_doy, simstrat_last_month

def lake_condition_summary(lake):
    languages = [
        {"name": "french", "short": "FR"},
        {"name": "german", "short": "DE"},
        {"name": "italian", "short": "IT"},
    ]
    model = "openai/gpt-5"
    forecast_table = simstrat_daily_average_forecast(lake)
    last_month_table = simstrat_last_month(lake)
    doy_table = simstrat_doy(lake)
    prompt = (
        "## 1 Context & Constraints\n"
        f"- Today is {datetime.now().strftime('%B %d, %Y')}"
        "- You are professional limnologist preparing a forecast for the lake conditions over the next few days\n"
        "- Formal, concise tone. ≤ 300 words\n"
        "- The report should be returned as a single paragraph with no new lines\n"
        "- You do not have any additional information than what is provided in the prompt\n"
        "- Do not include a call to action or any recommendations\n"
        "- Do not include any dates in the text\n"
        "- Do not include absolute temperature values\n"
        "- Only quote temperature values to at most 1 decimal place\n"
        "## 2 Input data\n"
        "- **Forecasted daily average surface temperature:**\n"
        f"{forecast_table}\n\n"
        "- **Daily average surface temperature for the 30 days:**\n"
        f"{last_month_table}\n\n"
        "- **Day of year average surface temperature statistics: **\n"
        f"{doy_table}\n\n"
        "## 3 Forecast instructions\n"
        "- First sentence that describes the general trend in the lake temperature over the days in the forecast."
        "Changes of more that 0.5 degrees per day are considered rapid changes.\n"
        f"- Second sentence that uses the day of year statistics to describe how today's temperature compares the historical records\n"
        "- Third sentence that uses the data from the last 30 days to describe the temperature trend of the past 30 days.\n"
    )
    print(f"Calling {model} with prompt")
    response = call_llm(model, prompt)
    output = {"produced": int(datetime.now().timestamp()), "data": {"EN": response}, "model": model, "prompt": prompt}

    for language in languages:
        print(f'Translating response to {language["name"]}')
        lp = f'Translate the following into {language["name"]}: {response}'
        output["data"][language["short"]] = call_llm("openai/gpt-4.1-nano", lp)
    return output
