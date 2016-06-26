from trfind.finders import ALL_FINDERS
from trfind.models import Peak


def main():
    peak = Peak('Mount Stuart', None, None)

    for finder in ALL_FINDERS:
        print finder(peak)