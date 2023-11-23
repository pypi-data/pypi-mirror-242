from __future__ import annotations  # Not required from 3.11 onwards
import argparse
from typing import Type
from datetime import datetime
from conf import Conf
from lstpressure import LSTIntervalType as I, Observation, LST
from ..AppInterface import AppInterface

conf = Conf()

filter_mapping = {
    I.NIGHT.name: I.NIGHT,
    I.SUNRISE_SUNSET.name: I.SUNRISE_SUNSET,
    I.ALL_DAY.name: I.ALL_DAY,
    I.SUNSET_SUNRISE.name: I.SUNSET_SUNRISE,
    I.OBSERVATION_WINDOW.name: I.OBSERVATION_WINDOW,
}


class Observables(AppInterface):
    id = "observables"

    def build(self) -> Type[Observables]:
        app = self.parser.add_subparsers(
            description=argparse.SUPPRESS,
            dest="command",
            metavar="observables",
            help="Generate a list of observable events based on specified criteria",
        )

        parser = app.add_parser("observables", usage=argparse.SUPPRESS)
        parser.add_argument(
            "--start",
            type=str,
            default=datetime.today().strftime("%Y%m%d"),
            help="The start date in the format 'YYYYMMDD'",
        )

        parser.add_argument(
            "--end",
            type=str,
            required=False,
            default=None,
            help="The end date in the format 'YYYYMMDD'. If not provided, the start date is used.",
        )

        parser.add_argument("--input", required=True, type=str, help="Path to the OPT csv file")

        parser.add_argument("--output", type=str, help="Path to the output csv file")

        parser.add_argument(
            "--filter",
            type=str,
            required=False,
            help="Select from: NIGHT, SUNRISE_SUNSET, ALL_DAY, SUNSET_SUNRISE, OBSERVATION_WINDOW",
        )

        parser.add_argument(
            "--lat",
            metavar="D:M:S",
            default=None,
            nargs="?",
            type=str,
            help="The latitude for the observation in the format 'D:M:S'. Default is '-30:42:39.8'. Use as follows --lat=location",
        )

        parser.add_argument(
            "--long",
            metavar="D:M:S",
            default=None,
            nargs="?",
            type=str,
            help="The longitude for the observation in the format 'D:M:S'. Default is '21:26:38.0'. Use as follows --long=location",
        )

        return self

    def parse(self, args) -> Type[Observables]:
        if args.lat and args.lat != "":
            conf.LATITUDE = args.lat
        if args.long and args.long != "":
            conf.LONGITUDE = args.long
        self.input = args.input
        self.start = args.start
        self.end = args.end if args.end else self.start
        self.filter_value = filter_mapping.get(args.filter, None)
        self.output = args.output if args.output else None
        return self

    def exe(self) -> Type[Observables]:
        def observation_filter(observation: Observation):
            if self.filter_value in observation.utc_constraints:
                return True
            return False

        if self.output:
            LST(
                self.input,
                calendar_start=self.start,
                calendar_end=self.end,
                observation_filter=observation_filter if self.filter_value else None,
                latitude=conf.LATITUDE,
                longitude=conf.LONGITUDE,
            ).to_csv_file(self.output)

        else:
            print(
                LST(
                    self.input,
                    calendar_start=self.start,
                    calendar_end=self.end,
                    observation_filter=observation_filter if self.filter_value else None,
                    latitude=conf.LATITUDE,
                    longitude=conf.LONGITUDE,
                ).to_csv_string()
            )
        return self
