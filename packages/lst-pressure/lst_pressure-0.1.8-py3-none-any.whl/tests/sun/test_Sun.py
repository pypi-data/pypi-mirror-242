import pytest
from lstpressure.sun import Sun
from lstpressure.sun.sun_providers import MeerKATProvider as MeerKATProvider

latitude, longitude = ["-30:42:39.8", "21:26:38.0"]

# NOTE - all times are in UTC

data = [
    (
        "20231121",
        {
            "astral_provider": {
                "dawn": "2023-11-21 02:59:16.055392",
                "sunrise": "2023-11-21 03:26:25.080197",
                "noon": "2023-11-21 10:19:52.000000",
                "sunset": "2023-11-21 17:13:54.229446",
                "dusk": "2023-11-21 17:41:06.904472",
            },
            "meerkat_provider": {
                "dawn": None,
                "sunrise": "2023-11-21 03:29:00.000000",
                "noon": None,
                "sunset": "2023-11-21 17:06:00.000000",
                "dusk": None,
            },
        },
    ),
    (
        "20230615",
        {
            "astral_provider": {
                "dawn": "2023-06-15 05:02:41.873453",
                "sunrise": "2023-06-15 05:29:46.909659",
                "noon": "2023-06-15 10:34:34.000000",
                "sunset": "2023-06-15 15:39:30.356171",
                "dusk": "2023-06-15 16:06:35.427817",
            },
            "meerkat_provider": {
                "dawn": None,
                "sunrise": "2023-06-15 05:32:00.000000",
                "noon": None,
                "sunset": "2023-06-15 15:32:00.000000",
                "dusk": None,
            },
        },
    ),
]


@pytest.mark.parametrize(
    "yyyymmdd, expected_results",
    data,
)
def test_Sun(yyyymmdd, expected_results):
    sun = Sun(yyyymmdd, latitude, longitude)

    for event, expected_time in expected_results["astral_provider"].items():
        calculated_time = getattr(sun, event).strftime("%Y-%m-%d %H:%M:%S.%f")
        assert calculated_time == expected_time


@pytest.mark.parametrize(
    "yyyymmdd, expected_results",
    data,
)
def test_Sun_with_MeerKATProvider(yyyymmdd, expected_results):
    sun = Sun(yyyymmdd=yyyymmdd, provider=MeerKATProvider())

    for event, expected_time in expected_results["meerkat_provider"].items():
        try:
            calculated_time = getattr(sun, event).strftime("%Y-%m-%d %H:%M:%S.%f")
        except AttributeError:
            calculated_time = None
        assert calculated_time == expected_time
