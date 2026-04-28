import { create } from 'zustand';
import { v4 as uuidv4 } from 'uuid';

export type TabType = 'Chat' | 'Memory Board' | 'Documents' | 'Debug';

interface AppState {
  activeTab: TabType;
  setActiveTab: (tab: TabType) => void;
  
  drawerOpen: boolean;
  setDrawerOpen: (open: boolean) => void;
  
  sessionId: string;
  setSessionId: (id: string) => void;
  
  autoSave: boolean;
  setAutoSave: (save: boolean) => void;
}

export const useAppStore = create<AppState>((set) => ({
  activeTab: 'Chat',
  setActiveTab: (tab) => set({ activeTab: tab }),
  
  drawerOpen: false,
  setDrawerOpen: (open) => set({ drawerOpen: open }),
  
  sessionId: uuidv4(),
  setSessionId: (id) => set({ sessionId: id }),
  
  autoSave: false,
  setAutoSave: (save) => set({ autoSave: save }),
}));
