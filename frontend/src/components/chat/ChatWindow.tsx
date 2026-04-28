import { useState, useRef, useEffect } from "react";
import { useAppStore } from "@/lib/store";
import { Copy, RefreshCw, BrainCircuit, Rocket, Paperclip, ArrowUp, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface Message {
  role: "user" | "assistant";
  content: string;
  route?: string;
}

export function ChatWindow() {
  const { sessionId } = useAppStore();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    // Load history
    fetch(`/api/chat/history/${sessionId}`)
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) setMessages(data);
      })
      .catch(console.error);
  }, [sessionId]);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
    // Auto-resize
    e.target.style.height = "auto";
    e.target.style.height = `${Math.min(e.target.scrollHeight, 160)}px`;
  };

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;
    const msg = input;
    setInput("");
    if (textareaRef.current) textareaRef.current.style.height = "auto";
    
    setMessages(prev => [...prev, { role: "user", content: msg }]);
    setIsLoading(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId, message: msg }),
      });
      const data = await res.json();
      if (res.ok) {
        setMessages(prev => [...prev, { role: "assistant", content: data.content, route: data.route }]);
      } else {
        setMessages(prev => [...prev, { role: "assistant", content: `❌ Error: ${data.error}` }]);
      }
    } catch (err) {
      setMessages(prev => [...prev, { role: "assistant", content: "❌ Network error." }]);
    } finally {
      setIsLoading(false);
    }
  };

  const onKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const renderBadge = (route?: string) => {
    if (!route) return null;
    let className = "";
    if (route === "GENERAL") className = "bg-[var(--accent-primary-dim)] text-[var(--accent-primary)]";
    else if (route === "RAG") className = "bg-[var(--color-success-dim)] text-[var(--color-success)]";
    else if (route === "TOOL") className = "bg-[var(--color-info-dim)] text-[var(--color-info)]";
    
    return (
      <div className={cn("text-[10px] font-bold tracking-[0.5px] px-2 py-0.5 rounded-full mb-1 inline-block", className)}>
        {route} AGENT
      </div>
    );
  };

  return (
    <div className="flex-1 flex flex-col min-h-0 bg-[var(--bg-base)]">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 pt-6 pb-4">
        <div className="max-w-[760px] mx-auto w-full flex flex-col gap-4">
          
          <div className="border-b border-[var(--border-subtle)] pb-4 mb-2">
             <h1 className="text-[16px] font-semibold text-[var(--text-primary)]">Workspace Chat</h1>
             <p className="text-[13px] text-[var(--text-secondary)]">Multi-agent powered workspace</p>
          </div>

          {messages.length === 0 && !isLoading && (
            <div className="flex flex-col items-center justify-center py-20 text-center">
              <Rocket className="w-12 h-12 text-[var(--accent-primary)] mb-4" />
              <h2 className="text-[22px] font-semibold text-[var(--text-primary)] mb-2">How can I help you today?</h2>
              <p className="text-[15px] text-[var(--text-secondary)] mb-8">Powered by multi-agent AI with persistent memory and document recall.</p>
            </div>
          )}

          {messages.map((m, i) => (
            <div key={i} className={cn("flex", m.role === "user" ? "justify-end mt-4" : "justify-start mt-4")}>
              <div className="flex flex-col max-w-[80%]">
                {m.role === "assistant" && renderBadge(m.route)}
                <div 
                  className={cn(
                    "px-4 py-2.5 text-[15px] max-w-full text-wrap break-words leading-relaxed whitespace-pre-wrap",
                    m.role === "user" 
                      ? "bg-[var(--accent-primary)] text-white rounded-[18px_18px_4px_18px]" 
                      : "bg-[var(--bg-card)] border border-[var(--border-subtle)] text-[var(--text-primary)] rounded-[18px_18px_18px_4px]"
                  )}
                >
                  {m.content}
                </div>
              </div>
            </div>
          ))}

          {isLoading && (
             <div className="flex justify-start mt-4">
               <div className="bg-[var(--bg-card)] border border-[var(--border-subtle)] px-4 py-3 rounded-[18px_18px_18px_4px] flex items-center gap-1.5 h-10 w-16">
                  <div className="typing-dot w-1.5 h-1.5 rounded-full bg-[var(--text-muted)]" />
                  <div className="typing-dot w-1.5 h-1.5 rounded-full bg-[var(--text-muted)]" />
                  <div className="typing-dot w-1.5 h-1.5 rounded-full bg-[var(--text-muted)]" />
               </div>
             </div>
          )}
          
          <div ref={endRef} />
        </div>
      </div>

      {/* Input */}
      <div className="sticky bottom-0 bg-[var(--bg-base)] border-t border-[var(--border-subtle)] px-6 pt-3 pb-4">
        <div className="max-w-[760px] mx-auto w-full">
          <div className="bg-[var(--bg-card)] border border-[var(--border-default)] rounded-xl flex items-end gap-2 p-2 focus-within:border-[var(--accent-primary)] focus-within:ring-[3px] focus-within:ring-[var(--accent-primary-dim)] transition-all">
            <button className="p-1.5 rounded-md text-[var(--text-muted)] hover:text-[var(--text-secondary)] hover:bg-[var(--bg-elevated)] transition-colors mb-0.5">
              <Paperclip className="w-4 h-4" />
            </button>
            <textarea
              ref={textareaRef}
              value={input}
              onChange={handleInput}
              onKeyDown={onKeyDown}
              placeholder={isLoading ? "Agent is thinking..." : "Ask anything..."}
              disabled={isLoading}
              className="flex-1 bg-transparent border-none outline-none resize-none text-[15px] text-[var(--text-primary)] min-h-[24px] max-h-[160px] py-1 placeholder:text-[var(--text-muted)]"
              rows={1}
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
              className="p-1.5 rounded-[8px] bg-[var(--accent-primary)] text-white hover:bg-[var(--accent-primary-hover)] disabled:bg-[var(--bg-elevated)] disabled:text-[var(--text-muted)] transition-all flex items-center justify-center w-8 h-8 mb-0.5"
            >
              <ArrowUp className="w-4 h-4" />
            </button>
          </div>
          <div className="text-center mt-2 text-[11px] text-[var(--text-muted)]">
            NovaMind uses Claude · Responses may be inaccurate
          </div>
        </div>
      </div>
    </div>
  );
}
