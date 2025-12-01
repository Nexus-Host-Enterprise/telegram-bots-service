"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { useBots } from "@/hooks/useBots";
import { useRouter } from "next/navigation";

type Field = { name: string; type: string; label?: string };

export default function CreateBotPage() {
  const [templates, setTemplates] = useState<any[]>([]);
  const [selected, setSelected] = useState<string | null>(null);
  const [schema, setSchema] = useState<Record<string, any> | null>(null);
  const [form, setForm] = useState<Record<string, any>>({});
  const [name, setName] = useState("");
  const [token, setToken] = useState("");
  const { create } = useBots();
  const router = useRouter();

  useEffect(()=> {
    api.get("/api/v1/templates").then(r=>setTemplates(r.data));
  },[]);

  useEffect(()=> {
    if (!selected) { setSchema(null); return; }
    const t = templates.find(t=>t.name===selected);
    setSchema(t?.config_schema ?? null);
    // init form defaults
    setForm({});
  }, [selected, templates]);

  function renderField(key: string, val: any) {
    // simple mapping: if schema describes "questions": "list" -> allow textarea lines
    if (val === "list") {
      return (
        <textarea value={(form[key] || []).join("\n")} onChange={(e)=> setForm({...form, [key]: e.target.value.split("\n").filter(Boolean) })} className="w-full p-2 border rounded" />
      );
    }
    if (val === "string" || val === "text") {
      return <input value={form[key] || ""} onChange={(e)=> setForm({...form, [key]: e.target.value })} className="w-full p-2 border rounded" />;
    }
    // default: json editor
    return <textarea value={JSON.stringify(form[key] ?? "", null, 2)} onChange={(e)=> { try { setForm({...form, [key]: JSON.parse(e.target.value)}); } catch { } }} className="w-full p-2 border rounded" />;
  }

  async function submit() {
    const cfg = schema ? Object.fromEntries(Object.entries(schema).map(([k, v]) => [k, form[k] || (v==="list" ? [] : "")])) : {};
    await create.mutateAsync({ name, template_name: selected, config: cfg, tg_token: token });
    router.push("/dashboard/bots");
  }

  return (
    <div>
      <h1 className="text-2xl mb-4">Создать бота</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block mb-1">Название</label>
          <input className="w-full p-2 border rounded mb-3" value={name} onChange={(e)=>setName(e.target.value)} />
          <label className="block mb-1">Шаблон</label>
          <select className="w-full p-2 border rounded mb-3" value={selected ?? ""} onChange={(e)=> setSelected(e.target.value)}>
            <option value="">— выберите шаблон —</option>
            {templates.map(t=> <option key={t.name} value={t.name}>{t.name} — {t.description}</option>)}
          </select>
          <label className="block mb-1">TG Bot Token</label>
          <input className="w-full p-2 border rounded mb-3" value={token} onChange={(e)=> setToken(e.target.value)} />
          <button className="px-4 py-2 bg-green-600 text-white rounded" onClick={submit}>Создать</button>
        </div>

        <div>
          <h3 className="font-medium mb-2">Конфигурация</h3>
          {!schema && <div className="text-gray-500">Выберите шаблон — поля появятся здесь.</div>}
          {schema && Object.entries(schema).map(([k,v]) => (
            <div key={k} className="mb-3">
              <label className="block mb-1 font-medium">{k}</label>
              {renderField(k,v)}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
