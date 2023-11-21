import requests

class ElectricityMap:
    def __init__(self, token):
        self.token = token

    def _get_headers(self):
        return {
            'auth-token': self.token
        }

    def get_health(self):
        '''
        Returns true if the health of electricitymap seems to be ok, otherwise false
        '''
        url = 'https://api.electricitymap.org/health'
        response = requests.get(url, headers=self._get_headers())
        return response.json()['status'] == 'ok'


    def get_zones(self):
        '''
        Returns an object with all the zones that are supported
        '''
        url = "https://api-access.electricitymaps.com/free-tier/zones"
        response = requests.get(url, headers=self._get_headers())
        return response.json()

    def get_carbon_intensity(self, zone=None, lat=None, lon=None):
        '''
        Returns the carbon intensity for a given zone or lat/lon
        '''

        if not zone and not lat and not lon:
            raise ValueError('You need at least zone or lat/long')

        url = 'https://api-access.electricitymaps.com/free-tier/carbon-intensity/latest?'

        if zone:
            url += f"zone={zone}"
        else:
            url += f"lat={lat}&lon={lon}"

        response = requests.get(url, headers=self._get_headers())
        return response.json()


    def get_power_production(self, zone=None, lat=None, lon=None):
        '''
        Returns the carbon intensity for a given zone or lat/lon
        '''

        if not zone and not lat and not lon:
            raise ValueError('You need at least zone or lat/long')

        url = 'https://api-access.electricitymaps.com/free-tier/power-breakdown/latest?'

        if zone:
            url += f"zone={zone}"
        else:
            url += f"lat={lat}&lon={lon}"

        response = requests.get(url, headers=self._get_headers())
        return response.json()

