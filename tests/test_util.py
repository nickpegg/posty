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


def test_bucket():
    x = list(range(1, 6))

    result = util.bucket(x, 2)
    assert result == [[1, 2], [3, 4], [5]]

    result = util.bucket(x, 3)
    assert result == [[1, 2, 3], [4, 5]]

    result = util.bucket(x, 10)
    assert result == [x]
