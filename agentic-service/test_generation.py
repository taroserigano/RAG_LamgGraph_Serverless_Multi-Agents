"""Test the travel generation endpoint"""
import requests
import json
import time

print("Waiting for server to start...")
for i in range(15):
    try:
        r = requests.get("http://localhost:8000/", timeout=3)
        if r.status_code == 200:
            print(f"✅ Server is UP: {r.json()}")
            break
    except:
        time.sleep(2)
        print(f"  Attempt {i+1}/15...")
else:
    print("❌ Server didn't start")
    exit(1)

print("\n" + "="*60)
print("TESTING TRAVEL PLAN GENERATION")
print("="*60)

payload = {
    "city": "Paris",
    "country": "France",
    "days": 2,
    "budget": 2000,
    "user_id": "test_user",
    "preferences": ["culture", "food"]
}

print(f"\nRequest: {json.dumps(payload, indent=2)}")
print("\nCalling /api/v1/agentic/generate-itinerary...")
print("(This may take 30-60 seconds for AI generation + Amadeus API calls)")

try:
    response = requests.post(
        "http://localhost:8000/api/v1/agentic/generate-itinerary",
        json=payload,
        timeout=120
    )
    
    print(f"\nResponse Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n" + "="*60)
        print("✅ SUCCESS - TRAVEL GENERATION WORKS!")
        print("="*60)
        
        print(f"\nRun ID: {data.get('run_id')}")
        print(f"Status: {data.get('status')}")
        
        tour = data.get('tour', {})
        print(f"\nTrip Details:")
        print(f"  Title: {tour.get('title')}")
        print(f"  City: {tour.get('city')}, {tour.get('country')}")
        print(f"  Description: {tour.get('description', '')[:100]}...")
        print(f"  Stops: {len(tour.get('stops', []))} locations")
        
        # Check for real Amadeus data
        real_data = tour.get('real_data', {})
        if real_data.get('has_real_data'):
            print(f"\n🎉 AMADEUS REAL TRAVEL DATA:")
            flights = real_data.get('flights', [])
            hotels = real_data.get('hotels', [])
            print(f"  ✈️  Flights found: {len(flights)}")
            if flights:
                cheapest = min(flights, key=lambda x: float(x['price']['total']))
                print(f"     Cheapest: {cheapest['price']['currency']} {cheapest['price']['total']}")
            
            print(f"  🏨 Hotels found: {len(hotels)}")
            if hotels:
                for i, hotel in enumerate(hotels[:3], 1):
                    print(f"     {i}. {hotel.get('name', 'N/A')}")
        else:
            print(f"\n⚠️  No Amadeus data (may need valid API keys)")
        
        # Check daily schedule
        schedule = tour.get('daily_schedule', [])
        if schedule:
            print(f"\n📅 Daily Schedule: {len(schedule)} days planned")
            for day in schedule[:2]:  # Show first 2 days
                print(f"  Day {day.get('day')}: {day.get('theme', 'N/A')}")
        
        print("\n" + "="*60)
        print("FULL RESPONSE (first 500 chars):")
        print("="*60)
        print(json.dumps(data, indent=2)[:500] + "...")
        
    else:
        print(f"\n❌ FAILED with status {response.status_code}")
        print(f"\nError Response:")
        try:
            error_data = response.json()
            print(json.dumps(error_data, indent=2))
        except:
            print(response.text[:500])
            
except requests.exceptions.Timeout:
    print("\n❌ REQUEST TIMED OUT (>120 seconds)")
    print("This might mean:")
    print("  - OpenAI API is slow")
    print("  - Amadeus API is slow")
    print("  - Server is stuck on something")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")

