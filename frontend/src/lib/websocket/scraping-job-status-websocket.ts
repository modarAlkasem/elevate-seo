import { getSession } from "next-auth/react";

interface ScrapingJoStatusData {
  job_id: string;
  status: ScrapingJobStatus;
}

export interface ScrapingJobStatusUpdateEventPayload {
  type: "job_status_update" | "connection";
  data?: ScrapingJoStatusData;
  message?: string;
}

export interface ScrapingJobStatusWSCallback {
  (data: ScrapingJobStatusUpdateEventPayload): void | Promise<void>;
}

export class ScrapingJobStatusWebSocket {
  private ws: WebSocket | null = null;
  private reconnectAttempts: number = 0;
  private maxReconnectAttempts: number = 5;
  private reconnectDelay: number = 2000;
  private callbacks: ScrapingJobStatusWSCallback[] = [];

  public connect = async (): Promise<void> =>
    new Promise(async (resolve, reject) => {
      const session = await getSession();

      const webSocketUrl = `${process.env.NEXT_PUBLIC_BASE_WEBSOCKET_URL}/scraping-jobs/status/?token=${session?.access}`;

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

          this.callbacks.forEach(async (cb) => await cb(data));
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

  public onJobsStatusUpdate = (
    callback: ScrapingJobStatusWSCallback
  ): (() => void) => {
    this.callbacks.push(callback);

    return () => {
      this.callbacks = this.callbacks.filter((cb) => cb !== callback);
    };
  };

  public disconnect = () => {
    if (this.ws) this.ws.close(1000, "Client disconnected");
  };
  public isConnected = () =>
    this.ws !== null && this.ws.readyState === WebSocket.OPEN;
}
