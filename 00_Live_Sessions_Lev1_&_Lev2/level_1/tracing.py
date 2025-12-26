# # from agents import Agent, Runner, function_tool, trace, agent_span
# # from dotenv import load_dotenv
# # from agents.tracing.processors import ConsoleSpanExporter, BatchTraceProcessor, TracingProcessor
# # from agents.tracing import add_trace_processor

# # # console_exporter = ConsoleSpanExporter()
# # # console_processor = BatchTraceProcessor(console_exporter)
# # # add_trace_processor(console_processor)

# # class CustomProcessor(TracingProcessor):
# #     def __init__(self):
# #         self.active_traces = {}
# #         self.active_spans = {}

# #     def on_trace_start(self, trace):
# #         self.active_traces[trace.trace_id] = trace
# #         print(f"Trace started: {trace.name} (ID: {trace.trace_id})")

# #     def on_trace_end(self, trace):
# #         print(f"Trace ended: {trace.name} (ID: {trace.trace_id}, Duration: {trace.end_time - trace.start_time} seconds)")
# #         del self.active_traces[trace.trace_id]

# #     def on_span_start(self, span):
# #         self.active_spans[span.span_id] = span
# #         print(f"Span started: {span.name} (ID: {span.span_id}, Type: {span.span_data.type})")

# #     def on_span_end(self, span):
# #         print(f"Span ended: {span.name} (ID: {span.span_id}, Duration: {span.end_time - span.start_time} seconds)")
# #         del self.active_spans[span.span_id]

# #     def shutdown(self):
# #         self.active_traces.clear()
# #         self.active_spans.clear()
# #         print("Processor shut down")

# #     def force_flush(self):
# #         pass  # No queued items to flush in this example

# # custom_processor = CustomProcessor()
# # add_trace_processor(custom_processor)

# # load_dotenv()

# # @function_tool
# # def get_weather(city:str):
# #     """get weather for given city"""

# #     return f"the current weather in {city} is cloudy"


# # main_agent = Agent(
# #     name="Assistant",
# #     instructions="you are helpfull assistant",
# #     tools=[get_weather]
# # )

# # try :
# #     with trace(workflow_name="kaladi"):
# #         result = Runner.run_sync(
# #         main_agent,
# #         "what is current weather in karachi ?",
# # )
# #     print(result.final_output)

# # except Exception as ae:
# #     print(f"Exception raise {ae}")




# from agents import Agent, Runner, function_tool, trace, agent_span
# from dotenv import load_dotenv
# from agents.tracing.processors import ConsoleSpanExporter, BatchTraceProcessor, TracingProcessor
# from agents.tracing import add_trace_processor

# # Define CustomProcessor
# class CustomProcessor(TracingProcessor):
#     def __init__(self):
#         self.active_traces = {}
#         self.active_spans = {}

#     def on_trace_start(self, trace):
#         print(f"TRACE START: id={trace.trace_id}, name={trace.name}")
        
#     def on_trace_end(self, trace):
#         # Process completed trace
#         print(f"TRACE END: id={trace.trace_id}, name={trace.name}, export={trace.export()}")

#     def on_span_start(self, span):
#         print(f"SPAN START: id={span.span_id}, trace_id={span.trace_id}, data={span.span_data}")

#     def on_span_end(self, span):
#         # Process completed span
#         print(f"SPAN END: id={span.span_id}, trace_id={span.trace_id}")

#     def shutdown(self):
#         # Clean up resources
#         self.active_traces.clear()
#         self.active_spans.clear()

#     def force_flush(self):
#         # Force processing of any queued items
#         pass

# # Set up tracing
# custom_processor = CustomProcessor()
# add_trace_processor(custom_processor)

# load_dotenv()

# @function_tool
# def get_weather(city: str):
#     """get weather for given city"""
#     return f"the current weather in {city} is cloudy"

# main_agent = Agent(
#     name="Assistant",
#     instructions="you are helpful assistant",
#     tools=[get_weather]
# )

# try:
#     with trace(workflow_name="kaladi"):
#         result = Runner.run_sync(
#             main_agent,
#             "what is current weather in karachi ?",
#         )
#         print(result.final_output)
# except Exception as ae:
#     print(f"Exception raised: {ae}")



# from agents import Agent, Runner, function_tool, trace
# from dotenv import load_dotenv

# load_dotenv()



# @function_tool
# def get_weather(city:str):
#     """get weather for given city"""

#     return f"the current weather in {city} is cloudy"


# main_agent = Agent(
#     name="Assistant",
#     instructions="you are helpfull assistant",
#     tools=[get_weather]
# )

# with trace(workflow_name="kaladi"):
#         result = Runner.run_sync(
#         main_agent,
#         "what is current weather in hyd ?",
#         )
#         print(result.final_output)






# from agents import Agent, Runner, function_tool, trace
# from dotenv import load_dotenv

# load_dotenv()

# @function_tool
# def get_weather(city: str):
#     """get weather for given city"""
#     return f"The current weather in {city} is cloudy"

# # Agent banate hain
# main_agent = Agent(
#     name="Assistant",
#     instructions="You are a helpful assistant",
#     tools=[get_weather]
# )

# # Trace manually banate hain (context manager ke bagair)
# trace = trace(workflow_name="kld")

# # 1️⃣ Start the trace manually
# trace.start(mark_as_current=True)
# print("Trace started:", trace.trace_id)

# try:
#     # Agent ko run karte hain
#     result = Runner.run_sync(main_agent, "what is current weather in hyd ?")
#     print("Agent output:", result.final_output)

# finally:
#     # 2️⃣ Trace ko finish karte hain
#     trace.finish(reset_current=False)
#     print("Trace finished:", trace.trace_id)

#     # 3️⃣ Export the trace data (dict form)
#     exported = trace.export()
#     print("Exported trace data:", exported)

from agents import Agent, Runner, function_tool, trace
from dotenv import load_dotenv

load_dotenv()

@function_tool
def get_weather(city: str):
    return f"The current weather in {city} is cloudy"

main_agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    tools=[get_weather]
)

t = trace(workflow_name="kld1")
t.start(mark_as_current=True)

print("Trace started:", t.trace_id)

# --- Agent run ---
result = Runner.run_sync(main_agent, "what is current weather in hyd ?")
print("Agent output:", result.final_output)

t.finish(reset_current=True)



result2 = Runner.run_sync(
    main_agent,
    "hello"
)
print(result2.final_output)