import { useState, useEffect } from "react";
import { useAppStore } from "@/lib/store";
import { Terminal, Copy } from "lucide-react";

export function DebugPanel() {
  const { sessionId } = useAppStore();
  const [logs, setLogs] = useState<any>(null);

  useEffect(() => {
    fetch(`/api/status`)
      .then(res => res.json())
      .then(data => setLogs(data))
      .catch(console.error);
  }, []);

  return (
    <div className="flex-1 p-6 overflow-y-auto max-w-[900px] mx-auto w-full">
      <div className="flex items-center gap-2 mb-6">
        <Terminal className="w-5 h-5 text-[var(--text-primary)]" />
        <h1 className="text-[20px] font-semibold text-[var(--text-primary)]">Debug Trace</h1>
      </div>

      <div className="bg-[var(--bg-card)] border border-[var(--border-subtle)] rounded-xl p-4 relative font-mono text-[12px] text-[var(--text-primary)] overflow-x-auto">
        <button className="absolute top-3 right-3 p-1.5 bg-[var(--bg-elevated)] border border-[var(--border-default)] rounded-md text-[var(--text-secondary)] hover:text-[var(--text-primary)]">
          <Copy className="w-3.5 h-3.5" />
        </button>
        <pre className="mt-2 leading-relaxed">
          {JSON.stringify({ sessionId, status: logs }, null, 2)}
        </pre>
      </div>
    </div>
  );
}
