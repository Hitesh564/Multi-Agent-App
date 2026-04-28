import { NextResponse } from 'next/server';

const API_BASE = 'http://127.0.0.1:8000';

export async function GET() {
  try {
    const res = await fetch(`${API_BASE}/api/memory`);
    const data = await res.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ error: 'Failed to fetch memory' }, { status: 500 });
  }
}

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const res = await fetch(`${API_BASE}/api/memory/add`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ error: 'Failed to add memory' }, { status: 500 });
  }
}

export async function DELETE() {
  try {
    const res = await fetch(`${API_BASE}/api/memory/clear`, {
      method: 'POST',
    });
    const data = await res.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json({ error: 'Failed to clear memory' }, { status: 500 });
  }
}
