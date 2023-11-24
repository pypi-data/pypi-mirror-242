from ..SunProvider import SunProvider
from astral.sun import sun as calc_sun
from astral import LocationInfo


class AstralProvider(SunProvider):
    def calc_sun(self, latitude, longitude, date):
        location = LocationInfo(latitude=latitude, longitude=longitude)
        location.timezone = "UTC"
        return calc_sun(location.observer, date=date)
