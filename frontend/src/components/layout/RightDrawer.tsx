import { useAppStore } from "@/lib/store";
import { X } from "lucide-react";
import { cn } from "@/lib/utils";

export function RightDrawer() {
  const { drawerOpen, setDrawerOpen } = useAppStore();

  return (
    <>
      <div 
        className={cn(
          "fixed inset-0 bg-[var(--bg-overlay)] z-[44] transition-opacity duration-250 pointer-events-none",
          drawerOpen ? "opacity-100 pointer-events-auto" : "opacity-0"
        )}
        onClick={() => setDrawerOpen(false)}
      />
      
      <aside 
        className={cn(
          "fixed top-12 right-0 bottom-0 w-[300px] z-[45] bg-[var(--bg-panel)] border-l border-[var(--border-subtle)] transform transition-transform duration-250 ease-[cubic-bezier(0.4,0,0.2,1)] flex flex-col",
          drawerOpen ? "translate-x-0" : "translate-x-[100%]"
        )}
      >
        <div className="flex items-center justify-between p-3.5 border-b border-[var(--border-subtle)]">
          <h2 className="text-[14px] font-semibold text-[var(--text-primary)]">Settings</h2>
          <button 
            onClick={() => setDrawerOpen(false)}
            className="text-[var(--text-secondary)] hover:bg-[var(--bg-elevated)] p-1 rounded-md"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
        
        <div className="p-4 flex flex-col gap-4">
          <div className="flex flex-col gap-2">
            <label className="text-[13px] font-medium text-[var(--text-secondary)]">Model</label>
            <select className="w-full bg-[var(--bg-card)] border border-[var(--border-default)] rounded-md px-3 py-2 text-[13px] text-[var(--text-primary)] focus:outline-none focus:border-[var(--accent-primary)]">
              <option>claude-3-5-sonnet</option>
              <option>claude-3-haiku</option>
            </select>
          </div>
          
          <div className="flex flex-col gap-2">
            <label className="text-[13px] font-medium text-[var(--text-secondary)]">Temperature</label>
            <input type="range" min="0" max="1" step="0.1" className="w-full accent-[var(--accent-primary)]" />
          </div>
        </div>
      </aside>
    </>
  );
}
