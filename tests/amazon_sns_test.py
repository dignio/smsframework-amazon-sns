# -*- coding: utf-8 -*-

import unittest, logging

from flask import Flask

from smsframework import Gateway, OutgoingMessage
from smsframework_amazon_sns import AmazonSNSProvider

from botocore.stub import Stubber


class AmazonSNSProviderTest(unittest.TestCase):
    def setUp(self):
        # Gateway
        gw = self.gw = Gateway()
        gw.add_provider('main', AmazonSNSProvider,
                        access_key='A', secret_access_key='B', region_name='eu-west-1')

        # Flask
        app = self.app = Flask(__name__)

        # Register receivers
        gw.receiver_blueprints_register(app, prefix='/in-sms/')

        # botocore logging is too verbose; raise the level
        logging.getLogger('boto3').setLevel(logging.WARNING)
        logging.getLogger('botocore').setLevel(logging.WARNING)

    def _stubber(self):
        """ Get SNS stubber """
        client = self.gw.get_provider('main').get_client()
        stubber = Stubber(client)
        return stubber

    def test_send_message(self):
        """ Test outgoing message """
        # 1. Simple message
        with self._stubber() as st:
            st.add_response('publish',
                            expected_params={'PhoneNumber': '+1999', 'Message': 'test 1', 'MessageAttributes':{}},
                            service_response={'MessageId': '1'}
                            )
            self.assertEqual('1', self.gw.send(OutgoingMessage('+1999', 'test 1')).msgid)

        # 2. Transactional message
        with self._stubber() as st:
            # 2. Transactional message with SenderId
            st.add_response('publish',
                            expected_params={'PhoneNumber': '+1999', 'Message': 'test 2',
                                             'MessageAttributes': {
                                                 'AWS.SNS.SMS.SenderID': {'DataType': 'String', 'StringValue': 'kolypto'},
                                                 'AWS.SNS.SMS.SMSType': {'DataType': 'String', 'StringValue': 'Transactional'},
                                             }},
                            service_response={'MessageId': '2'}
                            )
            self.assertEqual('2', self.gw.send(OutgoingMessage('+1999', 'test 2').options(senderId='kolypto', escalate=True)).msgid)
