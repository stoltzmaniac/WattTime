import requests
import base64


class WattTime:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = None
        self.headers = None
        self.balancing_authority = None

    def get_token(self):
        creds_raw = f"{self.username}:{self.password}".encode()
        creds_encoded = base64.b64encode(creds_raw).decode("utf-8")
        headers = {
            'Authorization': f'Basic {creds_encoded}'
        }

        req = requests.get('https://api2.watttime.org/v2/login/', headers=headers)
        print(req.json())

        self.token = req.json().get('token')
        if self.token:
            print(f"Token received, setting headers: {self.token}")
            self.headers = {
                'Authorization': f'Bearer {self.token}'
            }
        else:
            print('No token received!!!')
        pass

    def get_balancing_authority(self, latitude, longitude):
        req = requests.get(f'https://api2.watttime.org/v2/ba-from-loc/?latitude={latitude}&longitude={longitude}',
                           headers=self.headers)

        data = req.json()
        print(data)
        balancing_authority = data.get('abbrev')

        if balancing_authority:
            print(f'Setting balancing_authority: {balancing_authority}')
            self.balancing_authority = balancing_authority
        else:
            print('No balancing authority found!!!')
        pass

    def get_realtime_emissions(self, style='all', **kwargs):

        # Potentially being passed in by user as parameters
        latitude = kwargs.get('latitude')
        longitude = kwargs.get('longitude')
        ba = kwargs.get('ba')

        if ba:
            if self.balancing_authority and self.balancing_authority != ba:
                print(
                    f'WARNING: existing {self.balancing_authority} being overwritten to {ba} because it is being explicitly passed into the function.')
            self.balancing_authority = ba

        elif latitude and longitude:
            print(f'No balancing authority passed, getting data for\n    latitude={latitude}\n    longitude={longitude}')
            # Setting self.balancing_authority
            self.get_balancing_authority(latitude, longitude)

        if not self.balancing_authority:
            print("Please pass either a balancing authority (as ba) OR latitude & longitude into the function")
            return None

        print(f'Getting data for balancing authority: {self.balancing_authority}')
        req_url = f'https://api2.watttime.org/v2/index/?ba={self.balancing_authority}&style={style}'
        print(f"URL requested = {req_url}")
        req = requests.get(req_url, headers=self.headers)
        data = req.json()
        print(data)
        return data

    def register(self, email, organization):
        values = f"""
                  {{
                    "username": "{self.username}",
                    "password": "{self.password}",
                    "email": "{email}",
                    "org": "{organization}"
                  }}
                """

        headers = {
            'Content-Type': 'application/json'
        }

        print('Registering...')
        req = requests.post(url='https://api2.watttime.org/v2/register',
                            data=values, headers=headers)
        print(req.json())
        pass


    def reset_password(self):
        req = requests.get(f'https://api2.watttime.org/v2/password/?username={self.username}')
        print(req.json())
