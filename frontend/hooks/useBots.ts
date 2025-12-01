// hooks/useBots.ts
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";

export function useBots() {
  const qc = useQueryClient();

  const list = useQuery(["bots"], async () => {
    const r = await api.get("/api/v1/bots");
    return r.data;
  });

  const create = useMutation(async (payload: any) => {
    const r = await api.post("/api/v1/bots", payload);
    return r.data;
  }, { onSuccess: () => qc.invalidateQueries(["bots"]) });

  const stop = useMutation(async (botId: string) => {
    const r = await api.post(`/api/v1/bots/${botId}/stop`);
    return r.data;
  }, { onSuccess: () => qc.invalidateQueries(["bots"]) });

  const get = async (id: string) => {
    const r = await api.get(`/api/v1/bots/${id}`);
    return r.data;
  };

  const logs = async (id: string, lines = 200) => {
    const r = await api.get(`/api/v1/bots/${id}/logs?lines=${lines}`);
    return r.data;
  };

  return { list, create, stop, get, logs };
}

