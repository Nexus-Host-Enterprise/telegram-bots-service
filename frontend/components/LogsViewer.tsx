"use client";
import { useEffect, useState } from "react";

export default function LogsViewer({ fetchLogs }: { fetchLogs: () => Promise<string[]> }) {
  const [logs, setLogs] = useState<string[]>([]);
  useEffect(() => {
    let mounted = true;
    async function poll() {
      try {
        const data = await fetchLogs();
        if (!mounted) return;
        setLogs(data);
      } catch (e) {}
      setTimeout(poll, 3000);
    }
    poll();
    return () => { mounted = false; };
  }, [fetchLogs]);
  return (
    <div className="bg-black text-green-300 p-3 rounded h-80 overflow-auto text-sm font-mono">
      {logs.map((l, i) => <div key={i}>{l}</div>)}
    </div>
  );
}
