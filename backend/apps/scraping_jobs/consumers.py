# Python Imports
import json
from typing import TypedDict, Literal, Optional

# Third-Party Imports
from channels.generic.websocket import AsyncWebsocketConsumer

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


class ScrapingJoStatusWebsocketConsumer(AsyncWebsocketConsumer):

    async def connect(self) -> None:
        job_id = self.scope["url_route"].kwargs["job_id"]
        self.room_group_name = f"job_{job_id}"
        self.job_id = job_id

        job = await ScrapingJob.objects.get_job_by_id(job_id)

        if not job:
            await self.disconnect(code=4001)
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        event_data: ScrapingJoStatus = {
            "type": "connection",
            "message": f"Connected to Job ({job.id}) real time status updates",
        }
        await self.send(text_data=json.dumps(event_data))

    async def disconnect(self):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def job_update(self, event: ScrapingJoStatus):
        event_data: ScrapingJoStatus = {
            "type": "job_status_update",
            "data": {"job_id": self.job_id, "status": event["data"]["status"]},
        }
        await self.send(json.dumps(event_data))
