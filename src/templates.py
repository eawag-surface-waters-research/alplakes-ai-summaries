from datetime import datetime
from functions import call_llm, simstrat_daily_average_forecast, simstrat_doy, simstrat_last_month

lake_condition_summary_prompt = """
## Lake Temperature Forecast Prompt (Natural Language Version)

**CONTEXT**  
- Today’s date: **{today_str}**  
- Task: Write a brief lake temperature summary like a local weather forecast
- Style: Conversational and clear - how a meteorologist would actually speak
- Format: One paragraph, 3 sentences, 80-120 words total

**CORE RULES**
- Write like you're talking, not writing a scientific paper
- Keep it simple - no technical jargon
- Be concise - short, clear sentences
- Sound natural - like a weather forecast on the radio

**FORECAST_TEMPERATURES**  
{forecast_table}

**HISTORICAL_STATS**  
{doy_table}

**PAST_30_DAYS_TEMPERATURES**  
{last_month_table}

**OUTPUT STRUCTURE**
Sentence 1: What's happening this week
Source: **FORECAST_TEMPERATURES**
- Just tell us if temps are going up, down, or staying the same
- Mention the actual temperature range (like "around 21 degrees")
- Keep it under 30 words
Good examples:
- "Lake temperatures are expected to stay around 21°C this week."
- "A slight cooling trend is expected, with temperatures dipping from 21.3°C to 21°C by Thursday."
- "Expect stable conditions with temperatures hovering near 21 degrees."
Avoid:
- "thermal regime" → just say "temperatures"
- "modest cooling pattern" → say "slight cooling"
- "drift gently" → say "drop slowly"

Sentence 2: How this compares to normal
Source: **HISTORICAL_STATS**  
- Simply state if it's warmer or cooler than usual
- Mention the actual numbers
- Keep it under 30 words
Good examples:
- "That's about a degree above the September average of 20 degrees."
- "Temperatures are higher than normal but still below the record high of 22.9°C."
- "These readings are slightly higher than the typical 20 degrees expected in early September."
Avoid:
- "41-year mean" → say "average" or "normal"
- "seasonal variability" → skip this entirely
- "falling well short of" → say "below"

Sentence 3: What happened last month
Source: **PAST_30_DAYS_TEMPERATURES**
- Describe the recent trend in plain English
- Mention specific temperature change if significant
- Keep it under 35 words
Good examples:
- "The lake has cooled about 4 degrees since mid-August's peak of 25 degrees."
- "We've seen steady cooling over the past month, down from 25 degrees in August."
- "Temperatures have dropped significantly from last month's highs near 25 degrees."
Avoid:
- "substantial cooling regime" → say "cooled quite a bit"
- "thermal evolution" → just describe what happened
- "marked shift that underscores" → keep it simple

**TEMPERATURE RULES**
- Round to 1 decimal: 21.302 → 21.3
- Drop trailing zeros: 21.0 → 21
- Only use "°C" when quoting temperature

**BANNED PHRASES**
Never use these academic/technical terms:
- thermal regime, thermal profile, thermal evolution
- modest/marked/substantial (use simple/slight/big instead)
- drift, persist, underscore, situate
- seasonal variability, band of variability
- moderation, adjustment, pattern

**GOOD WORD CHOICES**
Use everyday words:
- going up/down, rising/falling, warming/cooling
- steady, stable, little change
- above/below normal, warmer/cooler than usual
- typical, average, normal
- peak, high, low

**QUALITY CHECK**
□ Sounds like a weather forecast, not a research paper 
□ 3 sentences, 80-120 words total 
□ Each sentence under 35 words 
□ No technical jargon 
□ Would sound natural on the radio 
□ Clear and to the point

**EXAMPLE OUTPUT** (Natural Style)
Good Example: "Lake temperatures will hold near 21.3 degrees through midweek before easing to 21 degrees by Thursday. That’s about a degree above the September average of 20, yet still shy of the record 22.9. The lake has dropped nearly 4 degrees since mid-August’s peak of 25, following the usual late-summer cooling trend."
Why this works:
- Short, clear sentences (17, 18, 20 words)
- Natural language ("easing to", "shy of the record", "peak of 25")
- Sounds like someone talking
- Total: 55 words, perfectly concise

**FINAL INSTRUCTION**
Generate a natural-sounding lake temperature summary using everyday language. Write it like you're a local meteorologist giving a quick update on the radio - friendly, clear, and to the point. Three sentences only, keeping each one short and simple. Use the data provided but translate it into plain English that anyone would understand.
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
