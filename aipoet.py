import json
from datetime import datetime, timezone
from groq import Groq

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def lambda_handler(event, context):
    latitude = event['latitude']
    longitude = event['longitude']

    # Extract location data directly from the event
    location_data = event['location_data']
    weather_data = event['weather_data']
    
    # Convert temperature to Fahrenheit
    temperature_f = celsius_to_fahrenheit(weather_data['temperature'])
    
    # Create the prompt with the received data
    prompt = (
        f"Make a poem about the user's area/weather, neighborhood specific fun facts (somewhat creepy that you know about their location). 2 sentences (dont say zip code). Here's what's nearby: "
        f"{location_data['display_name']}. " 
        f"The UTC time is: {datetime.now(timezone.utc)}. "
        f"The current weather is: {temperature_f:.1f}°F with {weather_data['weathercode']}, "
        f"windspeed {weather_data['windspeed']} km/h, wind direction {weather_data['winddirection']}°."
        f" Your name is BennyAI."
    )
    
    # Call the LLM with the prompt
    poem = generate_poem_with_llm(prompt)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'poem': poem
        })
    }

def generate_poem_with_llm(prompt):
    # Replace this with the call to your LLM API
    api_key = "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"
    # Assuming the client initialization and method to call LLM
    client = Groq(api_key=api_key)
    
    completion = client.chat.completions.create(
        model="gemma2-9b-it",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    
    poem = completion.choices[0].message.content
    return poem

def main():
    # Simulate an event for local testing
    test_event = {
        'latitude': 38.8830,
        'longitude': -77.0969,
        'location_data': {
            "display_name": "815, North Garfield Street, Lyon Park, Clarendon, Arlington, Arlington County, Virginia, 22201, United States",
            "address": {
                "house_number": "815",
                "road": "North Garfield Street",
                "neighbourhood": "Lyon Park",
                "suburb": "Clarendon",
                "city": "Arlington",
                "county": "Arlington County",
                "state": "Virginia",
                "postcode": "22201",
                "country": "United States"
            }
        },
        'weather_data': {
            "temperature": 21.1,
            "weathercode": "clear sky",
            "windspeed": 6.8,
            "winddirection": 295
        }
    }

    test_context = {}

    response = lambda_handler(test_event, test_context)
    
    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    main()
