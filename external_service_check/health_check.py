from datetime import datetime, timedelta

import requests
import json



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
        'status': 'OK' if res['status'] == 'ok' else 'WARRING',
    }


def gsuite_status():
    res = json.loads(requests.get('https://www.google.com/appsstatus/json/ko').text[16:-2])

    t = datetime.now()

    result = {
        'name': 'G Suite',
        'update_time': str(t.replace(microsecond=0)),
        'status': 'OK',
    }
    for msg in res['messages']:
        err_t = datetime.fromtimestamp(msg['time'] / 1000)
        if err_t.date() == t.date():
            result['status'] = 'WARRING'
            result['update_time'] = str(err_t)

    return result


def color(status):
    if status == 'OK':
        return '#0097FF'
    else:
        return '#E80E0E'


def slack_msg(check):
    url = ''

    data = {
        "attachments": [
            {
                "color": color(check['status']),
                "fields": [
                    {
                        "title": f"{check['name']} 상태 체크",
                        "short": False
                    }
                ],
                "footer": f"업데이트 날짜: {check['update_time']}"
            }
        ]
    }

    headers = {
        'Content-type': 'application/json'
    }

    r = requests.post(url, data=json.dumps(data), headers=headers)


def main():
    SLACK_PUSH = True

    check_list = [ github_check() , slack_check(), gsuite_status() ]

    for check in check_list:
        slack_msg(check) if SLACK_PUSH else print(check)




if __name__ == '__main__':
    main()