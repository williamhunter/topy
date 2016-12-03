from __future__ import print_function


__all__ = ['Logger']

class Logger(object):

    verbose = True

    @classmethod
    def display(self, *message):
        if Logger.verbose:
            print(*message)

    @classmethod
    def thin_line(self):
        Logger.display('-' * 80)

    @classmethod
    def thick_line(self):
        Logger.display('=' * 80)

