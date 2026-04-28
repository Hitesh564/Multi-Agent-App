import { NextResponse } from 'next/server';

const API_BASE = 'http://127.0.0.1:8000';

export async function GET() {
  try {
    const res = await fetch(`${API_BASE}/api/status`);
    const data = await res.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch status' }, { status: 500 });
  }
}
