from smsframework import IProvider, OutgoingMessage
import boto3

from . import error
from botocore.exceptions import BotoCoreError, ClientError


class AmazonSNSProvider(IProvider):
    """ Amazon SNS provider """

    def __init__(self, gateway, name, access_key, secret_access_key, region_name):
        """ Configure Amazon SNS provider

            :param access_key: AWS access key id
            :param secret_access_key: AWS secret access key
            :param region_name: AWS region name
        """
        self._client = boto3.client(
            "sns",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_access_key,
            region_name=region_name
        )
        super(AmazonSNSProvider, self).__init__(gateway, name)

    def send(self, message):
        """ Send a message

            :type message: OutgoingMessage
            :rtype: OutgoingMessage
            """
        # Parameters
        params = {}

        #if message.src:
        #if message.provider_options.allow_reply:
        #if message.provider_options.status_report:
        #if message.provider_options.expires:)
        if message.provider_options.senderId:
            params['AWS.SNS.SMS.SenderID'] = {'DataType': 'String', 'StringValue': message.provider_options.senderId}
        if message.provider_options.escalate:
            params['AWS.SNS.SMS.SMSType'] = {'DataType': 'String', 'StringValue': 'Transactional'}

        if 'MaxPrice' in message.provider_params:
            params['AWS.SNS.SMS.MaxPrice'] = {'DataType': 'Number', 'StringValue': str(message.provider_params.pop('MaxPrice'))}
        params.update(message.provider_params)

        # Send
        try:
            res = self._client.publish(
                PhoneNumber='+' + message.dst,
                Message=message.body,
                MessageAttributes=params
            )
            message.msgid = res['MessageId']
            return message
        except BotoCoreError as e:
            raise error.AmazonSNSProviderError(e.__class__.__name__, str(e))
        except ClientError as e:
            raise error.AmazonSNSProviderError(e.response['Error']['Code'], str(e))


    def make_receiver_blueprint(self):
        """ Create the receiver blueprint

            We do it in a function as the SmsFramework user might not want receivers, consequently, has no reasons
            for installing Flask
        """
        raise NotImplementedError()
        from . import receiver
        return receiver.bp

    #region Public

    def get_client(self):
        """ Get AWS Client

        :return: botocore.client.BaseClient
        """
        return self._client

    #endregion
