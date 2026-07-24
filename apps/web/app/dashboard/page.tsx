"use client";

import { useEffect, useState } from "react";
import { auth } from "@/lib/firebase";
import { useRouter } from "next/navigation";
import { onAuthStateChanged, signOut } from "firebase/auth";

interface Message {
  id: number;
  phone: string;
  content: string;
  received_at: string;
  unit_id: number;
}

export default function DashboardPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      if (!user) {
        router.push("/");
        return;
      }

      const token = await user.getIdToken();
      const res = await fetch("https://e3-crm-production.up.railway.app/messages", {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (res.ok) {
        const data = await res.json();
        setMessages(data);
      }

      setLoading(false);
    });

    return () => unsubscribe();
  }, [router]);

  const handleLogout = async () => {
    await signOut(auth);
    router.push("/");
  };

  if (loading) return (
    <main className="flex min-h-screen items-center justify-center bg-gray-950">
      <p className="text-white">Carregando...</p>
    </main>
  );

  return (
    <main className="min-h-screen bg-gray-950 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-2xl font-bold text-white">E3 CRM — Mensagens</h1>
          <button
            onClick={handleLogout}
            className="text-sm text-gray-400 hover:text-white transition"
          >
            Sair
          </button>
        </div>

        {messages.length === 0 ? (
          <p className="text-gray-500">Nenhuma mensagem recebida ainda.</p>
        ) : (
          <div className="flex flex-col gap-4">
            {messages.map((msg) => (
              <div key={msg.id} className="bg-gray-900 rounded-xl p-5">
                <p className="text-green-400 font-mono text-sm">{msg.phone}</p>
                <p className="text-white mt-1">{msg.content}</p>
                <p className="text-gray-500 text-xs mt-2">
                  {new Date(msg.received_at).toLocaleString("pt-BR")}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}