from datetime import datetime
from functions import call_llm, simstrat_daily_average_forecast

def lake_condition_summary(lake):
    forecast_table = simstrat_daily_average_forecast(lake)
    prompt = (
        "You are an assistant that interprets lake temperature forecasts.\n"
        "Here is the temperature forecast:\n\n"
        f"{forecast_table}\n\n"
        "Please describe the trend over the days. Is the lake warming or cooling?"
    )
    response = call_llm("openai/gpt-4.1-nano", prompt)
    print(response)
    return {"produced": int(datetime.now().timestamp()), "data": {"EN": response}, "model": "openai/gpt-4.1-nano"}
