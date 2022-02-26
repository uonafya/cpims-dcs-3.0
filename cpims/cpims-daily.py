#!/usr/bin/python3.6

# /home/nmugaya/Projects/2019/Staging/Live/cpims/cpims
# Every Day at 6:15 am
# 15 6 * * * cd lnk && python3.7 cpims-daily.py >> ~/cpims-daily.log 2>&1

from notify import notices


def process_notificaction(report_name):
    """Method to process notification."""
    try:
        notices(report_name)
    except Exception as e:
        raise e
    else:
        pass


if __name__ == '__main__':
    process_notificaction('daily')
