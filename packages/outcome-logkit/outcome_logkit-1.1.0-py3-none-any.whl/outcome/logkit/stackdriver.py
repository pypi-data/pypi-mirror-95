"""Outputs Stackdriver-compliant JSON."""

from datetime import datetime
from typing import cast

import structlog
from outcome.logkit.types import EventDict


class StackdriverRenderer(structlog.processors.JSONRenderer):
    def __call__(self, logger: object, name: str, event_dict: EventDict):
        return super().__call__(logger, name, self.format_for_stackdriver(event_dict))

    @classmethod
    def format_for_stackdriver(cls, event_dict: EventDict):
        level = event_dict.pop('level', None)
        if level:
            event_dict['severity'] = level

        event = event_dict.pop('event', None)
        if event:
            event_dict['message'] = event
        else:
            event_dict['message'] = ''

        timestamp = event_dict.pop('timestamp', None)
        if timestamp:
            try:
                ts = datetime.fromtimestamp(cast(float, timestamp)).isoformat('T')
                timestamp_str = f'{ts}Z'
            except Exception:
                timestamp_str = timestamp
        else:
            ts = datetime.now().isoformat('T')
            timestamp_str = f'{ts}Z'

        event_dict['timestamp'] = timestamp_str

        return event_dict
