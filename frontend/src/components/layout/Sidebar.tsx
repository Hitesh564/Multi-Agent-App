import { useState, useEffect } from "react";
import { Brain, FileText, Trash2, FileX, Save } from "lucide-react";
import { useAppStore } from "@/lib/store";
import { cn } from "@/lib/utils";

export function Sidebar({ className }: { className?: string }) {
  const { autoSave, setAutoSave } = useAppStore();
  const [stats, setStats] = useState({ memory_items: 0, indexed_docs: 0, mode: "Multi-agent" });

  useEffect(() => {
    // Poll stats occasionally
    const fetchStats = async () => {
      try {
        const res = await fetch("/api/status");
        if (res.ok) {
          const data = await res.json();
          setStats(data);
        }
      } catch (err) {}
    };
    fetchStats();
    const int = setInterval(fetchStats, 5000);
    return () => clearInterval(int);
  }, []);

  const handleClearMemory = async () => {
    await fetch("/api/memory", { method: "DELETE" });
  };
  
  const handleClearDocs = async () => {
    await fetch("/api/documents", { method: "DELETE" });
  };

  return (
    <aside className={cn("fixed top-12 left-0 bottom-0 w-[260px] bg-[var(--bg-panel)] border-r border-[var(--border-subtle)] p-4 overflow-y-auto z-40 hidden md:flex flex-col gap-4", className)}>
      
      {/* Live Status Metrics */}
      <div className="grid grid-cols-2 gap-2">
        <div className="bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-lg p-2.5 flex flex-col justify-between">
          <div className="flex items-center gap-1 text-[11px] font-medium text-[var(--text-muted)] tracking-[0.3px] uppercase">
            <Brain className="w-[14px] h-[14px] text-[var(--accent-primary)]" />
            Memory
          </div>
          <div className="text-[20px] font-semibold text-[var(--text-primary)] mt-1">{stats.memory_items}</div>
        </div>
        
        <div className="bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-lg p-2.5 flex flex-col justify-between">
          <div className="flex items-center gap-1 text-[11px] font-medium text-[var(--text-muted)] tracking-[0.3px] uppercase">
            <FileText className="w-[14px] h-[14px] text-[var(--color-info)]" />
            Docs
          </div>
          <div className="text-[20px] font-semibold text-[var(--text-primary)] mt-1">{stats.indexed_docs}</div>
        </div>
      </div>
      
      <div className="bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-lg p-2.5 flex justify-between items-center">
         <span className="text-[11px] font-medium text-[var(--text-muted)] tracking-[0.3px] uppercase">Mode</span>
         <span className="bg-[var(--accent-primary-dim)] text-[var(--accent-primary)] rounded px-1.5 py-0.5 text-[11px] font-semibold">
           {stats.mode}
         </span>
      </div>

      <div className="h-[1px] bg-[var(--border-subtle)] my-2" />

      {/* Workspace Actions */}
      <div className="flex flex-col gap-1.5">
        <button className="w-full flex items-center gap-2 px-2.5 py-2 rounded-lg border border-[var(--border-subtle)] bg-transparent text-[13px] font-medium text-[var(--text-secondary)] hover:border-[var(--border-default)] hover:bg-[var(--bg-card)] hover:text-[var(--text-primary)] transition-all">
          <Trash2 className="w-3.5 h-3.5" />
          Clear Conversation
        </button>
        <button onClick={handleClearMemory} className="w-full flex items-center gap-2 px-2.5 py-2 rounded-lg border border-[var(--border-subtle)] bg-transparent text-[13px] font-medium text-[var(--text-secondary)] hover:border-[var(--border-default)] hover:bg-[var(--bg-card)] hover:text-[var(--text-primary)] transition-all">
          <Brain className="w-3.5 h-3.5" />
          Clear Memory
        </button>
        <button onClick={handleClearDocs} className="w-full flex items-center gap-2 px-2.5 py-2 rounded-lg border border-[var(--border-subtle)] bg-transparent text-[13px] font-medium text-[var(--text-secondary)] hover:border-[var(--border-default)] hover:bg-[var(--bg-card)] hover:text-[var(--text-primary)] transition-all">
          <FileX className="w-3.5 h-3.5" />
          Clear Documents
        </button>
      </div>

      <div className="flex items-center justify-between py-2">
        <span className="text-[13px] text-[var(--text-secondary)]">Auto-save Context</span>
        <button 
          onClick={() => setAutoSave(!autoSave)}
          className={`w-8 h-[18px] rounded-full relative transition-colors ${autoSave ? 'bg-[var(--accent-primary)]' : 'bg-[var(--bg-elevated)] border border-[var(--border-default)]'}`}
        >
          <div className={cn("absolute top-[1px] left-[1px] w-3.5 h-3.5 bg-white rounded-full transition-transform", autoSave ? "translate-x-[14px]" : "")} />
        </button>
      </div>

      <div className="h-[1px] bg-[var(--border-subtle)] my-2" />

      {/* Memory Notes */}
      <div className="flex-1 flex flex-col gap-2">
        <span className="text-[12px] font-semibold text-[var(--text-muted)] uppercase tracking-[0.3px]">Memory Notes</span>
        <textarea 
          placeholder="Capture a note for future context..."
          className="w-full min-h-[80px] flex-1 bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-lg p-2.5 text-[13px] text-[var(--text-primary)] resize-none focus:outline-none focus:border-[var(--accent-primary)] focus:ring-2 focus:ring-[var(--accent-primary-dim)] placeholder:text-[var(--text-muted)]"
        />
        <button className="w-full flex items-center justify-center gap-1.5 bg-[var(--accent-primary)] text-white rounded-lg p-1.5 text-[13px] font-medium hover:bg-[var(--accent-primary-hover)] transition-colors">
          <Save className="w-3.5 h-3.5" />
          Save Note
        </button>
      </div>

    </aside>
  );
}
