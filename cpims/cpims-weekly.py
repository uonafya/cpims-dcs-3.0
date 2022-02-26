#!/usr/bin/python3.7

# /home/nmugaya/Projects/2019/Staging/Live/cpims/cpims
# Every Monday at 6:30 am
# 30 6 * * 1 cd lnk && python3.7 cpims-weekly.py >> ~/cpims-weekly.log 2>&1


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
    process_notificaction('weekly')
