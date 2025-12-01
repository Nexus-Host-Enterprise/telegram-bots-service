// lib/api.ts
import axios from "axios";
import { getState, setState } from "./store";

const baseURL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const api = axios.create({ baseURL, timeout: 10000 });

api.interceptors.request.use((cfg) => {
  const token = getState().accessToken;
  if (token && cfg.headers) cfg.headers.Authorization = `Bearer ${token}`;
  return cfg;
});

api.interceptors.response.use(
  (r) => r,
  async (err) => {
    const original = err.config;
    if (!original) return Promise.reject(err);
    if (err.response?.status === 401 && !original._retry) {
      original._retry = true;
      const refresh = getState().refreshToken;
      if (!refresh) {
        // logout
        setState({ accessToken: null, refreshToken: null, user: null });
        return Promise.reject(err);
      }
      try {
        const resp = await axios.post(`${baseURL}/api/v1/auth/refresh`, { refresh_token: refresh });
        setState({ accessToken: resp.data.access_token, refreshToken: resp.data.refresh_token });
        original.headers.Authorization = `Bearer ${resp.data.access_token}`;
        return axios(original);
      } catch (e) {
        setState({ accessToken: null, refreshToken: null, user: null });
        return Promise.reject(e);
      }
    }
    return Promise.reject(err);
  }
);
