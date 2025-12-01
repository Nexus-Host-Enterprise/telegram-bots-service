// lib/store.ts
import create from "zustand";

type User = { id: string; email: string; full_name?: string };

type State = {
  accessToken: string | null;
  refreshToken: string | null;
  user: User | null;
  setTokens: (a: string | null, r: string | null) => void;
  setUser: (u: User | null) => void;
  logout: () => void;
};

export const useStore = create<State>((set) => ({
  accessToken: null,
  refreshToken: null,
  user: null,
  setTokens: (a, r) => set({ accessToken: a, refreshToken: r }),
  setUser: (u) => set({ user: u }),
  logout: () => set({ accessToken: null, refreshToken: null, user: null }),
}));

// helpers for non-react modules (axios)
export const getState = () => {
  const s = useStore.getState();
  return { accessToken: s.accessToken, refreshToken: s.refreshToken, user: s.user };
};
export const setState = (patch: Partial<{ accessToken: string | null; refreshToken: string | null; user: User | null }>) => {
  useStore.setState(patch as any);
};
