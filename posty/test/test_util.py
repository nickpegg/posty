import pytest

from posty import util


def test_slugify_posty1():
    cases = (
        (
            'North Bay Area Bike Tour Log',
            'north_bay_area_bike_tour_log'
        ),
        (
            'Stupid Linux Trick # 1234   ',
            'stupid_linux_trick___1234'
        ),
    )

    for i, o in cases:
        assert util.slugify_posty1(i) == o
