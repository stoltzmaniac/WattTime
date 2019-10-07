from watttime.api import WattTime


def test_list_balancing_authorities():
    w = WattTime('user', 'password')
    bas = w.list_balancing_authorities()
    expected = ['AEC', 'AECI', 'AESO', 'AVA', 'AZPS', 'BANC', 'BCTC',
                   'BPAT', 'CISO', 'CFE', 'CHPD', 'CISO', 'CPLE', 'CPLW',
                   'DEAA', 'DOPD', 'DUK', 'EEI', 'EPE', 'ERCO', 'FMPP',
                   'FPC', 'FPL', 'GCPD', 'GRID', 'GRIF', 'GRMA', 'GVL',
                   'GWA', 'HGMA', 'HQT', 'HST', 'IESO', 'IID', 'IPCO',
                   'ISNE', 'JEA', 'LDWP', 'LGEE', 'MHEB', 'MISO', 'NBSO',
                   'NEVP', 'NSB', 'NWMT', 'NYIS', 'OVEC', 'PACE', 'PACW',
                   'PGE', 'PJM', 'PNM', 'PSCO', 'PSEI', 'SC', 'SCEG',
                   'SCL', 'SEC', 'SEPA', 'SOCO', 'SPA', 'SPC', 'SRP',
                   'SWPP', 'TAL', 'TEC', 'TEPC', 'TIDC', 'TPWR', 'TVA',
                   'WACM', 'WALC', 'WAUW', 'WWA', 'YAD']
    assert(bas == expected)


def test_get_balancing_authority():
    w = WattTime('user', 'password')
    data = w.get_balancing_authority(latitude=37.871667, longitude=-122.272778)
    ba = data.get('balancing_authority')

    if not ba:
        raise('No balancing authority')

    assert(ba == 'CAISO_NP15')


