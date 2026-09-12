# ============================================================
# 1. Greeting Workflow
# ============================================================
#
# Create a graph that receives a person's name and returns:
#
# "Hello, Saurabh! Welcome to LangGraph."
#
# Use one node and connect it from START to END.

# WRITE YOUR SOLUTION BELOW
# ------------------------------------------------------------
from typing import TypedDict
from langgraph.graph import StateGraph, END, START


class GreetingState(TypedDict):
    name: str
    output_message: str

def greetings_node(state: GreetingState) -> dict:
    return {"output_message": f"Hello, {state['name']}! Welcome to LangGraph."}

workflow = StateGraph(GreetingState)

workflow.add_node("greeting_message", greetings_node)

workflow.add_edge(START, "greeting_message")
workflow.add_edge("greeting_message", END)

app = workflow.compile()

# Invoke the compiled app, not the uncompiled workflow
result = app.invoke({"name": "Saurabh"})
print(result)
    


# ============================================================
# 2. Two-Step Greeting
# ============================================================
#
# Create a graph that:
# - Takes a person's name.
# - First node creates a greeting.
# - Second node adds a welcome message.
# - Returns the final message.

# WRITE YOUR SOLUTION BELOW
# ------------------------------------------------------------
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class Greeting(TypedDict):
    name: str
    output: str

def greet_step(state: Greeting) -> dict:
    return {"output": f"Hello, {state['name']}!"}

def welcome_step(state: Greeting) -> dict:
    return {"output": f"{state['output']} Welcome to LangGraph."}

graph = StateGraph(Greeting)

graph.add_node("greeting_message", greet_step)
graph.add_node("welcome_message", welcome_step)

graph.add_edge(START, "greeting_message")
graph.add_edge("greeting_message", "welcome_message")
graph.add_edge("welcome_message", END)

agent = graph.compile()

print(agent.invoke({"name": "Saurabh"}))

# ============================================================
# 3. Personal Introduction
# ============================================================
#
# Create a graph that receives:
# - Name
# - Age
# - City
#
# Use separate nodes to:
# 1. Create a basic introduction.
# 2. Add the person's city.
# 3. Return the final introduction.

# WRITE YOUR SOLUTION BELOW
# ------------------------------------------------------------
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class PersonalInfo(TypedDict):
    name: str
    age: int
    city: str
    output: str

def basic_info(state: PersonalInfo)->dict:
    return {"output":f"Hi my name is {state['name']}. I am {state['age']} year old"}

def add_city(state: PersonalInfo) -> dict:
    return {"output": f"{state['output']}, and i live in {state['city']}"}

workflow = StateGraph(PersonalInfo)

workflow.add_node("basic_info", basic_info)
workflow.add_node("add_city", add_city)

workflow.add_edge(START, "basic_info")
workflow.add_edge("basic_info", "add_city")
workflow.add_edge("add_city", END)

graph = workflow.compile()

print(graph.invoke({"name":"Saurabh Kumar", "age": 23, "city": "Begusarai"}))

# ============================================================
# 4. Text Processing Workflow
# ============================================================
#
# Create a graph that receives a sentence and processes it through:
#
# Input → Clean Text → Convert Text → Final Output
#
# Example:
# " hello WORLD " → "hello world"

# WRITE YOUR SOLUTION BELOW
# ------------------------------------------------------------
from typing import TypedDict
from langgraph.graph import StateGraph, START, END 

class TextState(TypedDict):
    raw_text : str
    cleaned_text: str
    final_output: str

def clean_text(state: TextState)-> dict:
    return {"cleaned_text": state['raw_text'].strip()}
    

def convert_text(state: TextState)-> dict:
    return {"final_output": state["cleaned_text"].lower()}

workflow = StateGraph(TextState)

workflow.add_node("clean", clean_text )
workflow.add_node("convert", convert_text )

workflow.add_edge(START, "clean")
workflow.add_edge("clean", "convert")
workflow.add_edge("convert", END)

graph = workflow.compile()

result = graph.invoke({"raw_text": " my name is sauraBh "})
print(result["final_output"])  # Outputs: "my name is saurabh"

# ============================================================
# 5. Simple Calculator Graph
# ============================================================
#
# Create a graph that receives two numbers and performs:
#
# Input → Add Numbers → Format Result → End
#
# Example:
# 10 + 20 → "The answer is 30"

# WRITE YOUR SOLUTION BELOW
# ------------------------------------------------------------


# ============================================================
# 6. Number Processing
# ============================================================
#
# Create a graph that receives a number and:
#
# 1. Checks the number.
# 2. Doubles it.
# 3. Creates a final message.
#
# Example:
# 5 → 10 → "The final number is 10"

# WRITE YOUR SOLUTION BELOW
# ------------------------------------------------------------


# ============================================================
# 7. Question Processing Workflow
# ============================================================
#
# Create a graph that receives a question and passes it through:
#
# - Question received
# - Question processed
# - Final answer returned
#
# Do not use a language model yet.

# WRITE YOUR SOLUTION BELOW
# ------------------------------------------------------------


# ============================================================
# 8. Multi-Step Order Workflow
# ============================================================
#
# Create a graph with four nodes that must execute in this exact order:
#
# Receive → Validate → Process → Finish
#
# Print a message from each node so you can see the execution order.

# WRITE YOUR SOLUTION BELOW
# ------------------------------------------------------------


# ============================================================
# 9. Mini Customer Request Workflow
# ============================================================
#
# Create a graph that receives a customer request and processes it through:
#
# Receive Request → Understand Request → Create Response → Finish
#
# Store the request and response in the graph state.

# WRITE YOUR SOLUTION BELOW
# ------------------------------------------------------------


# ============================================================
# 10. Complete Beginner Graph
# ============================================================
#
# Build a small workflow where:
#
# - The user provides some text.
# - One node cleans it.
# - One node processes it.
# - One node creates a result.
# - One node returns the final result.
#
# The goal is to understand the complete:
#
# Start → Nodes → End
#
# structure.

# WRITE YOUR SOLUTION BELOW
# ------------------------------------------------------------