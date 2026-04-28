import { useAppStore, TabType } from "@/lib/store";
import { Settings, Rocket, Menu } from "lucide-react";
import { Button } from "@/components/ui/button";

export function TopNav() {
  const { activeTab, setActiveTab, setDrawerOpen } = useAppStore();
  const tabs: TabType[] = ["Chat", "Memory Board", "Documents", "Debug"];

  return (
    <header className="fixed top-0 left-0 right-0 h-12 z-50 bg-[var(--bg-panel)] border-b border-[var(--border-subtle)] flex items-center justify-between px-4">
      {/* Left */}
      <div className="flex items-center gap-3">
        <Rocket className="w-4 h-4 text-[var(--accent-primary)]" />
        <span className="font-semibold text-sm text-[var(--text-primary)] hidden sm:block">AgentOS</span>
        <span className="text-[var(--text-muted)] hidden sm:block">·</span>
        <span className="text-sm text-[var(--text-secondary)] hidden sm:block">Workspace</span>
        
        {/* Mobile menu trigger */}
        <Button variant="ghost" size="icon" className="md:hidden h-8 w-8 text-[var(--text-secondary)]">
          <Menu className="w-4 h-4" />
        </Button>
      </div>

      {/* Center Tabs */}
      <nav className="flex items-center gap-1 bg-transparent">
        {tabs.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-3 py-1 text-[13px] font-medium rounded-full transition-all duration-150 ${
              activeTab === tab
                ? "bg-[var(--accent-primary)] text-white"
                : "text-[var(--text-secondary)] hover:bg-[var(--bg-elevated)] hover:text-[var(--text-primary)]"
            }`}
          >
            {tab}
          </button>
        ))}
      </nav>

      {/* Right */}
      <div className="flex items-center gap-4">
        {/* Live Status */}
        <div className="hidden sm:flex items-center gap-2">
          <div className="w-2 h-2 rounded-full bg-[var(--color-success)] status-dot" />
          <span className="text-xs text-[var(--text-secondary)]">Multi-agent</span>
        </div>

        <Button
          variant="ghost"
          size="icon"
          onClick={() => setDrawerOpen(true)}
          className="h-8 w-8 text-[var(--text-secondary)] hover:bg-[var(--bg-elevated)] rounded-md"
        >
          <Settings className="w-4 h-4" />
        </Button>

        <button className="hidden sm:block border-none bg-transparent rounded-md text-[13px] font-medium text-[var(--text-primary)] border border-[var(--border-default)] px-3 py-1 hover:border-[var(--border-strong)] hover:bg-[var(--bg-card)] transition-colors">
          Deploy
        </button>
      </div>
    </header>
  );
}
