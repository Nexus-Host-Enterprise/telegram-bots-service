// hooks/useAuth.ts
import { api } from "@/lib/api";
import { useStore } from "@/lib/store";
import { useQueryClient } from "@tanstack/react-query";

export const useAuth = () => {
  const setTokens = useStore((s) => s.setTokens);
  const setUser = useStore((s) => s.setUser);
  const qc = useQueryClient();

  async function login(email: string, password: string) {
    const resp = await api.post("/api/v1/auth/token", new URLSearchParams({ username: email, password })); // OAuth2PasswordRequestForm shape
    setTokens(resp.data.access_token, resp.data.refresh_token);
    await loadProfile();
  }

  async function register(email: string, password: string, full_name?: string) {
    const resp = await api.post("/api/v1/auth/register", { email, password, full_name });
    setTokens(resp.data.access_token, resp.data.refresh_token);
    await loadProfile();
  }

  async function loadProfile() {
    const resp = await api.get("/api/v1/users/me");
    setUser(resp.data);
  }

  async function logout() {
    setTokens(null, null);
    setUser(null);
    qc.clear();
  }

  return { login, register, loadProfile, logout };
};

