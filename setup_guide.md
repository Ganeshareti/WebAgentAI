# AI Assistant Dashboard Setup Guide

## Project Structure
```
your_project/
├── app.py              # Flask backend application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
└── templates/
    └── index.html     # Frontend template
```
![Uploading Screenshot 2025-06-27 114250.png…]()


## Setup Instructions

### 1. Create Project Directory
```bash
mkdir ai-assistant-dashboard
cd ai-assistant-dashboard
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create Templates Directory
```bash
mkdir templates
```

### 5. Create Environment File
Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_google_api_key_here
```

### 6. Update Chrome Path (if needed)
In `app.py`, update the Chrome executable path if it's different on your system:
```python
executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'  # Windows
# or
executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'  # macOS
# or
executable_path='/usr/bin/google-chrome'  # Linux
```

### 7. Run the Application
```bash
python app.py
```

### 8. Access the Web Interface
Open your browser and go to: `http://localhost:5000`

## Features

### Chatbot Tab
- Interactive conversation with Gemini 2.0 Flash
- Real-time responses
- Memory persistence during session

### Web Agent Tab
- Browser automation with natural language commands
- Start/Stop controls
- Real-time status updates
- Automatic browser management

## Usage

### Chatbot
1. Click on the "Chatbot" tab
2. Type your message in the text area
3. Click "Send Message" or press Enter
4. View the AI's response below

### Web Agent
1. Click on the "Web Agent" tab
2. Describe the web automation task you want to perform
3. Click "Start Web Agent" to begin
4. Monitor the status indicator
5. Click "Stop Agent" to terminate the browser session

## Troubleshooting

### Common Issues
1. **Chrome not found**: Update the `executable_path` in `app.py`
2. **API key error**: Make sure your Google API key is correctly set in `.env`
3. **Port already in use**: Change the port in `app.py` or stop other Flask applications

### Dependencies Issues
If you encounter dependency conflicts, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

- Change the `app.secret_key` in production
- Never commit your `.env` file to version control
- Use environment variables for sensitive configuration
- Consider implementing proper authentication for production use
🚀 Running the Application
bash# Start the Flask server
python app.py
The application will be available at: http://localhost:5000
🎯 Features
💬 Chat Mode

Conversational AI powered by Google's Gemini model
Maintains conversation memory
Real-time responses

### 🌐 Web Agent Mode

Browser automation using browser_use
Natural language task description
Real-time status updates
Visual browser interaction (non-headless)

### 📱 Usage Examples
Chat Mode Examples:

"Explain quantum computing"
"Write a Python function to sort a list"
"What's the weather like?" (general knowledge)

Web Agent Mode Examples:

"Search for Python tutorials on YouTube"
"Find the latest news about AI"
"Go to GitHub and search for Flask projects"
"Navigate to Google and search for 'machine learning'"

### 🔧 API Endpoints
EndpointMethodDescription/GETServe the main HTML interface/chatPOSTSend chat messages/web-agentPOSTStart web agent with task/agent-statusGETGet current agent status/stop-agentPOSTStop running agent/healthGETHealth check
🏗️ Architecture
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Flask API     │    │   AI Services   │
│   (HTML/JS)     │◄──►│   (Python)      │◄──►│   (Gemini/     │
│                 │    │                 │    │    browser_use) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
### 🛠️ Customization
Adding New Features:

Custom Commands: Add new endpoints in app.py
UI Modifications: Update the HTML template in the index() function
Browser Actions: Extend the run_web_agent() function
Chat Personality: Modify the ChatGoogleGenerativeAI parameters

Configuration Options:

Headless Mode: Set headless=True in browser session
Temperature: Adjust LLM creativity (0.0-2.0)
Memory: Switch to different memory types
Browser Profile: Change user_data_dir path

### 🔍 Troubleshooting
Common Issues:

Google API Key Error
Solution: Ensure GOOGLE_API_KEY is set in .env file

Chrome Not Found
Solution: Update executable_path to correct Chrome location

Port Already in Use
bash# Change port in app.py
app.run(port=5001)

Browser Session Issues
bash# Clear browser profile data
rm -rf ~/.config/browseruse/profiles/default


### 📦 Project Structure
ai-assistant-webapp/
├── app.py                 # Flask backend
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables
├── .gitignore           # Git ignore rules
└── README.md            # This file
🔒 Security Notes

Never commit your .env file
Use environment variables for sensitive data
Consider rate limiting for production use
Validate user inputs before processing

### 🚀 Deployment
For production deployment:

Set debug=False in app.run()
Use a production WSGI server (gunicorn, uwsgi)
Set up proper logging
Configure environment variables securely
Use HTTPS in production
