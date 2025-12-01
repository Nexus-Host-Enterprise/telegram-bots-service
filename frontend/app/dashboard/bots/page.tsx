"use client";
import { useBots } from "@/hooks/useBots";
import BotCard from "@/components/BotCard";
import Link from "next/link";

export default function BotsPage() {
  const { list } = useBots();
  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl">Мои боты</h1>
        <Link href="/dashboard/bots/create" className="px-3 py-2 bg-blue-600 text-white rounded">Создать бота</Link>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {list.data?.map((b:any)=> <BotCard key={b.id} bot={b} />)}
      </div>
    </div>
  );
}

