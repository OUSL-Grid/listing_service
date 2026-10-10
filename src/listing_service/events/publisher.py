import json
import uuid
from datetime import datetime, timezone
from typing import Any

import nats
from nats.aio.client import Client as NATS

from listing_service.config import settings


class EventPublisher:
    """NATS event publisher for listing events."""

    def __init__(self):
        self._nc: NATS | None = None

    async def connect(self):
        """Connect to NATS server."""
        try:
            self._nc = await nats.connect(settings.nats_url)
            print(f"Connected to NATS at {settings.nats_url}")
        except Exception as e:
            print(f"WARNING: Could not connect to NATS: {e}")
            self._nc = None

    async def close(self):
        """Close NATS connection."""
        if self._nc:
            await self._nc.close()
            self._nc = None

    async def publish(self, subject: str, data: dict[str, Any]):
        """Publish an event with the standard envelope."""
        if not self._nc:
            print(f"WARNING: NATS not connected, skipping publish to {subject}")
            return

        envelope = {
            "event_id": str(uuid.uuid4()),
            "event_type": subject,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data,
        }
        await self._nc.publish(subject, json.dumps(envelope).encode())


# Singleton
event_publisher = EventPublisher()