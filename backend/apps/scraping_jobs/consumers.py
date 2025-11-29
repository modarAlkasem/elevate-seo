# Python Imports
import json
from typing import TypedDict, Literal, Optional

# Third-Party Imports
from channels.generic.websocket import AsyncWebsocketConsumer

# Project Imports
from authentication.models import User

# App Imports
from .models import ScrapingJob
from .constants import ScrapingJobStatusChoices


class ScrapingJoStatusData(TypedDict):
    job_id: str
    status: Literal[*ScrapingJobStatusChoices.values]


class ScrapingJoStatus(TypedDict):
    type: Literal["connection", "job_status_update"]
    data: Optional[ScrapingJoStatusData]
    message: Optional[str]


class ScrapingJobsStatusWebsocketConsumer(AsyncWebsocketConsumer):

    async def connect(self) -> None:
        user: User = self.scope["user"]
        self.room_group_name = f"user_{user.id}_jobs_status"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        event_data: ScrapingJoStatus = {
            "type": "connection",
            "message": f"Connected to Scraping Jobs Status WebSocket for user {user.id}",
        }
        await self.send(text_data=json.dumps(event_data))

    async def disconnect(self):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def job_update(self, event: ScrapingJoStatus):
        event_data: ScrapingJoStatus = {
            "type": "job_status_update",
            "data": {
                "job_id": event["data"]["job_id"],
                "status": event["data"]["status"],
            },
        }
        await self.send(json.dumps(event_data))
