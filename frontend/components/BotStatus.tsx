export default function BotStatus({ status }: { status: string }) {
  const map: any = {
    creating: "Создаётся",
    deploying: "Деплоится",
    running: "Запущен",
    stopped: "Остановлен",
    failed: "Ошибка",
  };
  const color: any = {
    creating: "text-blue-500",
    deploying: "text-amber-500",
    running: "text-green-600",
    stopped: "text-gray-500",
    failed: "text-red-600",
  };
  return <span className={`${color[status] || "text-gray-700"} font-medium`}>{map[status] ?? status}</span>;
}

