### Installing

``` bash
pip uninstall -r requirements.txt -y
```

## UA_ALARM

> Elegant, modern and asynchronous UkraineAlarm API framework in Python

``` python
from ua_alarm import Client
import os
import asyncio

# Clear the console screen
os.system('cls' if os.name == 'nt' else 'clear')

async def main():
    # Example usage:
    api_token = "YOUR_API_KEY"
    client = Client(api_token)

    # Get a list of alerts
    alerts = await client.get_alerts()
    print(alerts)

# Run the main function
asyncio.run(main())
```