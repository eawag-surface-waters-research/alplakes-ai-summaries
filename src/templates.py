from datetime import datetime
from functions import call_llm, simstrat_daily_average_forecast, simstrat_doy, simstrat_last_month

lake_condition_summary_prompt = """
## Lake Temperature Forecast Prompt

**CONTEXT**  
- Today’s date: **{today_str}**  
- Role: Professional limnologist.  
- Task: Produce a lake surface temperature forecast report.  
- Tone: **Formal**, **concise**, **scientific**.  
- Length: **One paragraph**, **<300 words**, **no new lines**.  

**OUTPUT RULES**  
1. Do **not** include dates in the text.  
2. Do **not** include calls to action or recommendations.  
3. Round all temperature values to **1 decimal place**, no trailing zeros.  
4. Only include absolute temperature values when comparing to historical statistics.  
5. Paragraph must contain **exactly three sentences** in the order below.  

**SENTENCE 1 — Forecast Trend**  
- Use only **FORECAST_TEMPERATURES**.  
- Describe trend over the forecast period.  
- If any single-day change > 0.5 °C, call it a “rapid cooling/ heating” increase or decrease; otherwise, describe as gradual cooling/ heating or stable.  
- State whether temperatures are increasing, decreasing, or stable overall.  

**SENTENCE 2 — Historical Comparison**  
- Use **HISTORICAL_STATS**.  
- Compare today’s temperature to the mean, min, and max for this day of year.
- Indicate whether today’s temperature is above, below, or near each statistic.  
- Do **not** mention the min if above the mean, and do **not** mention the max if below the mean.  

**SENTENCE 3 — Past 30-Day Trend**  
- Use only **PAST_30_DAYS_TEMPERATURES**.  
- Describe the trend over the 30 days.

**FORECAST_TEMPERATURES**  
{forecast_table}

**PAST_30_DAYS_TEMPERATURES**  
{last_month_table}

**HISTORICAL_STATS**  
{doy_table}

**EXAMPLE IDEAL OUTPUTS**  
Example 1: Surface temperatures are projected to rise gradually over the next four days, with no rapid daily changes expected. Today’s value stands well above the long-term mean and minimum for this time of year, yet remains below the historical maximum. Over the past month, a cold spell caused the lake to cool before increasing again over the last 10 days.  
Example 2: A gradual upward trend in surface temperatures is expected over the next five days, with daily changes remaining moderate. Current conditions exceed both the multi-decade mean and historical minimum for this day, while remaining beneath the recorded maximum. Over the last thirty days, the lake has warmed consistently, reflecting an overall increase of 2.9 degrees.  
Example 3: Forecast data indicate a stable to gently increasing temperature pattern over the coming days, without any rapid shifts. Present readings are markedly higher than the long-term mean and minimum for the date but have not approached the record high. Analysis of the past month reveals a sustained warming phase totaling approximately 2.9 degrees.
"""

def lake_condition_summary(lake):
    languages = [
        {"name": "french", "short": "FR"},
        {"name": "german", "short": "DE"},
        {"name": "italian", "short": "IT"},
    ]
    model = "openai/gpt-5-mini"
    forecast_table = simstrat_daily_average_forecast(lake)
    last_month_table = simstrat_last_month(lake)
    doy_table = simstrat_doy(lake)

    prompt = lake_condition_summary_prompt.format(
        today_str=datetime.now().strftime('%B %d, %Y'),
        forecast_table=forecast_table,
        last_month_table=last_month_table,
        doy_table=doy_table,
    )

    print(f"Calling {model} with prompt")
    response = call_llm(model, prompt)

    output = {"produced": int(datetime.now().timestamp()), "data": {"EN": response}, "model": model, "prompt": prompt}

    for language in languages:
        print(f'Translating response to {language["name"]}')
        lp = f'Translate the following into {language["name"]}: {response}'
        output["data"][language["short"]] = call_llm("openai/gpt-4.1-nano", lp)
    return output
