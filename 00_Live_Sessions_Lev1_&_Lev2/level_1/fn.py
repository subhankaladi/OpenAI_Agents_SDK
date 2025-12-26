from agents import HandoffInputData, RunItem, ToolCallItem, ToolCallOutputItem

def remove_function_calls(data: HandoffInputData) -> HandoffInputData:
    """Remove all function_call and function_call_output items from history and items."""
    
    def filter_history(items):
        if not isinstance(items, tuple):
            return items
        return tuple(
            item for item in items
            if item.get("type") not in ["function_call", "function_call_output"]
        )

    def filter_items(items: tuple[RunItem, ...]):
        return tuple(
            item for item in items
            if not isinstance(item, (ToolCallItem, ToolCallOutputItem))
        )

    return HandoffInputData(
        input_history=filter_history(data.input_history),
        pre_handoff_items=filter_items(data.pre_handoff_items),
        new_items=filter_items(data.new_items),
    )
