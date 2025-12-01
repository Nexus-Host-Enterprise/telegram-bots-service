import Link from "next/link";
import { useStore } from "@/lib/store";

export default function Navbar() {
  const user = useStore((s) => s.user);
  return (
    <nav className="bg-white border-b">
      <div className="container mx-auto flex items-center justify-between p-4">
        <Link href="/"><span className="font-bold">Nexus Host — BotStudio</span></Link>
        <div className="flex items-center gap-4">
          <Link href="/dashboard">Дашборд</Link>
          {user ? <span className="text-sm text-gray-600">{user.email}</span> : <Link href="/auth/login">Войти</Link>}
        </div>
      </div>
    </nav>
  );
}
