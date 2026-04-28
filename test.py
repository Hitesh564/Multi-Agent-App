from services.app_factory import build_system

system = build_system()
router = system["router"]
llm_agent = system["llm_agent"]
rag_agent = system["rag_agent"]
tool_agent = system["tool_agent"]

print("\n--- Testing Router ---\n")
try:
    prompts = [
        "What is the weather in London?",
        "What is the price of AAPL stock?",
        "Explain quantum computing.",
        "What does the uploaded PDF say about architecture?"
    ]
    for p in prompts:
        print(f"Prompt: {p}")
        category = router.classify(p)
        print(f"Category: {category}")
        if category == "TOOL":
            resp = tool_agent.handle(p)
            print(f"Response: {resp}")
        elif category == "RAG":
            # For RAG, let's just test without an actual PDF
            resp = rag_agent.handle(p)
            print(f"Response: {resp}")
        else:
            resp = llm_agent.handle(p)
            print(f"Response: {resp}")
        print("-----")
except Exception as e:
    import traceback
    traceback.print_exc()
