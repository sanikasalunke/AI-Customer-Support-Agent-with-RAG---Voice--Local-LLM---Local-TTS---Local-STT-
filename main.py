# main.py
from core.llm_loader import load_llm
from core.agent import SupportAgent

def interactive():
    llm = load_llm()
    agent = SupportAgent(llm=llm)
    sid = "cli-session"
    agent.start_session(sid)
    print("Customer Support Agent — type 'exit' to quit")
    while True:
        msg = input("You: ")
        if msg.strip().lower() == "exit":
            break
        resp = agent.add_user_message(sid, msg)
        print("Agent:", resp["reply"])

if __name__ == "__main__":
    interactive()
