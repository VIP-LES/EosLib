import time


def spin(spinterval: int = 10) -> None:
    """ Loops forever.
    :param spinterval: number of seconds to sleep between wakeups
    """
    while True:
        time.sleep(spinterval)
