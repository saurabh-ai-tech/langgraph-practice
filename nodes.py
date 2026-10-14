"""
======================================================================
ASSIGNMENT: 3. NODES & WORKFLOWS
======================================================================
"""
from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict
from langgraph.graph import END, START, StateGraph
# ====================================================================
# EXERCISE 1: Single Task Node
# Create one node that receives a name and creates a greeting.
# ====================================================================
class Ex1State(TypedDict):
    name: str
    greeting: Optional[str]


def greet_node(state: Ex1State) -> Dict[str, Any]:
    return {"greeting": f"Hello, {state['name']}!"}


builder_1 = StateGraph(Ex1State)
builder_1.add_node("greet", greet_node)
builder_1.add_edge(START, "greet")
builder_1.add_edge("greet", END)
graph_1 = builder_1.compile()


# ====================================================================
# EXERCISE 2: Input Node + Processing Node
# Create two nodes:
#   - Node 1 receives user input.
#   - Node 2 processes the input.
# Pass the information using state.
# ====================================================================

class Info(TypedDict):
    raw_input: str
    processed_input: Optional[str]

def input_node(state: Info):
    return {"raw_input": state["raw_input"]}

def processing_node(state: Info):
    cleaned = state["raw_input"].strip().title()
    return {"processed_input": cleaned}


graph = StateGraph(Info)

graph.add_node("input_node", input_node)
graph.add_node("processing_node", processing_node)

graph.add_edge(START, "receive_input")
graph.add_edge("receive_input", "process_input")
graph.add_edge("process_input", END)

app = graph.compile()

result = app.invoke("How are you doing?")
print(result)





# ====================================================================
# EXERCISE 3: Three Separate Tasks
# Create three nodes:
#   - Clean Text
#   - Count Words
#   - Create Result
# Each node should have only one responsibility.
# ====================================================================

# [Your solution here]




# ====================================================================
# EXERCISE 4: Four-Step Workflow
# Create four nodes that perform:
#   Receive -> Validate -> Process -> Respond
# Connect them in the correct order.
# ====================================================================

# [Your solution here]




# ====================================================================
# EXERCISE 5: Reusable Processing Node
# Create a node that receives a piece of text and converts it to lowercase.
# Use this node in a workflow that processes several different inputs.
# ====================================================================

# [Your solution here]




# ====================================================================
# EXERCISE 6: Node That Uses Previous Work
# Create:
#   - Node 1 -> extracts a person's name.
#   - Node 2 -> uses the extracted name to create a greeting.
# The second node should not receive the original input directly;
# it should use state.
# ====================================================================

# [Your solution here]




# ====================================================================
# EXERCISE 7: Node With Multiple State Values
# Create a node that receives:
#   - name
#   - age
#   - city
# and creates a personalized introduction.
# ====================================================================

# [Your solution here]




# ====================================================================
# EXERCISE 8: Separate Model Node
# Create a workflow where:
#   - One node prepares the user's question.
#   - One node sends it to a language model.
#   - One node formats the model's response.
# ====================================================================

# [Your solution here]




# ====================================================================
# EXERCISE 9: Customer Support Nodes
# Create separate nodes for:
#   - Receiving customer message
#   - Understanding the message
#   - Creating an answer
#   - Returning the answer
# Connect all nodes into one workflow.
# ====================================================================

# [Your solution here]




# ====================================================================
# EXERCISE 10: Complete Multi-Node Project
# Build a workflow with at least five nodes where every node has a
# clear responsibility.
# Example:
#   Input -> Validate -> Prepare -> Process -> Final Response
# Goal: Practice breaking one large task into multiple nodes.
# ====================================================================

# [Your solution here]