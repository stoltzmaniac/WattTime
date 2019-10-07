import requests
import base64
from json import JSONDecodeError


class WattTime:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.token = None
        self.headers = None
        self.balancing_authority = None

    def get_token(self, pass_thru=False):
        creds_raw = f"{self.username}:{self.password}".encode()
        creds_encoded = base64.b64encode(creds_raw).decode("utf-8")
        headers = {
            'Authorization': f'Basic {creds_encoded}'
        }

        req = requests.get('https://api2.watttime.org/v2/login/', headers=headers)
        data = req.json()

        self.token = data.get('token')
        if self.token:
            print(f"Token received, setting headers: {self.token}")
            self.headers = {
                'Authorization': f'Bearer {self.token}'
            }
        else:
            print('No token received, check username / password / api limit!!!')
            raise
        return self.token

    def submit_get_request(self, url):
        if self.token:
            req = requests.get(url, headers=self.headers)
            return req

        else:
            self.get_token()

        if self.token:
            req = requests.get(url, headers=self.headers)
            return req

        raise('Tried to get_token() and received nothing or error.')


    def get_balancing_authority(self, latitude: float, longitude: float):

        req = self.submit_get_request(f'https://api2.watttime.org/v2/ba-from-loc/?latitude={latitude}&longitude={longitude}')

        data = req.json()
        balancing_authority = data.get('abbrev')

        if balancing_authority:
            print(f'Setting balancing_authority: {balancing_authority}')
            self.balancing_authority = balancing_authority
        else:
            print('No balancing authority found!!!')
        return {'balancing_authority': balancing_authority}

    def handle_balancing_authority(self, **kwargs):

        # Potentially being passed in by user as parameters
        latitude = kwargs.get('latitude')
        longitude = kwargs.get('longitude')
        ba = kwargs.get('ba')

        if latitude and longitude and ba:
            raise('Error: please only pass latitude & longitude OR ba. Not all 3.')

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
            raise("Please pass either a balancing authority (as ba) OR latitude & longitude into the function")

        return True


    def get_realtime_emissions(self, style='all', **kwargs):

        # Potentially being passed in by user as parameters
        latitude = kwargs.get('latitude')
        longitude = kwargs.get('longitude')
        ba = kwargs.get('ba')

        kw_handling = self.handle_balancing_authority(latitude=latitude, longitude=longitude, ba=ba)

        if not kw_handling:
            raise('Error with kwarg handling, ensure these are appropriate')

        print(f'Getting data for balancing authority: {self.balancing_authority}')
        req_url = f'https://api2.watttime.org/v2/index/?ba={self.balancing_authority}&style={style}'
        print(f"URL requested = {req_url}")
        req = self.submit_get_request(req_url)
        data = req.json()
        print(data)
        return data

    def get_historical_emissions_zip(self, version='all', **kwargs):

        # Potentially being passed in by user as parameters
        ba = kwargs.get('ba')

        kw_handling = self.handle_balancing_authority(ba=ba)

        if not kw_handling:
            raise ('Error with kwarg handling, ensure these are appropriate')

        print(f'Getting data for balancing authority: {self.balancing_authority}')
        req_url = f'https://api2.watttime.org/v2/historical/?ba={self.balancing_authority}&version={version}'
        print(f"URL requested = {req_url}")
        req = self.submit_get_request(req_url)
        data = req.json()
        return data  # Not sure what this response looks like

    def get_detailed_grid_data(self, starttime, endtime, style='all', **kwargs):

        # Potentially being passed in by user as parameters
        latitude = kwargs.get('latitude')
        longitude = kwargs.get('longitude')
        ba = kwargs.get('ba')

        kw_handling = self.handle_balancing_authority(latitude=latitude, longitude=longitude, ba=ba)

        if not kw_handling:
            raise('Error with kwarg handling, ensure these are appropriate')

        if not starttime:
            raise('Pass starttime parameter')
        if not endtime:
            raise('Pass endtime parameter')

        print(f'Getting data for balancing authority: {self.balancing_authority}')
        req_url = f'https://api2.watttime.org/v2/data/?ba={ba}&starttime={starttime}&endtime={endtime}&style={style}'
        print(f"URL requested = {req_url}")
        req = self.submit_get_request(req_url)
        data = req.json()
        print(data)
        return data

    @staticmethod
    def list_balancing_authorities():
        ba_list = ['AEC', 'AECI', 'AESO', 'AVA', 'AZPS', 'BANC', 'BCTC',
                   'BPAT', 'CISO', 'CFE', 'CHPD', 'CISO', 'CPLE', 'CPLW',
                   'DEAA', 'DOPD', 'DUK', 'EEI', 'EPE', 'ERCO', 'FMPP',
                   'FPC', 'FPL', 'GCPD', 'GRID', 'GRIF', 'GRMA', 'GVL',
                   'GWA', 'HGMA', 'HQT', 'HST', 'IESO', 'IID', 'IPCO',
                   'ISNE', 'JEA', 'LDWP', 'LGEE', 'MHEB', 'MISO', 'NBSO',
                   'NEVP', 'NSB', 'NWMT', 'NYIS', 'OVEC', 'PACE', 'PACW',
                   'PGE', 'PJM', 'PNM', 'PSCO', 'PSEI', 'SC', 'SCEG',
                   'SCL', 'SEC', 'SEPA', 'SOCO', 'SPA', 'SPC', 'SRP',
                   'SWPP', 'TAL', 'TEC', 'TEPC', 'TIDC', 'TPWR', 'TVA',
                   'WACM', 'WALC', 'WAUW', 'WWA', 'YAD']
        return ba_list

    def register(self, email: str, organization: str):
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
        data = req.json()
        print(data)
        return data


    def reset_password(self):
        req = requests.get(f'https://api2.watttime.org/v2/password/?username={self.username}')
        data = req.json()
        print(data)
        return data

