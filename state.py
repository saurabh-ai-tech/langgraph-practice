
# ============================================================
# 1. User Information State
# ============================================================

# Create a graph whose state contains:
# - name
# - age
# - city
#
# Create a node that reads these values and creates a sentence.
#
# Example output:
# "Saurabh is 25 years old and lives in Delhi."


# WRITE YOUR SOLUTION HERE
# ------------------------------------------------------------
from typing import TypedDict
from langgraph.graph import StateGraph, START, END 

class User(TypedDict): 
    name: str
    age: int
    city: str
    message: str

#defining node
def sentence_creator(state: User):
    message = f"{state['name']} is {state['age']} years old and lives in {state['city']}."
    return {"message": message}


graph = StateGraph(User)

graph.add_node("create_sentence", sentence_creator)

graph.add_edge(START, "create_sentence")
graph.add_edge("create_sentence", END)

app = graph.compile()

result = app.invoke({
    "name": "Saurabh",
    "age": 25,
    "city": "Delhi"
})

print(result)

# ============================================================
# 2. Update User Information
# ============================================================

# Create a graph where the initial state contains a person's age.
#
# Create a node that:
# - reads the age from state
# - increases the age by 1
# - saves the new age back into state


# WRITE YOUR SOLUTION HERE
# ------------------------------------------------------------
from typing import TypedDict
from langgraph.graph import StateGraph, START, END 

class UserInfo(TypedDict):
    age: str

def increase_age(state: UserInfo):
    return {
        "age": state["age"] + 1
    }

graph = StateGraph(UserInfo)

graph.add_node("increase_age", increase_age)

graph.add_edge(START, "increase_age")
graph.add_edge("increase_age", END)

app = graph.compile()

result = app.invoke({
    "age": 25
})

print(result)
# ============================================================
# 3. Add Information to State
# ============================================================

# Start with state containing:
# - name
#
# Create nodes that add:
# - age
# - city
# - occupation
#
# At the end, print the complete state.


# WRITE YOUR SOLUTION HERE
# ------------------------------------------------------------
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class UserState(TypedDict):
    name: str
    age: int
    city: str
    occupation: str


def add_age(state: UserState):
    return {"age": 25}


def add_city(state: UserState):
    return {"city": "Delhi"}


def add_occupation(state: UserState):
    return {"occupation": "AI Engineer"}


graph = StateGraph(UserState)

graph.add_node("add_age", add_age)
graph.add_node("add_city", add_city)
graph.add_node("add_occupation", add_occupation)

graph.add_edge(START, "add_age")
graph.add_edge("add_age", "add_city")
graph.add_edge("add_city", "add_occupation")
graph.add_edge("add_occupation", END)

app = graph.compile()

result = app.invoke({
    "name": "Saurabh"
})

print(result)

# ============================================================
# 4. Pass Information Between Nodes
# ============================================================

# Create three nodes:
#
# 1. First node creates a person's name.
#
# 2. Second node reads the name from state
#    and creates a greeting.
#
# 3. Third node reads the greeting from state
#    and creates the final message.
#
# The information must travel through the state.


# WRITE YOUR SOLUTION HERE
# ------------------------------------------------------------
from typing import TypedDict
from langgraph.graph import StateGraph, START, END 

class UserInfo(TypedDict):
    name: str
    greeting: str
    final_message: str

def first_node(state: UserInfo):
    return {"name": "Saurabh"}

def second_node(state: UserInfo):
    return {
        "greeting": f"Hello {state['name']}!"
    }

def third_node(state: UserInfo):
    return {
        "final_message": f"{state['greeting']} Welcome to LangGraph."
    }

graph = StateGraph(UserInfo)

graph.add_node("first_node", first_node)
graph.add_node("second_node", second_node)
graph.add_node("third_node", third_node)

graph.add_edge(START, "first_node")
graph.add_edge("first_node", "second_node")
graph.add_edge("second_node", "third_node")
graph.add_edge("third_node", END)

app = graph.compile()

result = app.invoke({})

print(result)


#============================================================
# 5. Question and Answer State
# ============================================================

# Create state containing:
# - question
# - answer
#
# The first node receives the question.
#
# The second node creates an answer.
#
# The answer must be saved into state.


# WRITE YOUR SOLUTION HERE
# ------------------------------------------------------------
from typing import TypedDict 
from langgraph.graph import StateGraph, START, END

class QAState(TypedDict):
    question: str
    answer: str


def receive_question(state: QAState):
    return {
        "question": state["question"]
    }


def create_answer(state: QAState):
    question = state["question"]

    return {
        "answer": f"The answer to your question '{question}' is being processed."
    }

graph = StateGraph(QAState)

graph.add_node("receive_question", receive_question)
graph.add_node("create_answer", create_answer)

graph.add_edge(START, "receive_question")
graph.add_edge("receive_question", "create_answer")
graph.add_edge("create_answer", END)

app = graph.compile()

result = app.invoke({
    "question": "What is LangGraph?"
})
# ============================================================
# 6. Conversation State
# ============================================================

# Create state containing a list of messages.
#
# When the user sends a message:
#
# 1. Add the user message.
#
# 2. Generate a response.
#
# 3. Add the AI response.
#
# The state should contain the complete conversation history.


