from ..SunProvider import SunProvider
from datetime import date, datetime, time
from .DateTimeUtils import DateTimeUtil
from .SolarSystemUtils import SolarSystem
from .AstroUtils import AstroUtil
from typing import Union
import json
import os


class MeerKATProvider(SunProvider):
    def calc_sun(self, date: date):
        date = datetime.combine(date, time(0))
        with open(os.path.join(os.path.dirname(__file__), "planets.json"), "r") as f:
            planets = json.load(f)

            jd = DateTimeUtil.jd(date)
            sun_pos = SolarSystem.sunpos(planets["Earth"], jd)
            sun_lst = calc_sun_rise_set(
                sun_pos["ra"], sun_pos["dec"], AstroUtil.MKAT_POSITION["latitude"], 0
            )

            set_utc = DateTimeUtil.lst2ut(
                sun_lst["lstSet"], AstroUtil.MKAT_POSITION["longitude"], date
            )
            rise_utc = DateTimeUtil.lst2ut(
                sun_lst["lstRise"], AstroUtil.MKAT_POSITION["longitude"], date
            )

            set_date = date.replace(hour=int(set_utc), minute=int((set_utc - int(set_utc)) * 60))
            rise_date = date.replace(
                hour=int(rise_utc), minute=int((rise_utc - int(rise_utc)) * 60)
            )

            return {
                "dawn": None,
                "dusk": None,
                "noon": None,
                "sunrise": rise_date,
                "sunrise_lst": sun_lst["lstRise"],
                "sunset": set_date,
                "sunset_lst": sun_lst["lstSet"],
            }


def calc_sun_rise_set(
    ra: Union[float, str],
    dec: Union[float, str],
    latitude: Union[float, str],
    thresh_hold: Union[float, str],
):
    cos_h = -(AstroUtil.sind(thresh_hold) + AstroUtil.sind(latitude) * AstroUtil.sind(dec)) / (
        AstroUtil.cosd(latitude) * AstroUtil.cosd(dec)
    )
    obj = {
        "never_up": False,
        "circumpolar": False,
        "lstRise": 0,
        "lstSet": 0,
    }
    ha = AstroUtil.acosd(cos_h) / 15.0
    ra_hours = ra / 15.0  # Convert RA to hours
    obj["lstRise"] = AstroUtil.rev24(ra_hours - ha)
    obj["lstSet"] = AstroUtil.rev24(ra_hours + ha)
    return obj
