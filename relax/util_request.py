from datetime import date, datetime
from time import sleep, strptime, mktime
from random import randint, choice
from ssl import create_default_context, CERT_NONE
from urllib import request


def get_header():
    first_num = randint(55, 76)
    third_num = randint(0, 3800)
    fourth_num = randint(0, 140)
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_14_5)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(
        first_num, third_num, fourth_num)

    ua = ' '.join(['Mozilla/5.0', choice(os_type), 'AppleWebKit/537.36',
                   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                  )
    return ua


def get_current_date(urls: list, retry=3):
    context = create_default_context()
    context.check_hostname = False
    context.verify_mode = CERT_NONE
    while retry > 0:
        try:
            for i in urls:
                req: request.Request = request.Request(url=i, headers={
                    'User-Agent': get_header(),
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Pragma': 'no-cache',
                    'Expires': '0'
                },)
                resp = request.urlopen(req,
                                       context=context)
                if resp.status == 200:
                    ts = resp.headers["date"]
                    time_array = strptime(ts[5:25], "%d %b %Y %H:%M:%S")
                    stamp = mktime(time_array) + 8 * 60 * 60
                    return datetime.fromtimestamp(stamp).date()
        except Exception as e:
            print(e, retry)
            retry -= 1
            sleep(0.5)
    else:
        return None
