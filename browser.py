from langchain_google_genai import ChatGoogleGenerativeAI 
from dotenv import load_dotenv 
from browser_use import Agent, BrowserSession 
import asyncio
load_dotenv()
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=1.2)
browser_session = BrowserSession(
    # Path to a specific Chromium-based executable (optional)
    executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
	#'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS
    # For Windows: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    # For Linux: '/usr/bin/google-chrome'
    
    # Use a specific data directory on disk (optional, set to None for incognito)
    user_data_dir='~/.config/browseruse/profiles/default',   # this is the default
    # ... any other BrowserProfile or playwright launch_persistnet_context config...
    # headless=False,
)
memory = ConversationBufferMemory()
chatbot_chain = ConversationChain(llm=llm, memory=memory)

agent = Agent(
	task="facebook ceo",
	llm=llm,
	browser_session=browser_session,
)
async def main():
	history = await agent.run()
	input('Press Enter to close the browser...')
	
	await browser_session.close()
if __name__ == '__main__':
	asyncio.run(main())