import { useState, useEffect } from "react";
import { Brain, Search, Trash2 } from "lucide-react";

export function MemoryBoard() {
  const [memories, setMemories] = useState<string[]>([]);
  const [search, setSearch] = useState("");

  const fetchMemories = async () => {
    try {
      const res = await fetch("/api/memory");
      const data = await res.json();
      setMemories(data.items || []);
    } catch(err) {}
  };

  useEffect(() => {
    fetchMemories();
  }, []);

  const handleClear = async () => {
    await fetch("/api/memory", { method: "DELETE" });
    fetchMemories();
  };

  const filtered = memories.filter(m => m.toLowerCase().includes(search.toLowerCase()));

  return (
    <div className="flex-1 p-6 overflow-y-auto max-w-[900px] mx-auto w-full">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <h1 className="text-[20px] font-semibold text-[var(--text-primary)]">Memory Board</h1>
          <span className="bg-[var(--bg-elevated)] text-[var(--text-secondary)] text-[12px] px-2 py-0.5 rounded-full">{memories.length}</span>
        </div>
        <button onClick={handleClear} className="text-[13px] text-[var(--text-muted)] hover:text-[var(--color-error)]">Clear All</button>
      </div>

      <div className="relative mb-6">
        <Search className="w-4 h-4 absolute left-3 top-2.5 text-[var(--text-muted)]" />
        <input 
          type="text" 
          placeholder="Search memories..." 
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-lg pl-9 pr-3 py-2 text-[14px] text-[var(--text-primary)] focus:outline-none focus:border-[var(--accent-primary)]"
        />
      </div>

      {filtered.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 text-center">
          <Brain className="w-8 h-8 text-[var(--text-muted)] mb-3" />
          <h3 className="text-[16px] font-medium text-[var(--text-primary)]">No memories yet</h3>
          <p className="text-[14px] text-[var(--text-secondary)] mt-1">Start a conversation and enable auto-save to build memory.</p>
        </div>
      ) : (
        <div className="flex flex-col gap-3">
          {filtered.map((m, i) => (
            <div key={i} className="flex items-start gap-4 p-3.5 bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-xl hover:border-[var(--border-default)] hover:bg-[var(--bg-elevated)] transition-colors group">
              <div className="flex items-center justify-center min-w-[24px] h-[24px] bg-[var(--accent-primary-dim)] text-[var(--accent-primary)] rounded-full text-[11px] font-bold">
                {i + 1}
              </div>
              <div className="flex-1 text-[14px] text-[var(--text-primary)] leading-snug">
                {m}
              </div>
              <div className="opacity-0 group-hover:opacity-100 transition-opacity">
                <button className="text-[var(--text-muted)] hover:text-[var(--color-error)] transition-colors">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
