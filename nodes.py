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

class task_state(TypedDict):
    text: str
    cleaned_text: Optional[str]
    words_count: Optional[int]
    result : str


def clean_text_node(state: task_state) -> Dict[str, Any]:
    return {"cleaned_text": " ".join(state["text"].split())}


def count_words_node(state: task_state) -> Dict[str, Any]:
    words = state["cleaned_text"].split() if state["cleaned_text"] else []
    return {"word_count": len(words)}


def create_result_node(state: task_state) -> Dict[str, Any]:
    summary = (
        f"Text '{state['cleaned_text']}' contains {state['word_count']} words."
    )
    return {"result": summary}


builder_3 = StateGraph(task_state)
builder_3.add_node("clean_text", clean_text_node)
builder_3.add_node("count_words", count_words_node)
builder_3.add_node("create_result", create_result_node)

builder_3.add_edge(START, "clean_text")
builder_3.add_edge("clean_text", "count_words")
builder_3.add_edge("count_words", "create_result")
builder_3.add_edge("create_result", END)
graph_3 = builder_3.compile()

# ====================================================================
# EXERCISE 4: Four-Step Workflow
# Create four nodes that perform:
#   Receive -> Validate -> Process -> Respond
# Connect them in the correct order.
# ====================================================================

class Ex4State(TypedDict):
    raw_data: Any
    is_valid: bool
    processed_data: Optional[str]
    response: Optional[str]


def receive_node(state: Ex4State) -> Dict[str, Any]:
    return {"raw_data": state["raw_data"]}


def validate_node(state: Ex4State) -> Dict[str, Any]:
    valid = isinstance(state["raw_data"], str) and len(state["raw_data"]) > 0
    return {"is_valid": valid}


def process_node(state: Ex4State) -> Dict[str, Any]:
    if not state.get("is_valid", False):
        return {"processed_data": None}
    return {"processed_data": state["raw_data"].upper()}


def respond_node(state: Ex4State) -> Dict[str, Any]:
    if not state.get("is_valid", False):
        return {"response": "Error: Invalid data provided."}
    return {"response": f"Successfully processed: {state['processed_data']}"}


builder_4 = StateGraph(Ex4State)
builder_4.add_node("receive", receive_node)
builder_4.add_node("validate", validate_node)
builder_4.add_node("process", process_node)
builder_4.add_node("respond", respond_node)

builder_4.add_edge(START, "receive")
builder_4.add_edge("receive", "validate")
builder_4.add_edge("validate", "process")
builder_4.add_edge("process", "respond")
builder_4.add_edge("respond", END)
graph_4 = builder_4.compile()

# ====================================================================
# EXERCISE 5: Reusable Processing Node
# Create a node that receives a piece of text and converts it to lowercase.
# Use this node in a workflow that processes several different inputs.
# ====================================================================
class Ex5State(TypedDict):
    input_strings: List[str]
    lowercased_strings: List[str]


def to_lower_node(state: Ex5State) -> Dict[str, Any]:
    # Processes all inputs using the same conversion logic
    converted = [item.lower() for item in state.get("input_strings", [])]
    return {"lowercased_strings": converted}


builder_5 = StateGraph(Ex5State)
builder_5.add_node("to_lower", to_lower_node)
builder_5.add_edge(START, "to_lower")
builder_5.add_edge("to_lower", END)
graph_5 = builder_5.compile()

# ====================================================================
# EXERCISE 6: Node That Uses Previous Work
# Create:
#   - Node 1 -> extracts a person's name.
#   - Node 2 -> uses the extracted name to create a greeting.
# The second node should not receive the original input directly;
# it should use state.
# ====================================================================

class Ex6State(TypedDict):
    raw_message: str
    extracted_name: Optional[str]
    greeting: Optional[str]


def extract_name_node(state: Ex6State) -> Dict[str, Any]:
    # e.g., "My name is John" -> "John"
    parts = state["raw_message"].split()
    name = parts[-1] if parts else "Friend"
    return {"extracted_name": name}


