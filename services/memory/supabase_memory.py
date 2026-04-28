from services.memory.supabase_client import supabase

def save_message(session_id, role, content):
    supabase.table("messages").insert({
        "session_id": session_id,
        "role": role,
        "content": content
    }).execute()


def load_messages(session_id):
    res = supabase.table("messages") \
        .select("*") \
        .eq("session_id", session_id) \
        .order("created_at") \
        .execute()

    return res.data if res.data else []