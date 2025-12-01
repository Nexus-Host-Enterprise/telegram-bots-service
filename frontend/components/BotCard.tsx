import Link from "next/link";
import BotStatus from "./BotStatus";

export default function BotCard({ bot }: { bot: any }) {
  return (
    <Link href={`/dashboard/bots/${bot.id}`} className="block">
      <div className="p-4 bg-white rounded shadow-sm hover:shadow-md transition">
        <div className="flex justify-between items-start">
          <div>
            <h3 className="font-medium">{bot.name}</h3>
            <p className="text-sm text-gray-500">{bot.template_name}</p>
          </div>
          <BotStatus status={bot.status} />
        </div>
      </div>
    </Link>
  );
}