def generate_greeting_node(state: Ex6State) -> Dict[str, Any]:
    # Reads ONLY extracted_name from state, not raw_message
    person = state.get("extracted_name", "Friend")
    return {"greeting": f"Nice to meet you, {person}!"}


builder_6 = StateGraph(Ex6State)
builder_6.add_node("extract_name", extract_name_node)
builder_6.add_node("generate_greeting", generate_greeting_node)
builder_6.add_edge(START, "extract_name")
builder_6.add_edge("extract_name", "generate_greeting")
builder_6.add_edge("generate_greeting", END)
graph_6 = builder_6.compile()

# ====================================================================
# EXERCISE 7: Node With Multiple State Values
# Create a node that receives:
#   - name
#   - age
#   - city
# and creates a personalized introduction.
# ====================================================================
class Ex7State(TypedDict):
    name: str
    age: int
    city: str
    introduction: Optional[str]


def introduce_person_node(state: Ex7State) -> Dict[str, Any]:
    name = state["name"]
    age = state["age"]
    city = state["city"]
    intro = f"Meet {name}, who is {age} years old and lives in {city}."
    return {"introduction": intro}


builder_7 = StateGraph(Ex7State)
builder_7.add_node("introduce", introduce_person_node)
builder_7.add_edge(START, "introduce")
builder_7.add_edge("introduce", END)
graph_7 = builder_7.compile()

# ====================================================================
# EXERCISE 8: Separate Model Node
# Create a workflow where:
#   - One node prepares the user's question.
#   - One node sends it to a language model.
#   - One node formats the model's response.
# ====================================================================

class Ex8State(TypedDict):
    raw_query: str
    prepared_prompt: Optional[str]
    raw_llm_response: Optional[str]
    final_output: Optional[str]


def prepare_question_node(state: Ex8State) -> Dict[str, Any]:
    formatted_prompt = (
        f"Answer this query concisely: {state['raw_query'].strip()}"
    )
    return {"prepared_prompt": formatted_prompt}


def call_model_node(state: Ex8State) -> Dict[str, Any]:
    # Mock LLM generation call
    prompt = state["prepared_prompt"]
    simulated_model_output = f"[AI Generated Answer for: '{prompt}']"
    return {"raw_llm_response": simulated_model_output}


def format_response_node(state: Ex8State) -> Dict[str, Any]:
    result = f"--- Result ---\n{state['raw_llm_response']}\n--------------"
    return {"final_output": result}


builder_8 = StateGraph(Ex8State)
builder_8.add_node("prepare_question", prepare_question_node)
builder_8.add_node("call_model", call_model_node)
builder_8.add_node("format_response", format_response_node)

builder_8.add_edge(START, "prepare_question")
builder_8.add_edge("prepare_question", "call_model")
builder_8.add_edge("call_model", "format_response")
builder_8.add_edge("format_response", END)
graph_8 = builder_8.compile()


# ====================================================================
# EXERCISE 9: Customer Support Nodes
# Create separate nodes for:
#   - Receiving customer message
#   - Understanding the message
#   - Creating an answer
#   - Returning the answer
# Connect all nodes into one workflow.
# ====================================================================
class Ex9State(TypedDict):
    customer_message: str
    intent: Optional[str]
    draft_reply: Optional[str]
    delivered_reply: Optional[str]


def receive_message_node(state: Ex9State) -> Dict[str, Any]:
    return {"customer_message": state["customer_message"]}


def understand_intent_node(state: Ex9State) -> Dict[str, Any]:
    msg = state["customer_message"].lower()
    if "refund" in msg:
        detected_intent = "billing_refund"
    elif "help" in msg or "broken" in msg:
        detected_intent = "technical_support"
    else:
        detected_intent = "general_inquiry"
    return {"intent": detected_intent}


