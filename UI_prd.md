# Product Requirements Document
## Adaptive Multi-Agent AI Portal — UI/UX Redesign for Vercel Deployment

**Version:** 1.0  
**Author:** [Your Name]  
**Date:** April 2026  
**Status:** Ready for Development  
**Deployment Target:** Vercel (Next.js / React)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Goals & Success Metrics](#2-goals--success-metrics)
3. [Target Users](#3-target-users)
4. [Technical Stack](#4-technical-stack)
5. [Information Architecture](#5-information-architecture)
6. [Design System](#6-design-system)
7. [Layout & Grid System](#7-layout--grid-system)
8. [Component Specifications](#8-component-specifications)
9. [Page-by-Page Breakdown](#9-page-by-page-breakdown)
10. [Interaction Design & Animations](#10-interaction-design--animations)
11. [Responsive Design](#11-responsive-design)
12. [Accessibility](#12-accessibility)
13. [Performance Requirements](#13-performance-requirements)
14. [Error States & Edge Cases](#14-error-states--edge-cases)
15. [Out of Scope](#15-out-of-scope)

---

## 1. Project Overview

### 1.1 What This Product Is

The **Adaptive Multi-Agent AI Portal** is a web-based AI assistant interface that supports multiple intelligent agents (General Agent, RAG Agent, Code Agent, etc.) with persistent memory, document indexing, and live tool access. Users can upload documents, ask questions across conversation sessions, and the system recalls context automatically.

### 1.2 Current State Problem

The current UI is built on Streamlit and has the following critical problems for a professional deployment:

- **Looks like a prototype.** Streamlit's default dark theme is immediately recognizable as non-production software. Internship reviewers and stakeholders will judge the product's maturity by its UI.
- **No visual hierarchy.** The current layout places equal visual weight on the chat, the sidebar controls, and the live status panel — making it cognitively overwhelming.
- **Poor chat UX.** Chat bubbles are not styled as bubbles — they are flat bordered boxes with left-border color coding that looks dated.
- **Wasted space.** The three-panel layout leaves large areas of dead space on standard 1440px screens.
- **No micro-interactions.** Nothing responds to hover, focus, or state changes with animations, making the product feel static and unresponsive.
- **Not deployable on Vercel.** Streamlit cannot deploy to Vercel. A full migration to Next.js + React is required.

### 1.3 Redesign Vision

A clean, fast, modern AI chat interface — comparable in visual quality to Perplexity AI, Claude.ai, or Linear — that demonstrates strong frontend engineering judgment. The redesign must:

- Feel production-ready and polished to impress internship evaluators
- Preserve all backend agent logic and API calls
- Be fully deployable on Vercel as a Next.js application
- Score well on Lighthouse (Performance > 90, Accessibility > 90)

---

## 2. Goals & Success Metrics

| Goal | Metric | Target |
|------|--------|--------|
| Visual quality | First impression score from evaluators | "Looks production-ready" |
| Performance | Lighthouse Performance score | ≥ 90 |
| Accessibility | Lighthouse A11y score | ≥ 90 |
| Chat responsiveness | Time-to-first-message-render | < 200ms |
| Mobile usability | Functional on 375px viewport | 100% core features work |
| Bundle size | Total JS bundle (gzipped) | < 200kb |

---

## 3. Target Users

### Primary User: Internship Evaluator / Technical Reviewer

- Views the project as a portfolio piece
- Judges UI quality in the first 5 seconds
- Looks for: visual consistency, component quality, thoughtful UX decisions
- Device: Desktop (1440px or 1920px monitor)

### Secondary User: End User of the AI Portal

- Wants to upload PDFs, ask questions, and get accurate answers
- Needs clear feedback on which agent is responding and why
- Wants to track what the system has remembered across sessions
- Device: Desktop-first, mobile occasionally

---

## 4. Technical Stack

| Layer | Technology | Reason |
|-------|-----------|--------|
| Framework | Next.js 14 (App Router) | Vercel-native, SSR, file-based routing |
| Language | TypeScript | Type safety across agent API responses |
| Styling | Tailwind CSS + CSS Variables | Utility-first + design token consistency |
| UI Components | shadcn/ui | Headless, accessible, customizable |
| Animation | Framer Motion | Production-grade animation library |
| State Management | Zustand | Lightweight, no boilerplate |
| API Layer | Next.js Route Handlers (`/api/`) | Backend proxy to Python agent logic |
| Font | Inter (Google Fonts, self-hosted) | Professional, widely used in SaaS |
| Icons | Lucide React | Consistent, minimal icon set |
| Deployment | Vercel | Zero-config, automatic CI/CD from GitHub |

### 4.1 File Structure

```
/app
  /layout.tsx           → Root layout with font, metadata, providers
  /page.tsx             → Main portal page
  /api
    /chat/route.ts      → POST handler proxying to Python agent backend
    /memory/route.ts    → GET/DELETE memory operations
    /documents/route.ts → POST/GET/DELETE document operations
/components
  /layout
    Sidebar.tsx
    TopNav.tsx
    RightDrawer.tsx
  /chat
    ChatWindow.tsx
    MessageBubble.tsx
    TypingIndicator.tsx
    ChatInput.tsx
  /panels
    MemoryBoard.tsx
    DocumentsPanel.tsx
    SettingsPanel.tsx
    DebugPanel.tsx
  /ui                   → shadcn/ui base components
/lib
  /store.ts             → Zustand global state
  /types.ts             → TypeScript interfaces
  /api.ts               → API fetch helpers
/styles
  /globals.css          → CSS variables, resets, base styles
```

---

## 5. Information Architecture

The application has one primary screen with contextual panels. Navigation is **tab-based** within the top navbar, not page-based routing.

```
Top Navigation Bar
├── Logo + App Name
├── Tab Pills: Chat | Memory Board | Documents | Debug
├── Status Indicator (live, pulsing)
└── Settings Icon | Deploy Button

Left Sidebar (fixed, 260px)
├── Live Status Metrics (Memory count, Docs count, Mode)
├── Workspace Actions (Clear Conversation, Clear Memory, Clear Documents)
├── Auto-save Toggle
└── Memory Notes (textarea + save button)

Main Content Area (flex-grow)
├── [Tab: Chat] → Chat Window + Input Bar
├── [Tab: Memory Board] → Full-width memory list with search
├── [Tab: Documents] → Document grid with upload dropzone
└── [Tab: Debug] → Raw JSON logs and agent trace

Right Drawer (collapsible, 300px, overlay)
└── Triggered by navbar icons, shows quick-access panels
```

---

## 6. Design System

### 6.1 Color Palette

All colors are defined as CSS custom properties in `globals.css` and automatically switch between light and dark mode via `prefers-color-scheme` and a manual toggle class `.dark` on `<html>`.

#### Dark Mode (Primary / Default)

```css
:root {
  /* Backgrounds — layered from darkest to lightest */
  --bg-base:        #0a0a0f;   /* Page background */
  --bg-panel:       #12121a;   /* Sidebar, navbar, drawer */
  --bg-card:        #1c1c26;   /* Card surfaces, input areas */
  --bg-elevated:    #252535;   /* Hover states, tooltips */
  --bg-overlay:     rgba(0, 0, 0, 0.6); /* Backdrop for drawers */

  /* Text */
  --text-primary:   #e8e8f0;   /* Main readable text */
  --text-secondary: #8888a8;   /* Labels, captions, metadata */
  --text-muted:     #44445a;   /* Placeholder text, dividers */
  --text-inverse:   #0a0a0f;   /* Text on accent backgrounds */

  /* Borders */
  --border-subtle:  rgba(255,255,255,0.06);  /* Default card borders */
  --border-default: rgba(255,255,255,0.10);  /* Interactive element borders */
  --border-strong:  rgba(255,255,255,0.18);  /* Focus rings, emphasis */

  /* Accent — Purple (primary brand color) */
  --accent-primary:     #7c6af7;  /* Buttons, active states */
  --accent-primary-dim: rgba(124, 106, 247, 0.15); /* Soft backgrounds */
  --accent-primary-hover: #9585f9; /* Hover variant */

  /* Semantic colors */
  --color-success:    #34c99a;
  --color-success-dim: rgba(52, 201, 154, 0.12);
  --color-warning:    #f5a623;
  --color-warning-dim: rgba(245, 166, 35, 0.12);
  --color-error:      #e24b4a;
  --color-error-dim:  rgba(226, 75, 74, 0.12);
  --color-info:       #378add;
  --color-info-dim:   rgba(55, 138, 221, 0.12);

  /* Agent type colors */
  --agent-general:    #7c6af7;  /* Purple — General Agent */
  --agent-rag:        #34c99a;  /* Teal — RAG Agent */
  --agent-code:       #378add;  /* Blue — Code Agent */
  --agent-search:     #f5a623;  /* Amber — Search Agent */
}
```

#### Light Mode

```css
.light {
  --bg-base:        #f4f4f8;
  --bg-panel:       #ffffff;
  --bg-card:        #f0f0f6;
  --bg-elevated:    #e8e8f0;
  --text-primary:   #1a1a2e;
  --text-secondary: #555570;
  --text-muted:     #aaaacc;
  --border-subtle:  rgba(0,0,0,0.06);
  --border-default: rgba(0,0,0,0.10);
  --border-strong:  rgba(0,0,0,0.18);
  --accent-primary: #6e56cf;
  --accent-primary-dim: rgba(110, 86, 207, 0.10);
}
```

### 6.2 Typography

**Font:** Inter, loaded via `next/font/google` with `display: swap` for performance.

| Role | Size | Weight | Line Height | Color |
|------|------|--------|-------------|-------|
| Page title | 24px | 600 | 1.2 | `--text-primary` |
| Section heading | 16px | 600 | 1.3 | `--text-primary` |
| Body / chat text | 15px | 400 | 1.7 | `--text-primary` |
| Label / UI chrome | 13px | 500 | 1.4 | `--text-secondary` |
| Caption / timestamp | 11px | 400 | 1.4 | `--text-muted` |
| Code blocks | 13px | 400 | 1.6 | `--text-primary` |

**Rules:**
- Minimum font size: 11px (captions only). Nothing below 11px.
- Use `font-weight: 600` only for headings and agent badges. Avoid 700 — too heavy.
- Sentence case everywhere. No ALL CAPS except badge abbreviations (3 chars max, e.g. "RAG").
- Letter spacing: `0.3px` on labels and badges only. Zero everywhere else.

### 6.3 Spacing Scale

Use a consistent 4px base unit. All spacing values must be multiples of 4.

```
4px   → xs  (icon-to-label gap)
8px   → sm  (within-component internal gap)
12px  → md  (between related elements)
16px  → lg  (section internal padding)
20px  → xl  (component external padding)
24px  → 2xl (section separation)
32px  → 3xl (major layout sections)
48px  → 4xl (page-level separation)
```

### 6.4 Border Radius

```
4px  → Chips, tags, small badges
8px  → Buttons, inputs, small cards
12px → Cards, panels, dropdowns
16px → Large cards, drawers
20px → Pill buttons, chat bubbles (large curve)
50%  → Avatar circles, status dots
```

### 6.5 Shadows

```css
/* Elevation 1 — Cards */
box-shadow: 0 1px 3px rgba(0,0,0,0.3), 0 1px 2px rgba(0,0,0,0.2);

/* Elevation 2 — Dropdowns, tooltips */
box-shadow: 0 4px 12px rgba(0,0,0,0.4), 0 2px 6px rgba(0,0,0,0.3);

/* Elevation 3 — Drawers, modals */
box-shadow: 0 8px 30px rgba(0,0,0,0.5);

/* Focus ring — accessible keyboard navigation */
box-shadow: 0 0 0 2px var(--accent-primary);
```

### 6.6 Iconography

Use **Lucide React** exclusively. Icon sizing rules:
- Navigation icons: `16px × 16px`, stroke `1.5px`
- Action buttons: `16px × 16px`, stroke `1.5px`
- Empty states / decorative: `32px × 32px`, stroke `1px`
- Inline text icons: `14px × 14px`

Never use emoji in the UI chrome. Emoji only allowed inside user-typed messages.

---

## 7. Layout & Grid System

### 7.1 Overall Layout

```
┌────────────────────────────────────────────────────────────┐
│                    TOP NAVBAR (48px)                        │
├──────────┬─────────────────────────────────┬───────────────┤
│          │                                 │               │
│  LEFT    │         MAIN CONTENT            │  RIGHT DRAWER │
│ SIDEBAR  │           AREA                  │  (collapsible)│
│  260px   │          (flex-grow)            │    300px      │
│  fixed   │                                 │   overlay     │
│          │                                 │               │
│          ├─────────────────────────────────┤               │
│          │       CHAT INPUT BAR (72px)     │               │
└──────────┴─────────────────────────────────┴───────────────┘
```

- **Top Navbar:** `position: fixed; top: 0; left: 0; right: 0; height: 48px; z-index: 50`
- **Left Sidebar:** `position: fixed; top: 48px; left: 0; bottom: 0; width: 260px; overflow-y: auto; z-index: 40`
- **Main Content:** `margin-left: 260px; margin-top: 48px; height: calc(100vh - 48px); display: flex; flex-direction: column`
- **Chat Window:** `flex: 1; overflow-y: auto` (only this scrolls)
- **Chat Input Bar:** `position: sticky; bottom: 0; height: 72px`
- **Right Drawer:** `position: fixed; top: 48px; right: 0; bottom: 0; width: 300px; z-index: 45; transform: translateX(100%)` (slides in on toggle)

### 7.2 Content Max Width

The chat message area should have a maximum readable width:
```css
.message-container {
  max-width: 760px;
  margin: 0 auto;
  padding: 0 24px;
}
```

This prevents messages from becoming unreadably wide on large monitors.

---

## 8. Component Specifications

### 8.1 Top Navigation Bar

**Dimensions:** Full width, 48px height  
**Background:** `var(--bg-panel)`  
**Border:** `border-bottom: 1px solid var(--border-subtle)`

**Left section (logo area):**
- Rocket icon SVG (16×16) in `--accent-primary` color
- App name: "NovaMind" or "AgentOS" — 14px, weight 600, `--text-primary`
- Separator: `·` in `--text-muted`
- Breadcrumb: "Workspace" — 13px, weight 400, `--text-secondary`

**Center section (tab navigation):**
- Tab items: Chat, Memory Board, Documents, Debug
- Each tab: `padding: 4px 14px; border-radius: 20px; font-size: 13px; font-weight: 500; cursor: pointer`
- Inactive tab: `color: --text-secondary; background: transparent`
- Active tab: `color: white; background: --accent-primary`
- Hover on inactive: `background: --bg-elevated; color: --text-primary`
- Transition: `all 0.15s ease`
- Tabs container: `display: flex; gap: 4px; align-items: center`

**Right section:**
- Live status indicator: green pulsing dot (8px circle, `background: --color-success`) + "Multi-agent" label (12px, `--text-secondary`)
- Icon button: Settings (gear icon) — `16px icon, 32×32px clickable area, border-radius: 6px, hover: bg-elevated`
- "Deploy" button: `border: 1px solid --border-default; background: transparent; border-radius: 6px; padding: 5px 12px; font-size: 13px; font-weight: 500; color: --text-primary; hover: border-strong, bg-card`

**Pulsing dot animation:**
```css
@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.85); }
}
.status-dot {
  animation: pulse-dot 2s ease-in-out infinite;
}
```

---

### 8.2 Left Sidebar

**Dimensions:** 260px wide, full height minus navbar  
**Background:** `var(--bg-panel)`  
**Border:** `border-right: 1px solid var(--border-subtle)`  
**Padding:** `16px 14px`  
**Overflow:** `overflow-y: auto` with hidden scrollbar on non-hover, visible on hover

**Section: Live Status Metrics**

Three metric tiles arranged in a 2+1 grid layout:
- Tile container: `background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 10px 12px`
- Label: 11px, weight 500, `--text-muted`, letter-spacing 0.3px
- Value: 20px, weight 600, `--text-primary`
- Memory tile: shows count + Brain icon (16px, `--accent-primary`)
- Docs tile: shows count + FileText icon (16px, `--color-info`)
- Mode tile: shows mode name as a badge — `background: --accent-primary-dim; color: --accent-primary; border-radius: 4px; font-size: 11px; padding: 2px 6px`

**Divider:**
- `border-top: 1px solid var(--border-subtle); margin: 14px 0`

**Section: Workspace Actions**

Three full-width ghost buttons stacked vertically with `gap: 6px`:
- Button style: `width: 100%; display: flex; align-items: center; gap: 8px; padding: 8px 10px; border-radius: 8px; border: 1px solid var(--border-subtle); background: transparent; font-size: 13px; font-weight: 500; color: var(--text-secondary); cursor: pointer`
- Hover: `border-color: var(--border-default); background: var(--bg-card); color: var(--text-primary)`
- Active/press: `scale(0.98)` transform
- Transition: `all 0.15s ease`
- Icons: Trash2 (Clear Conversation), Brain (Clear Memory), FileX (Clear Documents) — all 14px

**Section: Auto-save Toggle**

Custom toggle switch component — do NOT use a native `<input type="checkbox">` unstyled:
- Toggle container: `display: flex; align-items: center; justify-content: space-between; padding: 8px 0`
- Label: 13px, `--text-secondary`
- Switch: 32px × 18px pill shape
  - OFF state: `background: var(--bg-elevated); border: 1px solid var(--border-default)`
  - ON state: `background: var(--accent-primary); border: 1px solid transparent`
  - Thumb: 14px circle, `background: white`, transitions `transform: translateX(0)` → `translateX(14px)`
  - Transition: `all 0.2s ease`

**Section: Memory Notes**

- Section label: 12px, weight 600, `--text-muted`, letter-spacing 0.3px, uppercase → "MEMORY NOTES"
- Textarea: `width: 100%; min-height: 80px; background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 10px 12px; font-size: 13px; color: var(--text-primary); resize: vertical`
- Placeholder: "Capture a note for future context..." in `--text-muted`
- Hover: `border-color: var(--border-default)`
- Focus: `border-color: var(--accent-primary); outline: none; box-shadow: 0 0 0 2px var(--accent-primary-dim)`
- Save button: full-width, `background: var(--accent-primary); color: white; border-radius: 8px; padding: 7px; font-size: 13px; font-weight: 500; border: none; cursor: pointer`
- Save button hover: `background: var(--accent-primary-hover)`
- Save button icon: Save (14px) + label "Save Note"

---

### 8.3 Chat Window

The chat window is the core feature — it must look and feel exceptional.

**Container:**
- `flex: 1; overflow-y: auto; padding: 24px 0 0`
- Scrollbar: styled thin (4px wide), `--bg-elevated` track, `--border-default` thumb, visible only on hover

**Chat session header (inside main area, top):**
- Title: "Workspace Chat" — 16px, weight 600, `--text-primary`
- Subtitle: `{memoryCount} memories · {docCount} documents · {mode} mode` — 13px, `--text-secondary`
- Separator: `border-bottom: 1px solid var(--border-subtle); margin-bottom: 20px`

**Message List:**
- Container: `display: flex; flex-direction: column; gap: 4px; padding-bottom: 16px`
- Each message group (same sender sequence): `gap: 2px`
- Between different senders: `margin-top: 16px`

**User Message Bubble:**
```
Alignment:  Right (justify-content: flex-end)
Max-width:  68% of container
Background: var(--accent-primary)
Color:      white
Padding:    10px 16px
Border-radius: 18px 18px 4px 18px
Font-size:  15px, weight 400, line-height 1.6
```
- Timestamp: 10px, `rgba(255,255,255,0.5)`, `text-align: right`, `margin-top: 4px`

**Assistant Message Bubble:**
```
Alignment:  Left (justify-content: flex-start)
Max-width:  80% of container
Background: var(--bg-card)
Color:      var(--text-primary)
Border:     1px solid var(--border-subtle)
Padding:    12px 16px
Border-radius: 18px 18px 18px 4px
Font-size:  15px, weight 400, line-height 1.7
```
- Agent badge (above bubble, `margin-bottom: 4px`):
  - General Agent: `background: var(--accent-primary-dim); color: var(--accent-primary); font-size: 10px; font-weight: 600; letter-spacing: 0.5px; padding: 2px 8px; border-radius: 10px` — text: "GENERAL AGENT"
  - RAG Agent: `background: var(--color-success-dim); color: var(--color-success)` — text: "RAG AGENT"
  - Code Agent: `background: var(--color-info-dim); color: var(--color-info)` — text: "CODE AGENT"
- Timestamp: 10px, `--text-muted`, `margin-top: 6px`
- Markdown rendering: support `**bold**`, `` `code` ``, `code blocks`, bullet lists inside bubbles. Code blocks: `background: var(--bg-elevated); border-radius: 6px; padding: 12px; font-family: monospace; font-size: 13px; overflow-x: auto`

**Hover action toolbar (on assistant messages):**
- Appears `0.15s` after hover begins, fades in
- Position: `absolute; top: -32px; right: 0`
- Container: `background: var(--bg-elevated); border: 1px solid var(--border-default); border-radius: 8px; display: flex; gap: 2px; padding: 4px`
- Buttons: Copy, Regenerate, Recall Memory — icon only (14px), `padding: 5px; border-radius: 4px; hover: bg-card`
- Tooltip on hover: small text below icon

**Typing indicator (when agent is responding):**
- Shows as an assistant-style bubble with no text, just three animated dots
- Dots: `width: 6px; height: 6px; border-radius: 50%; background: var(--text-muted)`
- Animation: staggered fade+scale, `0s, 0.2s, 0.4s` delay respectively
```css
@keyframes typing-dot {
  0%, 80%, 100% { transform: scale(0.7); opacity: 0.4; }
  40% { transform: scale(1); opacity: 1; }
}
```

---

### 8.4 Chat Input Bar

This is a critical UX component — it must feel premium.

**Outer container:**
- `position: sticky; bottom: 0; background: var(--bg-base); border-top: 1px solid var(--border-subtle); padding: 12px 24px 14px`

**Inner input wrapper:**
- `background: var(--bg-card); border: 1px solid var(--border-default); border-radius: 14px; display: flex; align-items: flex-end; gap: 8px; padding: 10px 12px`
- Focus-within: `border-color: var(--accent-primary); box-shadow: 0 0 0 3px var(--accent-primary-dim)`
- Transition: `all 0.15s ease`

**Textarea (not input — allows multiline):**
- `flex: 1; background: transparent; border: none; outline: none; resize: none; font-size: 15px; color: var(--text-primary); line-height: 1.5; min-height: 24px; max-height: 160px; overflow-y: auto`
- Placeholder: "Ask anything..." in `--text-muted`
- Auto-grows with content (JS: `textarea.style.height = textarea.scrollHeight + 'px'`)
- Enter to send, Shift+Enter for newline

**Left icon buttons (inside input wrapper):**
- Paperclip icon (attach document): 16px, `--text-muted`, hover: `--text-secondary`, `border-radius: 6px; padding: 4px`

**Right section:**
- Send button (enabled when input not empty):
  - Enabled: `background: var(--accent-primary); color: white; border-radius: 8px; padding: 6px 10px; border: none; cursor: pointer`
  - Disabled: `background: var(--bg-elevated); color: var(--text-muted); cursor: not-allowed`
  - Icon: ArrowUp (16px)
  - Hover when enabled: `background: var(--accent-primary-hover); transform: scale(1.05)`
  - Transition: `all 0.15s ease`

**Below input:**
- `text-align: center; font-size: 11px; color: var(--text-muted); margin-top: 8px`
- Text: "NovaMind uses Claude · Responses may be inaccurate"

---

### 8.5 Memory Board Panel (Tab View)

When the user clicks the "Memory Board" tab, the main content area switches to this view (full width, replaces chat).

**Layout:**
- Page header: "Memory Board" (20px, weight 600) + count badge + "Clear All" button (right-aligned, ghost style)
- Search bar: full-width, `background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 9px 12px; font-size: 14px`; Search icon (Lucide) as leading icon inside
- Memory item list below

**Memory item card:**
- `background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 12px 14px; display: flex; align-items: flex-start; gap: 12px`
- Hover: `border-color: var(--border-default); background: var(--bg-elevated)`
- Left: index number in a 24×24 circle, `background: var(--accent-primary-dim); color: var(--accent-primary); font-size: 11px; font-weight: 600; border-radius: 50%`
- Content: memory text (14px, `--text-primary`), truncated to 2 lines with "..." if long, expandable on click
- Right: timestamp (11px, `--text-muted`) + delete icon button (Trash2, 14px, appears on hover)

---

### 8.6 Documents Panel (Tab View)

**Layout:**
- Page header: "Documents" (20px, weight 600) + count badge
- Upload dropzone:
  - `border: 2px dashed var(--border-default); border-radius: 12px; padding: 32px; text-align: center; background: var(--bg-card)`
  - Drag-over state: `border-color: var(--accent-primary); background: var(--accent-primary-dim)`
  - Icon: UploadCloud (32px, `--text-muted`)
  - Text: "Drop files here or click to upload" (14px, `--text-secondary`)
  - Subtext: "Supports PDF, TXT, DOCX" (12px, `--text-muted`)
- Document grid: `display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; margin-top: 16px`

**Document card:**
- `background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: 10px; padding: 14px`
- File type icon (24px, colored by type: PDF=red, TXT=blue, DOCX=blue)
- Filename (13px, weight 500, truncated)
- File size (11px, `--text-muted`)
- Delete button on hover: top-right X icon

---

### 8.7 Debug Panel (Tab View)

- Raw JSON display using a monospace code block styled with `background: var(--bg-card); border-radius: 10px; padding: 16px; overflow-x: auto; font-size: 12px; font-family: var(--font-mono); color: var(--text-primary); line-height: 1.6`
- JSON syntax highlighting: keys in `--accent-primary`, strings in `--color-success`, numbers in `--color-warning`, null/bool in `--color-error`
- Copy button: top-right of code block
- Auto-scrolls to latest log entry

---

### 8.8 Right Drawer

**Trigger:** Clicking settings/info icons in the top navbar  
**Behavior:** Slides in from right, overlays main content with a dark backdrop

**Backdrop:** `position: fixed; inset: 0; background: var(--bg-overlay); z-index: 44; opacity: 0 → 1 on open`

**Drawer panel:**
```css
position: fixed;
top: 48px;
right: 0;
bottom: 0;
width: 300px;
z-index: 45;
background: var(--bg-panel);
border-left: 1px solid var(--border-subtle);
transform: translateX(100%); /* closed */
transform: translateX(0);    /* open */
transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
```

**Drawer header:**
- Title (14px, weight 600) + Close button (X icon, 16px) on the right
- `border-bottom: 1px solid var(--border-subtle); padding: 14px 16px`

**Settings drawer content:**
- Model selection: labeled dropdown (`claude-3-5-sonnet`, `claude-3-haiku`, etc.)
- Temperature slider: range 0–1, step 0.1, custom styled thumb
- Mode toggle: Multi-agent / Single-agent
- All form controls follow the same consistent style as sidebar toggles

---

## 9. Page-by-Page Breakdown

### 9.1 Initial Load State

When the page first loads with no conversation history:
- Chat area shows a centered welcome state (not a message bubble):
  - Large icon (48px, agent-colored)
  - Heading: "How can I help you today?" (22px, weight 600)
  - Subtext: "Powered by multi-agent AI with persistent memory and document recall." (15px, `--text-secondary`)
  - Three suggestion chips below (quick-start prompts): `border: 1px solid var(--border-default); border-radius: 20px; padding: 8px 16px; font-size: 13px; cursor: pointer; hover: bg-card`

### 9.2 Active Conversation State

- Welcome state disappears, replaced by the message list
- Messages animate in on arrival (`fadeSlideIn` animation, see Section 10)
- If the agent is responding, typing indicator appears at the bottom of the list

### 9.3 Empty States

**Memory Board (empty):**
- Brain icon (32px, `--text-muted`)
- "No memories yet" (16px, weight 500)
- "Start a conversation and enable auto-save to build memory." (14px, `--text-secondary`)

**Documents (empty):**
- FolderOpen icon (32px, `--text-muted`)
- "No documents indexed"
- "Upload a PDF or text file to enable RAG-powered Q&A."

---

## 10. Interaction Design & Animations

All animations should be purposeful — they must either convey state change or improve perceived performance. No decorative animations.

### 10.1 Animation Specifications

| Interaction | Animation | Duration | Easing |
|-------------|-----------|----------|--------|
| New message appears | `fadeSlideIn`: opacity 0→1, translateY 8px→0 | 200ms | `ease-out` |
| Tab switch | Content area fade: opacity 0→1 | 150ms | `ease` |
| Right drawer open | `translateX(100% → 0)` | 250ms | `cubic-bezier(0.4, 0, 0.2, 1)` |
| Right drawer close | `translateX(0 → 100%)` | 200ms | `ease-in` |
| Button hover | `scale(1 → 1.02)` or background color change | 150ms | `ease` |
| Button press | `scale(0.98)` | 80ms | `ease` |
| Send button enable | opacity 0.4→1, color change | 150ms | `ease` |
| Typing indicator | Staggered dot bounce | 1.2s loop | `ease-in-out` |
| Status dot pulse | opacity + scale oscillation | 2s loop | `ease-in-out` |
| Toast notification | `slideInFromTop`, auto-dismiss | 300ms in, 3s hold, 200ms out | `ease` |

### 10.2 Hover States

Every interactive element must have a visible hover state. Nothing should respond to hover without a visual change. Rule: use `transition: all 0.15s ease` on all interactive elements.

### 10.3 Focus States

Every focusable element (buttons, inputs, links) must have a visible focus ring for keyboard navigation:
```css
:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px var(--accent-primary);
  border-radius: inherit;
}
```

### 10.4 Loading States

- **Initial page load:** Show a skeleton loader for the sidebar metric tiles (shimmer animation: `background: linear-gradient(90deg, var(--bg-card) 0%, var(--bg-elevated) 50%, var(--bg-card) 100%); background-size: 200%; animation: shimmer 1.5s infinite`)
- **Agent responding:** Typing indicator in chat + send button disabled + input placeholder changes to "Agent is thinking..."
- **Document uploading:** Progress bar inside the document card (full-width, `height: 2px; background: var(--accent-primary)`)

### 10.5 Toast Notifications

For actions like "Memory saved", "Conversation cleared", "Note saved":
- Position: `top: 64px; right: 16px; z-index: 100`
- Style: `background: var(--bg-elevated); border: 1px solid var(--border-default); border-radius: 10px; padding: 10px 14px; display: flex; align-items: center; gap: 8px; box-shadow: Elevation 2`
- Icon: CheckCircle2 for success (green), AlertCircle for error (red)
- Text: 13px, `--text-primary`
- Auto-dismisses after 3 seconds
- Dismiss button: X (12px) on the right

---

## 11. Responsive Design

### 11.1 Breakpoints

```
Mobile:  < 768px
Tablet:  768px – 1024px
Desktop: > 1024px (primary target)
Wide:    > 1440px
```

### 11.2 Mobile (< 768px)

- Left sidebar collapses completely. Hidden by default.
- Hamburger icon (☰) appears in the top-left of the navbar — tapping it slides the sidebar in as an overlay (full-height, 80% screen width)
- Right drawer occupies 100% width when open
- Chat message max-width becomes 90%
- Tab labels shortened to icons only on mobile (no text)
- Chat input bar padding reduced to `8px 12px`
- Top navbar tabs hidden; show only logo + hamburger + send area

### 11.3 Tablet (768px – 1024px)

- Left sidebar shown but narrower: 220px
- Main content area adjusts `margin-left: 220px`
- Right drawer becomes a full overlay (doesn't push main content)
- Chat message max-width: 80%

### 11.4 Wide (> 1440px)

- Main chat area remains max-width 760px, centered in the content area
- Extra whitespace on left and right sides of chat — do not stretch messages

---

## 12. Accessibility

### 12.1 WCAG 2.1 AA Requirements

- All text must meet contrast ratio ≥ 4.5:1 against its background
- Interactive elements must be reachable via keyboard Tab navigation
- All icons must have `aria-label` or accompanying visible text
- Focus indicators must be visible and high-contrast
- Images and icon-only buttons require `aria-label` or `title`

### 12.2 Semantic HTML

```html
<!-- Use semantic elements -->
<nav> for top navbar and tab navigation
<main> for the main content area
<aside> for the sidebar
<button> for all clickable actions (not <div onClick>)
<form> for the chat input area
<ul> + <li> for message list and memory list
<article> for each message bubble
<time datetime="..."> for timestamps
<h1>, <h2>, <h3> in correct hierarchy — never skip heading levels
```

### 12.3 Aria Attributes

- Chat input: `aria-label="Chat message input" aria-multiline="true"`
- Send button: `aria-label="Send message"` when icon-only
- Memory items: `aria-label="Memory item {index}: {first 50 chars}"`
- Tab navigation: `role="tablist"`, `role="tab"`, `role="tabpanel"`, `aria-selected`, `aria-controls`
- Right drawer: `role="dialog"`, `aria-modal="true"`, `aria-labelledby` pointing to drawer heading
- Status indicator: `aria-live="polite"` on the agent status area so screen readers announce mode changes

### 12.4 Keyboard Navigation

- `Tab` / `Shift+Tab`: cycle through interactive elements
- `Enter` / `Space`: activate buttons
- `Escape`: close right drawer, dismiss tooltips
- `Arrow keys`: navigate tabs in the top navbar (`role="tablist"`)
- `Ctrl+Enter` or `Cmd+Enter` (alternative): send message

---

## 13. Performance Requirements

### 13.1 Core Web Vitals Targets

| Metric | Target |
|--------|--------|
| LCP (Largest Contentful Paint) | < 2.5s |
| FID (First Input Delay) | < 100ms |
| CLS (Cumulative Layout Shift) | < 0.1 |
| TTFB (Time to First Byte) | < 600ms |

### 13.2 Implementation Requirements

- **Font loading:** Use `next/font/google` with `display: swap` to prevent FOUT blocking render
- **No layout shift:** Reserve fixed dimensions for sidebar metrics tiles and avatar placeholders using skeleton loaders during data fetch
- **Image optimization:** Use `next/image` for any images. All icons are inline SVG (via Lucide) — no image network requests for icons.
- **Code splitting:** Each tab panel (MemoryBoard, Documents, Debug) should be dynamically imported with `next/dynamic` so they don't inflate the initial bundle
- **Virtualization:** If the memory list exceeds 50 items, use `react-window` or `@tanstack/virtual` to virtualize the list — don't render 200 DOM nodes at once
- **Memoization:** Wrap `MessageBubble`, `MemoryItem`, `DocumentCard` in `React.memo` to prevent unnecessary re-renders on parent state changes

---

## 14. Error States & Edge Cases

### 14.1 API Error (Agent fails to respond)

- Show an error message bubble in assistant style: `border-color: var(--color-error); background: var(--color-error-dim)`
- Text: "Something went wrong. Please try again." + a "Retry" button
- Log the raw error to the Debug panel automatically

### 14.2 Empty Chat Input

- Send button remains disabled (greyed out) when input is whitespace-only
- No error shown — just prevent submission

### 14.3 Document Upload Failure

- Toast notification: error style (red icon) — "Failed to upload [filename]. Please check the file format."
- Remove the failed upload from the document list

### 14.4 Network Offline

- Show a non-dismissible banner below the navbar: `background: var(--color-warning-dim); color: var(--color-warning); text-align: center; padding: 8px; font-size: 13px` — "You appear to be offline. Messages will not send."
- Input bar disabled while offline

### 14.5 Very Long Messages

- Messages over ~1000 characters: show first 400 chars + "Show more" link in `--accent-primary`
- No automatic truncation for shorter messages

### 14.6 Code in Messages

- Detect triple backtick code blocks in agent responses
- Render with: syntax highlighting library (Prism.js or shiki), copy button top-right, language label top-left
- Code block container: `overflow-x: auto; max-width: 100%`

---

## 15. Out of Scope

The following are explicitly not included in this redesign sprint:

- **User authentication / login flow** — Assume a single-user deployment for the internship demo
- **Multi-user / collaborative features** — One user at a time
- **Mobile app** (iOS/Android native) — Web responsive only
- **Dark/light mode toggle** — Default to dark mode only for V1; light mode support in V2
- **Internationalization (i18n)** — English only
- **Voice input** — The microphone icon is decorative/placeholder in V1
- **End-to-end encryption** — Backend security is out of scope for UI PRD
- **Billing or plan management UI** — Not applicable for internship demo
- **Analytics dashboard** — Not applicable for V1

---

## Appendix A: Component Checklist

Use this checklist during development to verify all components are implemented:

- [ ] TopNav — logo, tabs, status dot, deploy button
- [ ] LeftSidebar — metrics tiles, action buttons, auto-save toggle, memory notes
- [ ] ChatWindow — message list, scroll behavior, welcome state, empty state
- [ ] MessageBubble (User) — right-aligned, purple, border-radius
- [ ] MessageBubble (Assistant) — left-aligned, with agent badge, hover toolbar
- [ ] TypingIndicator — three-dot animation
- [ ] ChatInputBar — auto-grow textarea, send button state, file attach
- [ ] MemoryBoardPanel — search, item cards, delete, empty state
- [ ] DocumentsPanel — dropzone, document grid cards, progress bar, empty state
- [ ] DebugPanel — JSON code block, syntax highlight, copy button
- [ ] RightDrawer — slide animation, backdrop, close on backdrop click
- [ ] SettingsDrawer — model select, temperature slider, toggles
- [ ] Toast notifications — success, error, auto-dismiss
- [ ] Skeleton loaders — sidebar metrics, initial load
- [ ] Focus rings — all interactive elements
- [ ] Keyboard navigation — Tab order, Escape, Arrow keys on tabs
- [ ] Responsive layout — 375px, 768px, 1440px tested

---

## Appendix B: Design Token Reference (Quick Copy)

```css
/* Paste into globals.css */
:root {
  --bg-base: #0a0a0f;
  --bg-panel: #12121a;
  --bg-card: #1c1c26;
  --bg-elevated: #252535;
  --text-primary: #e8e8f0;
  --text-secondary: #8888a8;
  --text-muted: #44445a;
  --border-subtle: rgba(255,255,255,0.06);
  --border-default: rgba(255,255,255,0.10);
  --border-strong: rgba(255,255,255,0.18);
  --accent-primary: #7c6af7;
  --accent-primary-dim: rgba(124,106,247,0.15);
  --accent-primary-hover: #9585f9;
  --color-success: #34c99a;
  --color-success-dim: rgba(52,201,154,0.12);
  --color-warning: #f5a623;
  --color-warning-dim: rgba(245,166,35,0.12);
  --color-error: #e24b4a;
  --color-error-dim: rgba(226,75,74,0.12);
  --color-info: #378add;
  --color-info-dim: rgba(55,138,221,0.12);
}
```

---

*End of PRD — Adaptive Multi-Agent AI Portal UI/UX Redesign v1.0*