import os
import uuid
from datetime import datetime
import json


class Event:
    def __init__(self, action: str, context = {}):
        self.action = action
        self.context = context
        self.pk = str(uuid.uuid4())
        self.env = os.environ.get('ENV', 'production')

    def fire(self) -> dict:
        event = {
            'action': self.action,
            'pk': self.pk,
            'env': self.env,
            'created_at': datetime.utcnow().isoformat(),
            'context': self.context,
        }
        print('streams-fire {}'.format(json.dumps(event)))
        return event