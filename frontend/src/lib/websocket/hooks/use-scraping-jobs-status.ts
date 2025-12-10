import { useEffect } from "react";

import {
  type ScrapingJobStatusWSCallback,
  ScrapingJobStatusWebSocket,
} from "../scraping-job-status-websocket";

export const useScrapingJobsStatus = (cb: ScrapingJobStatusWSCallback) => {
  useEffect(() => {
    const ws = new ScrapingJobStatusWebSocket();

    (async () => {
      await ws.connect();
    })();

    const cleanupFN = ws.onJobsStatusUpdate(cb);

    return () => {
      cleanupFN();
      ws.disconnect();
    };
  }, []);
};
