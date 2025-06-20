from langgraph_agent import graph_executor

def main():
    print("LangGraph-Agent gestartet. Tippe 'exit' zum Beenden.")
    while True:
        user_input = input("Du: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        state = {"user_input": user_input}
        result = graph_executor.invoke(state)
        print("KI:", result["response"])

if __name__ == "__main__":
    main()
