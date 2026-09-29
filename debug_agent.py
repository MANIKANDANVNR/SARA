from main import create_sara

c = create_sara()
c.security.authenticate()

original = c.agent_runner.run

def debug_run(*args, **kwargs):
    task = original(*args, **kwargs)

    print("DEBUG STATUS:", task.status)
    print(
        "DEBUG STEP RESULT:",
        task.steps[0].result if task.steps else None
    )
    print("DEBUG TASK RESULT:", task.result)
    print("DEBUG ERROR:", task.error)
    print("DEBUG REPORT:", task.report)

    return task

c.agent_runner.run = debug_run

result = c.handle_agent(
    "Use the calculator tool to calculate 157 * 83. "
    "Return only the result."
)

print("FINAL:", result)
