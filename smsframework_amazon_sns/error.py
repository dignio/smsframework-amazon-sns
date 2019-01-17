""" Amazon error codes """

from smsframework.exc import *


class AmazonSNSProviderError(ProviderError):
    """ Any error reported by Amazon SNS """

    def __init__(self, code, message=''):
        self.code = code
        super(AmazonSNSProviderError, self).__init__(
            '#{}: {}'.format(self.code, message)
        )
