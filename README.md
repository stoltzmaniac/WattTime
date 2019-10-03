# WattTime API v2 - Easy to Use Model
Creating an easier way to interact with WattTime API v2 (api2.watttime.org) The API documentation is at: <https://watttimeapiv2.docs.apiary.io> and the Watttime organization is really cool, so check them out at <https://www.watttime.org/>.

Written in Python 3.7, should work with 3.6+

On PyPI
`pip install watttime`

## To use:  

If you already have a username and password registered with the API v2, then no need to register again. If you do not, follow these steps:


```
from watttime.api import WattTime

w = WattTime(username=<DesiredUsername>, password=<YourDesiredPassword>)
w.register(email=<your@email.com>, organization=<your organization>)
``` 

console output:  
```
Registering...
{'user': '<DesiredUsername>', 'ok': 'User created'}
```


If you need to reset your password:  
```
w.reset_password()
```

console output:
```
{'ok': 'Please check your email for the password reset link'}
```
  
  
Before you do any work, you must request a token:  
```
w.get_token()
```

console output:
```
{'token': 'crazy_hash'}
Token received, setting headers: crazy_hash
```

Now you're ready to get your realtime emissions!!!

If you want to use latitude and longitude, pass them into your function explicitly
```
data = w.get_realtime_emissions(latitude=37.871667, longitude=-122.272778)
```

console output:
```
No balancing authority passed, getting data for
    latitude=37.871667
    longitude=-122.272778
{'id': 137, 'abbrev': 'CAISO_NP15', 'name': 'CAISO NP15 Trading Hub'}
Setting balancing_authority: CAISO_NP15
Getting data for balancing authority: CAISO_NP15
URL requested = https://api2.watttime.org/v2/index/?ba=CAISO_NP15&style=all
{'validUntil': '2019-10-02T21:45:00Z', 'pointTime': '2019-10-02T21:40:00Z', 'freq': '300', 'market': 'RTM', 'ba': 'CAISO_NP15', 'rating': '4', 'switch': '0', 'percent': '64', 'point_time': '2019-10-02T21:40:00Z', 'validFor': 175}
```

your `data` variable output in console:
```
{'validUntil': '2019-10-02T21:45:00Z',
 'pointTime': '2019-10-02T21:40:00Z',
 'freq': '300',
 'market': 'RTM',
 'ba': 'CAISO_NP15',
 'rating': '4',
 'switch': '0',
 'percent': '64',
 'point_time': '2019-10-02T21:40:00Z',
 'validFor': 175}
```

If you prefer to pass in a balancing authority, you may do so explicitly as well. *Note*: anything you pass as `ba` will overwrite and set your instance `balancing_authority` to whatever you pass and that will be used by default until you change it. 
```
w.get_realtime_emissions(ba='<your_balancing_authority_abbreviation>')
```

If you need to find a balancing authority (because you can't overwrite by using `latitude` and `longitude` alone, use the `get_balancing_authority` function in order to override it.

```
w.get_balancing_authority(latitude=37.871667, longitude=-122.272778)
```

Then you may proceed as normal!
