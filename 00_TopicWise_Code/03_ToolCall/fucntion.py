# Approach 1: Code function ko platform schema ke according banao

@function_tool
def get_weather(location: str, unit: str = "c") -> str:  # ← Match platform schema
    """
    Determine weather in my location
    
    Args:
        location: The city and state e.g. San Francisco, CA
        unit: Temperature unit ('c' for Celsius, 'f' for Fahrenheit)
    """
    try:
        # API call
        result = requests.get(
            f"http://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={location}"
        )
        data = result.json()
        
        # Unit conversion
        if unit.lower() == "f":
            temp = data["current"]["temp_f"]
            unit_display = "°F"
        else:
            temp = data["current"]["temp_c"] 
            unit_display = "°C"
            
        return f"The current weather in {location} is {temp}{unit_display} with {data['current']['condition']['text']}."
    
    except Exception as e:
        return f"Could not fetch weather data due to {e}"

# Agent with platform prompt
agent = Agent(
    name="Weather Assistant",
    prompt={
        "id": "your_platform_prompt_id",  # Platform schema use hoga
    },
    tools=[get_weather],  # Function schema match karega platform se
    model="gpt-4o"
)
