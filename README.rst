`Build
Status <https://travis-ci.org/kolypto/py-smsframework-amazon-sns>`__
`Pythons <.travis.yml>`__

SMSframework Amazon SNS Provider
================================

`Amazon
SNS <https://docs.aws.amazon.com/sns/latest/dg/sns-mobile-phone-number-as-subscriber.html>`__
Provider for
`smsframework <https://pypi.python.org/pypi/smsframework/>`__.

In the Amazon Console, you can specify

Getting started:

1. Create an AWS account, if you don’t have one:
   https://aws.amazon.com/. You will have 100 messages you can send for
   free. You’ll need to give them your debit card, but it’s free.
2. Sign in to the AWS Management Console:
   https://console.aws.amazon.com/sns/v2/home, choose (or search for)
   “SNS” in the menu at the top.
3. Click “get started”
4. Choose your region (top right, small drop-down).

   Note: some regions do not support SMS messages; choose one that does.
   You’ll know it when you see “Text messaging (SMS)” in the left menu.

   Copy the region identifier from the URL:
   ``home?region=eu-west-1#/home`` -> ``eu-west-1``. You will use it
   with this library
5. In the left menu, choose “Text messaging (SMS)”, go to “Text
   messaging preferences”, and set it up.

   Here, you can specify whether you want low-cost messaging
   (“promotional”), or reliable delivery (“transactional”). These
   preferences take effect for every SMS message that you send from your
   account, but you can override some of them when you send an
   individual message.

   Also, specify your default SenderID.

6. Click at your login at the top, choose “My Security credentials”.
   Choose “Access keys”, click on the “Create new access key” button.
   These are the credentials you’re going to use with this library:
   ``Access Key ID`` and ``Secret Access Key``.

Installation
============

Install from pypi:

::

   $ pip install smsframework_amazon_sns

To receive SMS messages, you need to ensure that `Flask
microframework <http://flask.pocoo.org>`__ is also installed:

::

   $ pip install smsframework_amazon_sns[receiver]

Initialization
==============

.. code:: python

   from smsframework import Gateway
   from smsframework_amazon_sns import AmazonSNSProvider

   gateway = Gateway()
   gateway.add_provider('amazon', AmazonSNSProvider,
       access_key='AAABBB111222CCCDDDEE',
       secret_access_key='fOAPpu78gZ6/HSJKCHqFj0xOJIFDt9mKQjkR+XTt',
       region_name='eu-west-1',
   )

Config
------

Source: /smsframework_amazon_sns/provider.py

-  ``access_key: str``: AWS access key id
-  ``secret_access_key: str``: AWS secret access key
-  ``region_name: str``: AWS region name

Example
=======

.. code:: python

   from smsframework import OutgoingMessage

   # Send a regular, low-cose message (when the default message type is "promotional"
   gateway.send(OutgoingMessage('+19998887766', 'Test'))

   # escalate=True sends a 'transactional' message: Amazon will use reliable delivery
   gateway.send(OutgoingMessage('19998887766', 'Test').options(senderId='kolypto', escalate=True))

Supported Options
=================

-  ``.options(senderId='kolypto')``: Sets an alpha-numeric SenderID
-  ``.options(escalate=True)``: Amazon will optimize the delivery to
   achieve the highest reliability.

Provider-Specific Parameters
============================

Provider-specific sending params:

-  ``MaxPrice: float``: The maximum amount in USD that you are willing
   to spend to send the SMS message.

Example:

.. code:: python

   from smsframework import OutgoingMessage

   gateway.send(OutgoingMessage('+123', 'hi').params(MaxPrice=0.15))

Limitations
===========

Incoming messages are currently not supported.
