from agents import Runner, custom_span
from agents.tracing import trace

with trace(workflow_name="kaladi", metadata={"user_id": "123", "session": "abc"}) as t:
    print("Trace started:", t.trace_id)







from agents.tracing import get_current_trace, get_current_span


with trace(workflow_name="kaladi"):
    print("Current trace:", get_current_trace().trace_id)
    with custom_span("Normalization"):
        print("Current span:", get_current_span().span_id)
        result = Runner.run_sync(
        # main_agent,
        "what is current weather in hyd ?",
        )
        print(result.final_output)