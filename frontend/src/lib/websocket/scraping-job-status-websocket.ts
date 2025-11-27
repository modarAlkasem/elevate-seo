import { getSession } from "next-auth/react";

import { client as queryClient } from "@/wrappers/query-client-wrapper";
import { scrapingJobKeys } from "../query-keys";

interface ScrapingJoStatusData {
  job_id: string;
  status: ScrapingJobStatus;
}

interface ScrapingJobStatusUpdateEventPayload {
  type: "job_status_update";
  data: ScrapingJoStatusData;
  message?: string;
}

export class ScrapingJobStatusWebSocket {
  private ws: WebSocket | null = null;
  private reconnectAttempts: number = 0;
  private maxReconnectAttempts: number = 5;
  private reconnectDelay: number = 2000;

  public connect = async (): Promise<void> =>
    new Promise(async (resolve, reject) => {
      const session = await getSession();

      const webSocketUrl = `${process.env.NEXT_PUBLIC_BASE_WEBSOCKET_URL}/scraping-jobs/?token=${session?.access}`;

      this.ws = new WebSocket(webSocketUrl);

      this.ws.onopen = () => {
        console.log("Connected to WebSocket:", webSocketUrl);

        this.reconnectAttempts = 0;

        resolve();
      };

      this.ws.onmessage = (e: MessageEvent) => {
        try {
          const data: ScrapingJobStatusUpdateEventPayload = JSON.parse(e.data);

          console.log("📩 Received WebSocket message:", data);

          queryClient.setQueryData(
            scrapingJobKeys.list(),
            (oldJobs: ScrapingJob[]) => {
              if (!oldJobs) return oldJobs;

              return oldJobs.map((job) =>
                job.id === data.data.job_id
                  ? { ...job, status: data.data.status }
                  : job
              );
            }
          );
        } catch (error) {
          console.error("❌ Error parsing WebSocket message:", error);
        }
      };

      this.ws.onerror = (event: Event) => {
        console.error("❌ WebSocket error occurred:", event);
        reject();
      };

      this.ws.onclose = (event: CloseEvent) => {
        console.log(
          `🔌 ScrapingJobStatusWebSocket connection closed with code: ${event.code}`
        );

        if (
          event.code !== 1000 &&
          this.reconnectAttempts < this.maxReconnectAttempts
        ) {
          this.reconnectAttempts++;

          setTimeout(() => this.connect(), this.reconnectDelay);
        }
      };
    });

  public disconnect = () => {
    if (this.ws) this.ws.close(1000, "Client disconnected");
  };
  public isConnected = () =>
    this.ws !== null && this.ws.readyState === WebSocket.OPEN;
}
