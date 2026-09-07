"use client";

import { useState, useRef, useEffect } from "react";
import TopBar from "@/components/TopBar";
import { api } from "@/lib/api";

interface Msg { role: "user" | "assistant"; content: string; }

const SAMPLE_QUESTIONS = ["Aloo ka rate?", "Weather update", "Khad ke rates?"];

export default function AssistantPage() {
  const [messages, setMessages] = useState<Msg[]>([
    { role: "assistant", content: "Assalam o Alaikum! Main Smart Kisan AI Assistant hoon. Aap mujhe kisi bhi zarooat ke hawalay se pooch sakte hain." },
  ]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => { endRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  async function send(text: string) {
    if (!text.trim() || sending) return;
    setMessages((m) => [...m, { role: "user", content: text }]);
    setInput("");
    setSending(true);
    const reply = await api.chat(text);
    setMessages((m) => [...m, { role: "assistant", content: reply }]);
    setSending(false);
  }

  return (
    <>
      <TopBar title="AI Assistant" />
      <div className="p-8 flex justify-center">
        <div className="w-full max-w-2xl bg-white rounded-2xl shadow-card border border-black/5 flex flex-col h-[600px]">
          <div className="flex-1 overflow-y-auto p-6 space-y-4 scrollbar-thin">
            {messages.map((m, i) => (
              <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
                <div className={`max-w-[75%] px-4 py-2.5 rounded-2xl text-sm leading-relaxed ${
                  m.role === "user" ? "bg-brand-600 text-white rounded-br-sm" : "bg-cream text-ink rounded-bl-sm"
                }`}>
                  {m.content}
                </div>
              </div>
            ))}
            {sending && <p className="text-xs text-ink/30">Typing…</p>}
            <div ref={endRef} />
          </div>

          <div className="px-6 pb-3 flex flex-wrap gap-2">
            {SAMPLE_QUESTIONS.map((q) => (
              <button key={q} onClick={() => send(q)} className="text-xs border border-black/10 rounded-full px-3 py-1 text-ink/60 hover:border-brand-500 hover:text-brand-600 transition-colors">
                {q}
              </button>
            ))}
          </div>

          <div className="border-t border-black/5 p-4 flex gap-3">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && send(input)}
              placeholder="Type your question..."
              className="flex-1 bg-cream rounded-full px-4 py-2.5 text-sm outline-none"
            />
            <button onClick={() => send(input)} className="bg-brand-600 hover:bg-brand-700 text-white w-10 h-10 rounded-full flex items-center justify-center transition-colors">
              ➤
            </button>
          </div>
        </div>
      </div>
    </>
  );
}
