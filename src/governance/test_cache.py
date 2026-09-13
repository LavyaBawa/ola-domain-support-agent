from src.governance.response_cache import ResponseCache


cache = ResponseCache()

llm_call_count = 0


def generate_response(query):
    global llm_call_count

    cached = cache.get(query)

    if cached is not None:
        print("CACHE HIT")
        return cached

    llm_call_count += 1
    print("LLM/GENERATION CALL")

    response = "Critical tickets have a 1 hour initial response target."

    cache.set(query, response)

    return response


query1 = "What is the SLA for a critical ticket?"
query2 = "  what is the SLA for a critical ticket?  "


print("FIRST REQUEST:")
print(generate_response(query1))

print("\nSECOND REQUEST:")
print(generate_response(query2))

print("\nGeneration calls:", llm_call_count)

assert llm_call_count == 1
assert generate_response(query1) == generate_response(query2)

print("\nResponse cache test passed.")
