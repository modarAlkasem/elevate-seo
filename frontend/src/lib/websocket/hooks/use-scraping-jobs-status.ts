import { useEffect, use } from "react";

import {
  type ScrapingJobStatusWSCallback,
  ScrapingJobStatusWebSocket,
} from "../scraping-job-status-websocket";

export const useScrapingJobsStatus = (cb: ScrapingJobStatusWSCallback) => {
  useEffect(() => {
    const ws = new ScrapingJobStatusWebSocket();

    use(ws.connect());

    const cleanupFN = ws.onJobsStatusUpdate(cb);

    return () => {
      cleanupFN();
      ws.disconnect();
    };
  }, []);
};
