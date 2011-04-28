class LocalWorker(object):
    """ Dummy worker for local immediate execution """
    def proceed(self, postponed, callback):
        callback(postponed._proceed())

