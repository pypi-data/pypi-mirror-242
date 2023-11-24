"""
lstpressure.sun.Sun
"""
from __future__ import annotations  # Not required from Python 3.11 onwards
from typing import Union, Optional
from .sun_providers import SunProvider, AstralProvider
from ..utils import normalize_coordinates, normalize_yyyymmdd_to_datetime, utc_to_lst


class Sun:
    """
    Sun statistics for a particular date, at a particular lat/long.

    Attributes
    ----------
    dawn : datetime
        The dawn time for the given date and location.
    dawn_lst : datetime
        The dawn time converted to Local Sidereal Time (LST) for the given date and location.
    sunrise : datetime
        The sunrise time for the given date and location.
    sunrise_lst : datetime
        The sunrise time converted to Local Sidereal Time (LST) for the given date and location.
    noon : datetime
        The solar noon time for the given date and location.
    noon_lst : datetime
        The solar noon time converted to Local Sidereal Time (LST) for the given date and location.
    sunset : datetime
        The sunset time for the given date and location.
    sunset_lst : datetime
        The sunset time converted to Local Sidereal Time (LST) for the given date and location.
    dusk : datetime
        The dusk time for the given date and location.
    dusk_lst : datetime
        The dusk time converted to Local Sidereal Time (LST) for the given date and location.

    Parameters
    ----------
    latitude : Union[float, str]
        The latitude of the location in decimal degrees or string format.
    longitude : Union[float, str]
        The longitude of the location in decimal degrees or string format.
    yyyymmdd : str
        The date in 'YYYYMMDD' format for which sun statistics are calculated.

    Raises
    ------
    ValueError
        If the date format is incorrect or if the location coordinates cannot be normalized.

    """

    def __init__(
        self,
        yyyymmdd: str,
        latitude: Optional[Union[float, str]] = None,
        longitude: Optional[Union[float, str]] = None,
        provider: Optional[SunProvider] = None,
    ) -> None:
        """
        Initialize a Sun object.

        Parameters
        ----------
        yyyymmdd : str
            The date in 'YYYYMMDD' format for which sun statistics are calculated.
        latitude : Optional[Union[float, str]]
            The latitude of the location in decimal degrees or string format. Defaults to None.
        longitude : Optional[Union[float, str]]
            The longitude of the location in decimal degrees or string format. Defaults to None.
        provider: Optional[Any]
            A sun/time provider for customizing class calculations. Defaults to None.

        Raises
        ------
        ValueError
            If the date format is incorrect or if the location coordinates cannot be normalized.
        """
        dt = normalize_yyyymmdd_to_datetime(yyyymmdd)
        self._provider = provider

        if latitude and longitude:
            latitude, longitude = normalize_coordinates(latitude, longitude)
        self._latitude = latitude
        self._longitude = longitude

        if provider:
            self._attributes = provider.calc_sun(dt)
        else:
            self._attributes = AstralProvider().calc_sun(
                latitude=latitude, longitude=longitude, date=dt
            )

    @property
    def provider(self) -> SunProvider:
        return self._provider

    def time(self, event, get_fallback=lambda: None):
        result = self._attributes.get(event, None)
        if not result:
            result = get_fallback()
        return result

    @property
    def dawn(self):
        return self.time("dawn")

    @property
    def dawn_lst(self):
        return self.time(
            "dawn_lst", lambda: utc_to_lst(self.time("dawn"), self._latitude, self._longitude)
        )

    @property
    def sunrise(self):
        return self.time("sunrise")

    @property
    def sunrise_lst(self):
        return self.time(
            "sunrise_lst", lambda: utc_to_lst(self.time("sunrise"), self._latitude, self._longitude)
        )

    @property
    def noon(self):
        return self.time("noon")

    @property
    def noon_lst(self):
        return self.time(
            "noon_lst", lambda: utc_to_lst(self.time("noon"), self._latitude, self._longitude)
        )

    @property
    def sunset(self):
        return self.time("sunset")

    @property
    def sunset_lst(self):
        return self.time(
            "sunset_lst", lambda: utc_to_lst(self.time("sunset"), self._latitude, self._longitude)
        )

    @property
    def dusk(self):
        return self.time("dusk")

    @property
    def dusk_lst(self):
        return self.time(
            "dusk_lst", lambda: utc_to_lst(self.time("dusk"), self._latitude, self._longitude)
        )
