from langchain_core.runnables import RunnableLambda

from src.memory.session_memory import build_memory_chain


def respond(data):
    history = data.get("history", [])

    if history:
        return (
            f"Previous conversation: {history[-1].content}\n"
            f"Current question: {data['input']}"
        )

    return f"Current question: {data['input']}"


base_runnable = RunnableLambda(respond)

memory_chain = build_memory_chain(base_runnable)


session_id = "demo-session"

print("TURN 1:")
result = memory_chain.invoke(
    {"input": "What is the SLA for a critical ticket?"},
    config={"configurable": {"session_id": session_id}},
)
print(result)

print("\nTURN 2:")
result = memory_chain.invoke(
    {"input": "And what about a low priority ticket?"},
    config={"configurable": {"session_id": session_id}},
)
print(result)

print("\nNEW SESSION:")
result = memory_chain.invoke(
    {"input": "What did I ask previously?"},
    config={"configurable": {"session_id": "new-session"}},
)
print(result)
