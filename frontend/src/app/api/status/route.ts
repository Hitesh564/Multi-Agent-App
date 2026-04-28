import { NextResponse } from 'next/server';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export async function GET() {
  try {
    const res = await fetch(`${API_BASE}/api/status`);
    const data = await res.json();
    return NextResponse.json(data);
  } catch (error: any) {
    return NextResponse.json({ 
      error: `Failed to proxy request to backend. URL used: ${API_BASE}. Exact error: ${error.message}` 
    }, { status: 500 });
  }
}
