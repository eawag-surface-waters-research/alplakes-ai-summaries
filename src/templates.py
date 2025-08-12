from datetime import datetime
from functions import call_llm, simstrat_daily_average_forecast

def lake_condition_summary(lake):
    languages = [
        {"name": "french", "short": "FR"},
        {"name": "german", "short": "DE"},
        {"name": "italian", "short": "IT"},
    ]
    model = "openai/gpt-4.1-nano"
    forecast_table = simstrat_daily_average_forecast(lake)
    prompt = (
        "You are an assistant that interprets lake temperature forecasts.\n"
        "Here is the temperature forecast:\n\n"
        f"{forecast_table}\n\n"
        "Please describe the trend over the days. Is the lake warming or cooling?"
    )
    response = call_llm(model, prompt)
    output = {"produced": int(datetime.now().timestamp()), "data": {"EN": response}, "model": model, "prompt": prompt}
    for language in languages:
        lp = f'Translate the following into {language["name"]}: {response}'
        output["data"][language["short"]] = call_llm(model, lp)
    return output
