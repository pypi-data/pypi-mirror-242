from copy import deepcopy

from importlib import import_module

from ordotools.tools.feast import Feast

from ordotools.tools.helpers import LiturgicalYearMarks
from ordotools.tools.helpers import days
from ordotools.tools.helpers import ladys_office
from ordotools.tools.helpers import leap_year

from ordotools.tools.liturgical_dates import integer_to_roman

from ordotools.tools.temporal import Temporal

from ordotools.sanctoral.diocese.roman import Sanctoral

import logging
from logging import debug
# from logging import info

logging.basicConfig(level=logging.DEBUG)


class LiturgicalCalendar:

    def __init__(self, year, diocese, country=""):
        self.year = year
        self.diocese = diocese
        self.transfers = None
        self.temporal = Temporal(self.year).return_temporal()
        self.FIRST_ADVENT = LiturgicalYearMarks(self.year).first_advent
        self.LAST_ADVENT = LiturgicalYearMarks(self.year).last_advent
        self.LENT_BEGINS = LiturgicalYearMarks(self.year).lent_begins
        self.LENT_ENDS = LiturgicalYearMarks(self.year).lent_ends

    def expand_octaves(self, feast: Feast) -> dict:
        """
        Generates (or expands) the octave for a feast.
        """
        octave = {}
        day = 1
        while day < 9:
            intro = f"De {integer_to_roman(day)} die"
            if day == 1: # TODO: get rid of the first 'if'
                pass
            if day == 8:
                feast.name = feast.infra_octave_name
            else:
                feast.name = f"{intro} infra {feast.infra_octave_name}"
            feast.fasting = False
            feast.rank_v = "feria"
            feast.rank_n = 18 if day < 6 else 13 # for common octaves
            octave |= {feast.date+days(day-1): feast.updated_properties}
            day += 1
        return octave

    def find_octave(self, year: dict) -> dict:
        """
        Finds the octaves of the sanctoral cycle and adds them to the year.
        """
        y = year.copy()
        # there might be a faster way of doing this
        temporals = []
        for feast in self.temporal.values():
            temporals.append(feast["feast"])
        for candidate in y.values():
            if candidate.name in temporals:
                # all of the octaves of the temporal cycle are already expanded
                continue
            elif candidate.octave is True:
                octave = self.expand_octaves(deepcopy(candidate))
                y |= self.add_feasts(master=y, addition=octave)
        return y

    def commemoration(self, feast: Feast, com: Feast) -> Feast:
        feast.com.insert(0, com.feast_properties)
        return feast

    def rank_by_nobility(self, feast_1: Feast, feast_2: Feast) -> dict:
        for x in range(6):
            if feast_1.nobility[x] < feast_2.nobility[x]:
                return {'higher': feast_1, 'lower': feast_2}
            elif feast_1.nobility[x] > feast_2.nobility[x]:
                return {'higher': feast_2, 'lower': feast_1}
            else:
                pass
        return {'higher': feast_1, 'lower': feast_2}

    def rank(self, dynamic: Feast, static: Feast) -> Feast:
        """
        Ranks feasts that occur on the same date. Send feasts that can be
        transferred to the transfer dictionary. "Dynamic" is from the sanctoral
        cycle, and "static" is from the temporal cycle.
        """
        # if the feasts are the same rank:
        if dynamic.rank_n == static.rank_n:
            # it is possible that the lower can be the
            # commemoration of the higher...
            return self.rank_by_nobility(
                    dynamic,
                    static
                )['higher']
        else:
            candidates = {
                dynamic.rank_n: dynamic,
                static.rank_n: static,
            }
            higher = candidates[sorted(candidates)[0]]
            lower = candidates[sorted(candidates)[1]]
            if lower.rank_n == 22:
                pass
            if lower.rank_n == 19:  # lent
                return self.commemoration(
                        feast=higher,
                        com=lower
                    )

            # feasts that do not take a commemoration
            if higher.rank_n <= 4:
                # lower feast is transferred
                if lower.rank_n == 3:  # holy week ferias, etc.
                    self.transfers == higher
                    return lower
                if lower.rank_n <= 10:
                    if lower.fasting is True:
                        higher.fasting = True
                    if lower != self.transfers:
                        self.transfers = lower
                    return higher
                else:
                    # lower feast is ignored
                    if lower.fasting is True:
                        higher.fasting = True
                    return higher

            # impeded DM, D and SD
            elif 14 <= lower.rank_n <= 16:
                return self.commemoration(
                        feast=higher,
                        com=lower
                    )
            else:
                return self.commemoration(
                        feast=higher,
                        com=lower
                    )

    def transfer_feast(self, feast: Feast) -> None:
        """
        Checks for feasts in the transfer dictionary.
        """
        return self.rank(dynamic=self.transfers, static=feast)

    def add_feasts(self, master: dict, addition: dict) -> dict:
        """
        Adds additional feasts to the master feast dictionary;
        Sends the feasts that confilict to the ranking algorithm.
        """
        calendar = master.copy()
        for date, data in calendar.items():
            if date in addition:
                if type(data) is Feast:
                    data = data.updated_properties
                feast = self.rank(
                    dynamic=Feast(date, addition[date]),
                    static=Feast(date, data)
                )
            else:
                if type(data) is Feast:
                    data = data.updated_properties
                feast = Feast(date, data)
            if self.transfers is not None:
                result = self.transfer_feast(
                    Feast(date, feast.updated_properties)
                )
                if result.feast == feast.feast:
                    pass
                else:
                    self.transfers = None
                    feast = result
            try:
                calendar |= {date: feast}
            except TypeError:
                pass
        return calendar

    def our_ladys_saturday(self, calendar: dict) -> None:
        """
        Adds Office of the BVM to the compiled calendar.
        """
        # TODO: add Mass number according to season
        year = calendar.copy()
        office = ladys_office
        for feast in year.keys():
            if feast.strftime("%w") == str(6):
                if self.LENT_BEGINS.date() <= feast.date() <= self.LENT_ENDS.date():
                    continue
                elif self.FIRST_ADVENT.date() <= feast.date() <= self.LAST_ADVENT.date():
                    continue
                else:
                    if year[feast].rank_n > 16:  # not a double
                        year[feast] = Feast(feast, office)  # TODO: add commemorations
                    else:
                        continue
        return year

    def build(self) -> None:
        saints = Sanctoral(self.year)
        if self.diocese == 'roman':
            sanctoral = saints.data if leap_year(self.year) is False \
                else saints.leapyear()
        else:
            diocese = import_module(
                f"sanctoral.diocese.{self.diocese}",
            )
            sanctoral = diocese.Diocese(self.year).calendar()
        full_calendar = self.add_feasts(self.temporal, sanctoral).copy()
        full_calendar |= self.our_ladys_saturday(full_calendar)
        full_calendar |= self.find_octave(year=full_calendar)
        return list(full_calendar.values())
