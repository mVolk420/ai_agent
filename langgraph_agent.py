from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.utils.function_calling import convert_to_openai_function  # ✅ NEU

from tools.file_tools import read_file, find_file
from config import OPENAI_API_KEY, DEBUG

# Zustandstyp für den Graph
AgentState = dict

# ✅ Tools definieren und für das Modell aufbereiten
tools = [read_file, find_file]  # echte Tool-Objekte mit .invoke()
tool_definitions = [convert_to_openai_function(t) for t in tools]  # GPT-kompatibles JSON-Schema

# Name → Tool-Mapping
tool_lookup = {t.name: t for t in tools}

# 🧠 GPT-Modell mit Tool-Unterstützung
llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-4",  # oder "gpt-4o"
    temperature=0
).bind_tools(tool_definitions)

# 🧩 Node-Funktion für LangGraph
def run_llm(state: dict) -> dict:
    user_msg = state.get("user_input", "")
    msg = HumanMessage(content=user_msg)
    response = llm.invoke([msg])

    if DEBUG:
        print("\n--- DEBUG: Tool Calls ---")
    if hasattr(response, "tool_calls") and response.tool_calls:
        tool_outputs = []
        for tool_call in response.tool_calls:
            name = tool_call.get("name")
            args = tool_call.get("args")
            if DEBUG:
                print(f"→ Tool-Call erkannt: {name} | args: {args}")

            tool = tool_lookup.get(name)
            if tool:
                try:
                    output = tool.invoke(args)
                    tool_outputs.append(f"[{name}] → {output}")
                except Exception as e:
                    tool_outputs.append(f"[{name}] → Fehler bei Tool-Ausführung: {e}")
            else:
                tool_outputs.append(f"[{name}] → Tool nicht gefunden")

        return {"user_input": user_msg, "response": "\n".join(tool_outputs)}
    else:
        if DEBUG:
            print("→ Keine Tool Calls erkannt")
        return {"user_input": user_msg, "response": response.content}

# 🧠 LangGraph-Definition
graph = StateGraph(AgentState)
graph.add_node("agent", RunnableLambda(run_llm))
graph.set_entry_point("agent")
graph.set_finish_point("agent")

# 🚀 Agent ausführen
graph_executor = graph.compile()
