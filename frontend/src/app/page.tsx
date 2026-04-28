"use client";

import { useAppStore } from "@/lib/store";
import { TopNav } from "@/components/layout/TopNav";
import { Sidebar } from "@/components/layout/Sidebar";
import { RightDrawer } from "@/components/layout/RightDrawer";
import { ChatWindow } from "@/components/chat/ChatWindow";
import { MemoryBoard } from "@/components/panels/MemoryBoard";
import { DocumentsPanel } from "@/components/panels/DocumentsPanel";
import { DebugPanel } from "@/components/panels/DebugPanel";

export default function Home() {
  const { activeTab } = useAppStore();

  return (
    <div className="flex h-screen w-full flex-col overflow-hidden bg-base text-primary">
      <TopNav />
      
      <div className="flex flex-1 overflow-hidden pt-12">
        <Sidebar className="hidden md:flex" />
        
        <main className="flex-1 transition-all md:ml-[260px] flex flex-col relative">
          {activeTab === 'Chat' && <ChatWindow />}
          {activeTab === 'Memory Board' && <MemoryBoard />}
          {activeTab === 'Documents' && <DocumentsPanel />}
          {activeTab === 'Debug' && <DebugPanel />}
        </main>

        <RightDrawer />
      </div>
    </div>
  );
}
