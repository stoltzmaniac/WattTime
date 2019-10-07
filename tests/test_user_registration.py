from watttime.api import WattTime


def test_register_existing_user():
    w = WattTime('user', 'password')
    reg = w.register(email='user@organization.com', organization='organization')
    err = reg.get('error')

    if not err:
        raise('No error found during registration')

    assert(err == 'That username is taken. Please choose another.')


def test_reset_password():
    w = WattTime('user', 'password')
    res = w.reset_password()

    ok = res.get('ok')

    if not ok:
        raise ('No ok found during registration')

    assert (ok == 'Please check your email for the password reset link')


def test_get_token():
    w = WattTime('user', 'password')

    if w.token:
        raise('Already started with token, need to reinstantiate object')

    data = w.get_token()

    if not w.token:
        raise('No token returned')

    assert(len(w.token) > 50)
