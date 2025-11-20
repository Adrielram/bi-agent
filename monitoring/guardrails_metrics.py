from prometheus_client import Counter

# Guardrails metrics
guard_input_blocked_total = Counter(
    'bi_agent_guard_input_blocked_total',
    'Total number of user inputs blocked by guardrails or validators'
)

guard_output_redacted_total = Counter(
    'bi_agent_guard_output_redacted_total',
    'Total number of outputs redacted by guardrails or validators'
)

guard_tool_redacted_total = Counter(
    'bi_agent_guard_tool_redacted_total',
    'Total number of tool outputs redacted by guardrails or validators'
)
