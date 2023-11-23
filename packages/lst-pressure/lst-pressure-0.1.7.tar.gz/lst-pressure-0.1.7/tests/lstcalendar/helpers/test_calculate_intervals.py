import pytest
from lstpressure.lstcalendar.helpers.calculate_intervals import (
    calculate_intervals,
    normalize_interval,
)
from lstpressure.utils import normalize_yyyymmdd_to_datetime


@pytest.mark.parametrize(
    "start, end, expected",
    [
        (7, 13, (7, 13)),
        (22, 7, (22, 31)),
        (1, 6, (1, 6)),
        (18, 2, (18, 26)),
    ],
)
def test_normalize_interval(start, end, expected):
    result = normalize_interval(start, end)
    assert result == expected


@pytest.mark.parametrize(
    "latitude,longitude,today_dt",
    [
        ("-30:42:39.8", "21:26:38.0", "20231116"),
    ],
)
def test_calculate_intervals(latitude, longitude, today_dt):
    today = normalize_yyyymmdd_to_datetime(today_dt)
    intervals = calculate_intervals(latitude, longitude, today, None)
    # TODO - what to assert


# tomorrow sunrise 2023-11-17 03:28:07.876877+00:00
# tomorrow sunrset 2023-11-17 17:10:25.684388+00:00

# tomorrow sunrise 2023-11-17 03:28:07.876877+00:00
# tomorrow sunrset 2023-11-17 17:10:25.684388+00:00
