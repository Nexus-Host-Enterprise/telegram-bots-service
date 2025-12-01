"use client";
import { useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [pw, setPw] = useState("");
  const { login } = useAuth();
  const router = useRouter();

  async function submit() {
    await login(email, pw);
    router.push("/dashboard/bots");
  }

  return (
    <div className="container mx-auto py-20 max-w-md">
      <h2 className="text-2xl mb-4">Вход</h2>
      <input className="w-full p-2 border rounded mb-2" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
      <input className="w-full p-2 border rounded mb-4" placeholder="Пароль" type="password" value={pw} onChange={e=>setPw(e.target.value)} />
      <button className="px-4 py-2 bg-blue-600 text-white rounded" onClick={submit}>Войти</button>
    </div>
  );
}

