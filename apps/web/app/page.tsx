"use client";

import { signInWithPopup } from "firebase/auth";
import { auth, googleProvider } from "@/lib/firebase";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();

  const handleLogin = async () => {
    try {
      await signInWithPopup(auth, googleProvider);
      router.push("/dashboard");
    } catch (error) {
      console.error("Erro ao fazer login:", error);
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-gray-950">
      <div className="bg-gray-900 p-10 rounded-2xl shadow-xl flex flex-col items-center gap-6">
        <h1 className="text-2xl font-bold text-white">E3 CRM</h1>
        <p className="text-gray-400">Faça login para acessar sua unidade</p>
        <button
          onClick={handleLogin}
          className="bg-white text-gray-900 font-semibold px-6 py-3 rounded-lg hover:bg-gray-100 transition"
        >
          Entrar com Google
        </button>
      </div>
    </main>
  );
}