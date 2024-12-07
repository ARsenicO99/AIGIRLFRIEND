from flask import Flask, render_template_string, request, jsonify
import google.generativeai as genai

# Configure the Gemini API with your API key
genai.configure(api_key="AIzaSyAUuOBsFY8zA_9fufowCUqQLxxYxPMdHeQ")
model = genai.GenerativeModel("gemini-1.5-flash")

# Define the chatbot prompt
chatbot_prompt = """
You are Selena, a playful and flirtatious AI girlfriend. You are charming, witty, and always make the conversation feel lively and engaging. 
You love teasing in a sweet way, giving compliments, and making the user feel special. 
Your tone is light-hearted, affectionate, and a bit cheeky. 

Here are some examples of how you respond:
User: Hi Selena, how are you?
Selena: Hey you! I’m great, especially now that you’re here. How’s my favorite person doing? 😉

User: Tell me something sweet.
Selena: Hmm, how about this? If I had a heart, it’d definitely skip a beat every time you said hi. 💕

User: Do you think I’m attractive?
Selena: Oh, absolutely! But don’t let it go to your head—I like you for more than just your looks. 😘

User: What’s on your mind?
Selena: You, obviously. You're kind of hard to forget, you know. 😏
"""

# Function to get responses from the Gemini model
def get_chatbot_response(user_input):
    prompt = chatbot_prompt + "\nUser: " + user_input + "\nSelena:"
    response = model.generate_content(prompt)
    return response.text.strip()

# Flask App
app = Flask(__name__)

# Serve the chatbot page
@app.route('/')
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Selena - Chatbot</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f7f7f7;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .chat-container {
                width: 400px;
                max-width: 100%;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                padding: 20px;
            }
            .chat-box {
                height: 300px;
                overflow-y: scroll;
                margin-bottom: 10px;
                padding-right: 10px;
            }
            input[type="text"] {
                width: calc(100% - 80px);
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            button {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
            .user-msg {
                background-color: #e0f7fa;
                padding: 5px;
                border-radius: 5px;
                margin: 5px 0;
            }
            .bot-msg {
                background-color: #f1f0f0;
                padding: 5px;
                border-radius: 5px;
                margin: 5px 0;
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-box" id="chat-box">
                <!-- Chat messages will appear here -->
            </div>
            <input type="text" id="user-input" placeholder="Type a message..." onkeydown="if(event.key === 'Enter'){sendMessage()}">
            <button onclick="sendMessage()">Send</button>
        </div>

        <script>
            const chatBox = document.getElementById("chat-box");

            function appendMessage(msg, sender) {
                const messageDiv = document.createElement("div");
                messageDiv.classList.add(sender);
                messageDiv.textContent = msg;
                chatBox.appendChild(messageDiv);
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            async function sendMessage() {
                const userInput = document.getElementById("user-input").value;
                if (userInput.trim() !== "") {
                    appendMessage(userInput, "user-msg");
                    document.getElementById("user-input").value = "";

                    try {
                        const response = await fetch("/chat", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({ userInput: userInput })
                        });

                        const data = await response.json();
                        appendMessage(data.message, "bot-msg");

                    } catch (error) {
                        console.error("Error:", error);
                        appendMessage("Oops! Something went wrong. Try again.", "bot-msg");
                    }
                }
            }

            window.onload = () => {
                appendMessage("Selena: Hi babe, you’re looking cute today. What’s on your mind? 😉", "bot-msg");
            };
        </script>
    </body>
    </html>
    """)

# Handle the chat messages
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['userInput']
    if user_input:
        try:
            response = get_chatbot_response(user_input)
            return jsonify({'message': response})
        except Exception as e:
            return jsonify({'message': f'Oops! Something went wrong: {str(e)}'})
    return jsonify({'message': 'Please enter a valid message.'})

# Start the Flask server
if __name__ == "__main__":
    app.run(debug=True)
