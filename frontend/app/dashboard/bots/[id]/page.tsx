"use client";
import { useEffect, useState, useCallback } from "react";
import { useRouter, useParams } from "next/navigation";
import { useBots } from "@/hooks/useBots";
import LogsViewer from "@/components/LogsViewer";

export default function BotPage() {
  // next/navigation in app router: useParams only in component; here we take id from search
  // for simplicity use window.location
  const id = typeof window !== "undefined" ? window.location.pathname.split("/").pop() : null;
  const { get, stop, logs } = useBots();
  const [bot, setBot] = useState<any>(null);

  useEffect(()=> {
    if (!id) return;
    get(id).then(r=>setBot(r));
  }, [id]);

  const fetchLogs = useCallback(async () => {
    if (!id) return [];
    const resp = await fetch(`${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/v1/bots/${id}/logs?lines=200`, {
      headers: { Authorization: `Bearer ${ (localStorage.getItem("accessToken") || "") }` }
    });
    const data = await resp.json();
    // data might be string or lines array — normalize
    if (Array.isArray(data)) return data;
    if (typeof data === "string") return data.split("\n").reverse();
    return [JSON.stringify(data)];
  }, [id]);

  if (!bot) return <div>Загрузка...</div>;

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl">{bot.name}</h1>
        <div>
          <button className="px-3 py-1 bg-red-600 text-white rounded" onClick={() => stop.mutate(bot.id)}>Остановить</button>
        </div>
      </div>

      <div className="mb-4">
        <strong>Шаблон:</strong> {bot.template_name} — <strong>Статус:</strong> {bot.status}
      </div>

      <h3 className="mb-2">Логи</h3>
      <LogsViewer fetchLogs={fetchLogs} />
    </div>
  );
}