def create_answer_node(state: Ex9State) -> Dict[str, Any]:
    intent = state.get("intent")
    answers = {
        "billing_refund": "Please share your order ID so we can process your refund.",
        "technical_support": "Our technical team will reach out to resolve the glitch.",
        "general_inquiry": "Thanks for contacting us! How can we assist you today?",
    }
    return {"draft_reply": answers.get(intent, "How can we help?")}


def return_answer_node(state: Ex9State) -> Dict[str, Any]:
    formatted = f"Support Team: {state['draft_reply']}"
    return {"delivered_reply": formatted}


builder_9 = StateGraph(Ex9State)
builder_9.add_node("receive_message", receive_message_node)
builder_9.add_node("understand_intent", understand_intent_node)
builder_9.add_node("create_answer", create_answer_node)
builder_9.add_node("return_answer", return_answer_node)

builder_9.add_edge(START, "receive_message")
builder_9.add_edge("receive_message", "understand_intent")
builder_9.add_edge("understand_intent", "create_answer")
builder_9.add_edge("create_answer", "return_answer")
builder_9.add_edge("return_answer", END)
graph_9 = builder_9.compile()

# ====================================================================
# EXERCISE 10: Complete Multi-Node Project
# Build a workflow with at least five nodes where every node has a
# clear responsibility.
# Example:
#   Input -> Validate -> Prepare -> Process -> Final Response
# Goal: Practice breaking one large task into multiple nodes.
# ====================================================================

class Ex10State(TypedDict):
    raw_payload: Optional[Dict[str, Any]]
    is_valid: bool
    sanitized_text: Optional[str]
    analysis_stats: Optional[Dict[str, int]]
    final_response: Optional[str]


# Node 1: Input
def step_input(state: Ex10State) -> Dict[str, Any]:
    return {"raw_payload": state.get("raw_payload", {})}


# Node 2: Validate
def step_validate(state: Ex10State) -> Dict[str, Any]:
    payload = state.get("raw_payload", {})
    text_val = payload.get("text")
    valid = isinstance(text_val, str) and len(text_val.strip()) > 0
    return {"is_valid": valid}


# Node 3: Prepare
def step_prepare(state: Ex10State) -> Dict[str, Any]:
    if not state.get("is_valid", False):
        return {"sanitized_text": ""}
    raw_text = state["raw_payload"].get("text", "")
    return {"sanitized_text": raw_text.strip()}


# Node 4: Process
def step_process(state: Ex10State) -> Dict[str, Any]:
    if not state.get("is_valid", False):
        return {"analysis_stats": {}}
    content = state.get("sanitized_text", "")
    stats = {
        "char_count": len(content),
        "word_count": len(content.split()),
        "uppercase_letters": sum(1 for c in content if c.isupper()),
    }
    return {"analysis_stats": stats}


# Node 5: Final Response
def step_final_response(state: Ex10State) -> Dict[str, Any]:
    if not state.get("is_valid", False):
        return {"final_response": "Status 400: Invalid payload provided."}

    stats = state.get("analysis_stats", {})
    response = (
        f"Processing completed successfully.\n"
        f"- Words: {stats.get('word_count', 0)}\n"
        f"- Characters: {stats.get('char_count', 0)}\n"
        f"- Uppercase characters: {stats.get('uppercase_letters', 0)}"
    )
    return {"final_response": response}


# Pipeline Assembly
builder_10 = StateGraph(Ex10State)
builder_10.add_node("input", step_input)
builder_10.add_node("validate", step_validate)
builder_10.add_node("prepare", step_prepare)
builder_10.add_node("process", step_process)
builder_10.add_node("final_response", step_final_response)

builder_10.add_edge(START, "input")
builder_10.add_edge("input", "validate")
builder_10.add_edge("validate", "prepare")
builder_10.add_edge("prepare", "process")
builder_10.add_edge("process", "final_response")
builder_10.add_edge("final_response", END)

graph_10 = builder_10.compile()