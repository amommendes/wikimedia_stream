from datetime import datetime, timedelta
import time


def get_mseconds():
    """
    This method returns actual time in milliseconds
    """
    return int(round(time.time()*1000))
