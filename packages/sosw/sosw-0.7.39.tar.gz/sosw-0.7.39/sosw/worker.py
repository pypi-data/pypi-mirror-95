"""
..  hidden-code-block:: text
    :label: View Licence Agreement <br>

    sosw - Serverless Orchestrator of Serverless Workers

    The MIT License (MIT)
    Copyright (C) 2021  sosw core contributors <info@sosw.app>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

__all__ = ['Worker']
__author__ = "Nikolay Grishchenko"
__version__ = "1.0"

import json
import logging

from sosw.app import Processor
from sosw.managers.meta_handler import MetaHandler
from typing import Dict


logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Worker(Processor):
    """
    We recommend that you inherit your core Processor from this class in Lambdas that are orchestrated by `sosw`.

    The ``__call__`` method is supposed to accept the ``event`` of the Lambda invocation.
    This is a dictionary with the payload received in the lambda_handler during invocation.

    Worker has all the common methods of :ref:`Processor` and tries to mark task as completed if received
    ``task_id`` in the ``event``. Worker create a payload with ``stats`` and ``result`` if exist and invoke worker
    assistant lambda.

    Worker class can optionally record ``'completed'`` and ``'failed'`` events to the DynamoDB tasks meta data table.
    In order to enable this feature, you have to provide ``'meta_handler_config'`` in your custom_config.
    You also need to grant write permissions for this table to your Lambda.

    You can find more information about the configuration in the :ref:`MetaHandler<meta_handler>` chapter.
    """

    DEFAULT_CONFIG = {
        'init_clients':                 ['lambda'],
        'sosw_worker_assistant_lambda': 'sosw_worker_assistant'
    }

    lambda_client = None
    meta_handler: MetaHandler = None


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        if 'meta_handler_config' in self.config:
            self.meta_handler = MetaHandler(custom_config=self.config['meta_handler_config'])


    def __call__(self, event: Dict):
        """
        You can either call super() at the end of your child function or completely overwrite this function.
        """

        # Mark the task as completed in DynamoDB if the event had task_id.
        try:
            if event.get('task_id'):
                self.mark_task_as_completed(event['task_id'])
        except Exception:
            logger.exception(f"Failed to call WorkerAssistant for event {event}")
            pass

        super().__call__(event)


    def mark_task_as_completed(self, task_id: str):
        """ Call worker assistant lambda and tell it to close task """

        if not self.lambda_client:
            self.register_clients(['lambda'])

        worker_assistant_lambda_name = self.config.get('sosw_worker_assistant_lambda', 'sosw_worker_assistant')
        payload = {
            'action':  'mark_task_as_completed',
            'task_id': task_id,
        }

        if self.stats:
            payload.update({'stats': self.stats})

        if self.result:
            payload.update({'result': self.result})

        payload = json.dumps(payload)

        lambda_response = self.lambda_client.invoke(
                FunctionName=worker_assistant_lambda_name,
                InvocationType='Event',
                Payload=payload
        )
        if self.meta_handler:
            self.meta_handler.post(task_id=task_id, action='completed')
        logger.debug(f"mark_task_as_completed response: {lambda_response}")


    def mark_task_as_failed(self, task_id: str):
        """ Call worker assistant lambda and tell it to update task info """

        if not self.lambda_client:
            self.register_clients(['lambda'])

        worker_assistant_lambda_name = self.config.get('sosw_worker_assistant_lambda', 'sosw_worker_assistant')
        payload = {
            'action':  'mark_task_as_failed',
            'task_id': task_id,
        }

        if self.stats:
            payload.update({'stats': self.stats})

        if self.result:
            payload.update({'result': self.result})

        payload = json.dumps(payload)

        lambda_response = self.lambda_client.invoke(
                FunctionName=worker_assistant_lambda_name,
                InvocationType='Event',
                Payload=payload
        )
        if self.meta_handler:
            self.meta_handler.post(task_id=task_id, action='failed')
        logger.debug(f"mark_task_as_failed response: {lambda_response}")
