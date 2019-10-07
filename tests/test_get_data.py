from watttime.api import WattTime


def test_get_realtime_emissions():
    w = WattTime('user', 'password')

    data = w.get_realtime_emissions(ba='MISO_MI')
    ba = data.get('ba')
    if not ba:
        raise('Error, no ba found, request may be broken')
    assert(ba == 'MISO_MI')

    data2 = w.get_realtime_emissions(latitude=37.871667, longitude=-122.272778)
    ba2 = data2.get('ba')
    if not ba2:
        raise('Error, no ba found, request may be broken')
    assert (ba2 == 'CAISO_NP15')

    try:
        ok = False
        data3 = w.get_realtime_emissions(latitude=37.871667, longitude=-122.272778, ba='MISO_MI')
    except TypeError as e:
        ok = True

    assert(ok)

def test_get_historical_emissions_zip():
    w = WattTime('user', 'password')
    data = w.get_historical_emissions_zip(ba='CAISO_NP15')

    err = data.get('error')

    if not err:
        raise('User is not unauthorized or None was not returned')

    assert(err == "Unauthorized")


def test_get_detailed_grid_data():
    w = WattTime('user', 'password')
    data = w.get_detailed_grid_data(starttime='2019-01-01', endtime='2019-01-10', ba='CAISO_ZP26')
    market = data[0].get('market')

    if not market:
        raise('Error: market not returned, check free tier for ba')

    assert(market == 'RTM')