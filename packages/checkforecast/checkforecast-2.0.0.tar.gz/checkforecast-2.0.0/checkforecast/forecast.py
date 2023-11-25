import requests


class Weather:
    """
    Creats a weather object getting an api as input
    and either a city name or lat and lon coordinates.

    package use example:

    # Creats a weather object using city name.
    # Get your own Api key from https://openweathermap.org
    # And wait for a couple of hours for the key to be activated.

    >>> weather1 = Weather(apikey="Your_Key", city="Madrid")

    # using lat and lon coordinates(*please enter actual coordinates)
    >>> weather2 = Weather(api_key="Your_key", lat=41.1, lon=-4.1)

    # Get complete whether data for next 12 hours:
    >>> weather1.next_12h()

    # simplified data for next 12 hours:
    >>> weather1.next_12h_simplefied()

    # Sample url to get the sky condition icons:
    https://openweathermap.org/img/wn/10d@2x.png

    """

    def __init__(self, city=None, lat=None, lon=None, api_key=None):

        if city:
            url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}," \
                  f"&appid={api_key}&units=imperial"
            data = requests.get(url)
            self.data = data.json()
            # https://api.openweathermap.org/data/2.5/forecast?lat=44.34&lon=10.99&APPID=e819f50f2bafbf62d45eed894f79f905&units=imperial
        elif lat and lon:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon},&APPID={api_key}&units=imperial"

            data = requests.get(url)

            self.data = data.json()


        else:
            raise TypeError("Provide either a city or lat and lon argument")

        if self.data['cod'] != "200":
            # displays error message
            raise ValueError(self.data['message'])

    def next_12h(self):
        """ Returns 3 - hour data for next 12 hours as a dict """
        return self.data['list'][:4]

    def next_12h_simplefied(self):
        """ Returns date temp and sky condition of 3 hours for next 12 hours as a touple"""
        data = []
        for dict in self.data['list'][:4]:
            data.append((dict['dt_txt'], dict['main']['temp'],
                         dict['weather'][0]['description'], dict['weather'][0]['icon']),)
        return data