# WRITE YOUR SOLUTION HERE
# ------------------------------------------------------------
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class ConversationState(TypedDict):
    messages: list


def add_user_message(state: ConversationState):
    messages = state["messages"].copy()

    messages.append({
        "role": "user",
        "content": "Hello!"
    })

    return {
        "messages": messages
    }


def generate_ai_response(state: ConversationState):
    messages = state["messages"].copy()

    messages.append({
        "role": "assistant",
        "content": "Hello! How can I help you?"
    })

    return {
        "messages": messages
    }


graph = StateGraph(ConversationState)

graph.add_node("add_user_message", add_user_message)
graph.add_node("generate_ai_response", generate_ai_response)

graph.add_edge(START, "add_user_message")
graph.add_edge("add_user_message", "generate_ai_response")
graph.add_edge("generate_ai_response", END)

app = graph.compile()

result = app.invoke({
    "messages": []
})

print(result)


# ============================================================
# 7. Processing Status
# ============================================================

# Create state containing:
# - input
# - result
# - status
#
# Set:
#     status = "processing"
#
# while processing the input.
#
# Then set:
#     status = "completed"
#
# when the processing is finished.


# WRITE YOUR SOLUTION HERE
# ------------------------------------------------------------
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class ProcessState(TypedDict):
    input: str
    result: str
    status: str

def start_processing(state: ProcessState):
    return {
        "status": "processing"
    }

def process_input(state: ProcessState):
    result = state["input"].upper()

    return {
        "result": result,
        "status": "completed"
    }


# ============================================================
# 8. Multiple State Updates
# ============================================================

# Create three nodes where each node modifies
# a different part of the state.
#
# Node 1 → adds name
# Node 2 → adds age
# Node 3 → adds city
#
# Check/print the state after every node.


# WRITE YOUR SOLUTION HERE
# ------------------------------------------------------------
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class UserState(TypedDict):
    name: str
    age: int
    city: str


def add_name(state: UserState):
    return {
        "name": "Saurabh"
    }


def add_age(state: UserState):
    return {
        "age": 25
    }


def add_city(state: UserState):
    return {
        "city": "Delhi"
    }


graph = StateGraph(UserState)

graph.add_node("add_name", add_name)
graph.add_node("add_age", add_age)
graph.add_node("add_city", add_city)

graph.add_edge(START, "add_name")
graph.add_edge("add_name", "add_age")
graph.add_edge("add_age", "add_city")
graph.add_edge("add_city", END)

app = graph.compile()

result = app.invoke({
    "name": "",
    "age": 0,
    "city": ""
})

print(result)
    

# ============================================================
# 9. State-Based Result
# ============================================================

# Create a graph that receives a student's:
# - marks
# - subject
#
# One node calculates the result.
#
# Another node saves:
# - marks
# - subject
# - pass/fail result
#
# into state.


# WRITE YOUR SOLUTION HERE
# ------------------------------------------------------------
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class StudentState(TypedDict):
    marks: int
    subject: str
    result: str


def calculate_result(state: StudentState):
    if state["marks"] >= 40:
        result = "Pass"
    else:
        result = "Fail"

    return {
        "result": result
    }


def save_result(state: StudentState):
    return {
        "marks": state["marks"],
        "subject": state["subject"],
        "result": state["result"]
    }


graph = StateGraph(StudentState)

graph.add_node("calculate_result", calculate_result)
graph.add_node("save_result", save_result)

graph.add_edge(START, "calculate_result")
graph.add_edge("calculate_result", "save_result")
graph.add_edge("save_result", END)

app = graph.compile()

result = app.invoke({
    "marks": 75,
    "subject": "Python",
    "result": ""
})

print(result)


# ============================================================
# 10. Complete State Workflow
# ============================================================

# Build a workflow where state contains:
#
# - user input
# - cleaned input
# - processed information
# - final result
# - status
#
# Every node should update the appropriate
# part of the state.


# WRITE YOUR SOLUTION HERE
# ------------------------------------------------------------
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class WorkflowState(TypedDict):
    user_input: str
    cleaned_input: str
    processed_information: str
    final_result: str
    status: str


def clean_input(state: WorkflowState):
    cleaned = state["user_input"].strip().lower()

    return {
        "cleaned_input": cleaned,
        "status": "processing"
    }


def process_information(state: WorkflowState):
    processed = f"Processed: {state['cleaned_input']}"

    return {
        "processed_information": processed
    }


def create_final_result(state: WorkflowState):
    final = f"Final result: {state['processed_information']}"

    return {
        "final_result": final,
        "status": "completed"
    }


graph = StateGraph(WorkflowState)

graph.add_node("clean_input", clean_input)
graph.add_node("process_information", process_information)
graph.add_node("create_final_result", create_final_result)

graph.add_edge(START, "clean_input")
graph.add_edge("clean_input", "process_information")
graph.add_edge("process_information", "create_final_result")
graph.add_edge("create_final_result", END)

app = graph.compile()

result = app.invoke({
    "user_input": "  Hello LangGraph  ",
    "cleaned_input": "",
    "processed_information": "",
    "final_result": "",
    "status": "pending"
})

print(result)