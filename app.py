"""
Flask backend for
    • normal Chat mode  (Google Generative AI via LangChain)
    • Web-Agent mode    (browser_use.Agent)

A single, dedicated asyncio loop runs forever in a daemon thread.
All async work is scheduled onto that loop with run_async().
"""

import os
import asyncio
import threading
import atexit
from concurrent.futures import Future

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

from browser_use import Agent, BrowserSession   # ← your own module

# ------------------------------------------------------------------------------
#  Global asyncio loop running in its own thread
# ------------------------------------------------------------------------------

_loop = asyncio.new_event_loop()
asyncio.set_event_loop(_loop)        # set for main thread (just in case)

def _loop_runner():
    _loop.run_forever()

threading.Thread(target=_loop_runner, daemon=True).start()

def run_async(coro) -> Future:
    """
    Schedule *coro* on the background event loop and get a concurrent.futures.Future.
    """
    return asyncio.run_coroutine_threadsafe(coro, _loop)

# ------------------------------------------------------------------------------
#  Initialise services
# ------------------------------------------------------------------------------

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=1.2)
memory = ConversationBufferMemory()
chat_chain = ConversationChain(llm=llm, memory=memory)

browser_session = BrowserSession(
    executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    user_data_dir=os.path.expanduser("~/.config/browseruse/profiles/default"),
)

# Will hold the running Agent object and its Future
agent_future: Future | None = None
agent_obj:    Agent  | None = None

# ------------------------------------------------------------------------------
#  Flask application
# ------------------------------------------------------------------------------

app = Flask(__name__)

@app.route("/")
def index():
    """Serve the SPA (your HTML lives in templates/index.html)."""
    return render_template("index.html")


# ---------------------------- Chat endpoint -----------------------------------

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_msg = request.json.get("message", "")
        bot_reply = chat_chain.run(user_msg)
        return jsonify({"response": bot_reply})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


# ---------------------------- Web-Agent endpoints ------------------------------

@app.route("/web-agent", methods=["POST"])
def web_agent():
    """
    Kick off a long-running web-agent task.
    It returns immediately; progress is polled via /agent-status.
    """
    global agent_future, agent_obj

    if agent_future and not agent_future.done():
        return jsonify({"error": "An agent task is already running."}), 409

    task_description = request.json.get("task", "facebook ceo")
    agent_obj = Agent(task=task_description, llm=llm, browser_session=browser_session)
    agent_future = run_async(agent_obj.run())      # schedule async task

    return jsonify({"response": f"Started web-agent task: {task_description}"}), 202


@app.route("/agent-status", methods=["GET"])
def agent_status():
    """
    Polling endpoint used by the front-end every few seconds.
    """
    if not agent_future:
        return jsonify({"running": False})

    if agent_future.done():
        try:
            result = agent_future.result()
            return jsonify({"completed": True, "result": result})
        except Exception as exc:
            return jsonify({"completed": True, "result": f"Agent failed: {exc}"})
    return jsonify({"running": True})


@app.route("/stop-agent", methods=["POST"])
def stop_agent():
    """
    Cancel a running agent (if any).
    """
    global agent_future
    if agent_future and not agent_future.done():
        agent_future.cancel()
        agent_future = None
        return jsonify({"response": "Agent cancelled by user."})
    return jsonify({"response": "No agent was running."})


# ------------------------------------------------------------------------------
#  Graceful shutdown – close the browser & loop when Flask exits
# ------------------------------------------------------------------------------

@atexit.register
def _cleanup():
    async def close_browser():
        await browser_session.close()

    try:
        run_async(close_browser()).result(5)   # wait up to 5 s
    finally:
        _loop.call_soon_threadsafe(_loop.stop)


# ------------------------------------------------------------------------------
#  Development entry-point
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    # Use threaded=True (default) – our event-loop lives happily in its own thread.
    app.run(debug=True)
