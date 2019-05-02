import requests


from datetime import datetime, timedelta


def github_check():
    res = requests.get('https://kctbh9vrtdwd.statuspage.io/api/v2/status.json').json()
    return {
        'name': 'GitHub',
        'update_time': str(datetime.strptime(res['page']['updated_at'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(microsecond=0)
                           + timedelta(hours=9)),
        'status': 'OK' if res['status']['indicator'] == 'none' else 'WARRING',
    }


def slack_check():
    res = requests.get('https://status.slack.com/api/current').json()
    return {
        'name': 'Slack',
        'update_time': str(datetime.strptime(res['date_created'][:-6], '%Y-%m-%dT%H:%M:%S') + timedelta(hours=17)),
        'status': res['status']
    }


def main():
    print(github_check())
    print(slack_check())


if __name__ == '__main__':
    main()