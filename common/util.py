import datetime


def retrieve_time_from_timespan(timespan: datetime.timedelta):
    duration = str(timespan)
    return duration[:duration.find('.')]
