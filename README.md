# WattTime
Creating an easier way to interact with WattTime API v2 (api2.watttime.org)


## To use:  

If you already have a username and password registered with the API v2, then no need to register again. If you do not, follow these steps:


```
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
  
  
