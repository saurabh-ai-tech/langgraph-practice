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
# Create a graph that receives two numbers and performs:
# Input → Add Numbers → Format Result → End
# Example:
# 10 + 20 → "The answer is 30"
# WRITE YOUR SOLUTION BELOW
# ------------------------------------------------------------
from typing import TypedDict
from langgraph.graph import START, END, StateGraph

class CalcState(TypedDict):
    num1: float
    num2: float
    sum_result: float
    message: str

def add_no(state: CalcState)-> dict:
    addition = state['num1'] + state['num2']
    return{"sum_result": addition}

def format_result(state: CalcState) -> dict:
    val = state["sum_result"]
    display_val = int(val) if val.is_integer() else val
    return {"message": f"The answer is {display_val}"}

builder = StateGraph(CalcState)

builder.add_node("add", add_no)
builder.add_node("format", format_result)

builder.add_edge(START, "add")
builder.add_edge("add", "format")
builder.add_edge("format", END)

graph = builder.compile()
print(graph.invoke({"num1": 10, "num2": 20}))
# ============================================================
# 6. Number Processing
# ============================================================
# Create a graph that receives a number and:
# 1. Checks the number.
# 2. Doubles it.
# 3. Creates a final message.
# Example:
# 5 → 10 → "The final number is 10"
# WRITE YOUR SOLUTION BELOW
# ------------------------------------------------------------
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class NumberState(TypedDict):
    number: int
    is_valid: bool
    doubled_value: int
    output: str

def check_number(state: NumberState) -> dict:
    return {"is_valid": isinstance(state["number"], (int, float))}

def double_number(state: NumberState) -> dict:
    return {"doubled_value": state["number"] * 2}

def finalize_message(state: NumberState) -> dict:
    return {"output": f"The final number is {state['doubled_value']}"}

builder = StateGraph(NumberState)
builder.add_node("check", check_number)
builder.add_node("double", double_number)
builder.add_node("finalize", finalize_message)

builder.add_edge(START, "check")
builder.add_edge("check", "double")
builder.add_edge("double", "finalize")
builder.add_edge("finalize", END)

graph = builder.compile()
print(graph.invoke({"number": 5}))

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
from typing import TypedDict
from langgraph.graph import START, END, StateGraph

class QAState(TypedDict):
    question: str
    status: str
    answer: str

def receive_question(state: QAState) -> dict:
    return {"status": "Question received"}

def process_question(state: QAState) -> dict:
    # Rule-based processing demo
    q = state["question"].lower()
    if "capital of france" in q:
        ans = "Paris"
    else:
        ans = "Query processed successfully."
    return {"status": "Question processed", "answer": ans}

def return_answer(state: QAState) -> dict:
    return {"answer": f"Final Answer: {state['answer']}"}


builder = StateGraph(QAState)

builder.add_node("receive", receive_question)
builder.add_node("process", process_question)
builder.add_node("return_ans", return_answer)

builder.add_edge(START, "receive")
builder.add_edge("receive", "process")
builder.add_edge("process", "return_ans")
builder.add_edge("return_ans", END)

graph = builder.compile()
print(graph.invoke({"question": "What is the capital of France?"}))

# ============================================================
# 8. Multi-Step Order Workflow
# ============================================================
# Create a graph with four nodes that must execute in this exact order:
# Receive → Validate → Process → Finish
# Print a message from each node so you can see the execution order.
# WRITE YOUR SOLUTION BELOW
# ------------------------------------------------------------
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class OrderState(TypedDict):
    order_id: str
    is_valid: bool
    status: str

def receive_node(state: OrderState) -> dict:
    print(f"[1/4] Receiving Order: {state['order_id']}")
    return {"status": "received"}

def validate_node(state: OrderState) -> dict:
    print(f"[2/4] Validating Order: {state['order_id']}")
    return {"is_valid": True, "status": "validated"}

def process_node(state: OrderState) -> dict:
    print(f"[3/4] Processing Payment and Inventory: {state['order_id']}")
    return {"status": "processed"}

def finish_node(state: OrderState) -> dict:
    print(f"[4/4] Finishing Order: {state['order_id']}")
    return {"status": "completed"}

builder = StateGraph(OrderState)
builder.add_node("receive", receive_node)
builder.add_node("validate", validate_node)
builder.add_node("process", process_node)
builder.add_node("finish", finish_node)

builder.add_edge(START, "receive")
builder.add_edge("receive", "validate")
builder.add_edge("validate", "process")
builder.add_edge("process", "finish")
builder.add_edge("finish", END)

graph = builder.compile()
graph.invoke({"order_id": "ORD-9482"})

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
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class CustomerState(TypedDict):
    request: str
    intent: str
    response: str

def understand_request(state: CustomerState) -> dict:
    req = state["request"].lower()

    if "refund" in req or "return" in req:
        intent = "refund"
    elif "status" in req or "tracking" in req or "order" in req:
        intent = "order_status"
    else:
        intent = "general_inquiry"

    return {"intent": intent}

def create_response(state: CustomerState) -> dict:
    intent = state["intent"]

    if intent == "refund":
        reply = "We have initiated your return process. Please allow 3-5 business days."
    elif intent == "order_status":
        reply = "Your order is currently in transit and scheduled for delivery soon."
    else:
        reply = "Thank you for reaching out! A support representative will assist you shortly."

    return {"response": reply}

workflow = StateGraph(CustomerState)

workflow.add_node("understand", understand_request)
workflow.add_node("respond", create_response)

workflow.add_edge(START, "understand")
workflow.add_edge("understand", "respond")
workflow.add_edge("respond", END)

graph = workflow.compile()

initial_input = {"request": "Hi, where is my order? Tracking number is 12345."}
result = graph.invoke(initial_input)

print("Original Request:", result["request"])
print("Detected Intent: ", result["intent"])
print("Final Response:  ", result["response"])

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

from typing import TypedDict
from langgraph.graph import StateGraph, START, END


# 1. Define the State
class WorkflowState(TypedDict):
    raw_input: str
    cleaned_input: str
    processed_input: str
    result_message: str
    final_output: str


# 2. Define the Nodes
def clean_node(state: WorkflowState) -> dict:
    """Step 1: Strip extra spaces and normalize."""
    cleaned = state["raw_input"].strip()
    return {"cleaned_input": cleaned}


def process_node(state: WorkflowState) -> dict:
    """Step 2: Transform the text (e.g., capitalize words)."""
    processed = state["cleaned_input"].title()
    return {"processed_input": processed}


def create_result_node(state: WorkflowState) -> dict:
    """Step 3: Construct a descriptive result string."""
    msg = f"Processed successfully: '{state['processed_input']}'"
    return {"result_message": msg}


def return_final_node(state: WorkflowState) -> dict:
    """Step 4: Package the final payload to return."""
    return {"final_output": state["result_message"]}


# 3. Assemble the Graph
workflow = StateGraph(WorkflowState)

# Add each node to the graph
workflow.add_node("clean", clean_node)
workflow.add_node("process", process_node)
workflow.add_node("create_result", create_result_node)
workflow.add_node("return_final", return_final_node)

# 4. Connect the Pipeline: START → Clean → Process → Create → Return → END
workflow.add_edge(START, "clean")
workflow.add_edge("clean", "process")
workflow.add_edge("process", "create_result")
workflow.add_edge("create_result", "return_final")
workflow.add_edge("return_final", END)

# 5. Compile and Execute
graph = workflow.compile()

initial_state = {"raw_input": "   welcome to langgraph workflows   "}
output = graph.invoke(initial_state)

print(output["final_output"])
# Output: Processed successfully: 'Welcome To Langgraph Workflows'