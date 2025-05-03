from flask import Flask, request

app = Flask(__name__)
VERIFY_TOKEN = "your_custom_verify_token"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Verification failed", 403
    if request.method == 'POST':
        data = request.get_json()
        try:
            # Extract message details
            entry = data["entry"][0]
            changes = entry["changes"][0]
            value = changes["value"]
            messages = value.get("messages")
            
            if messages:
                msg = messages[0]
                sender = msg.get("from")
                message_body = msg.get("text", {}).get("body", "")
                
                print(f"\n📩 New message from {sender}: {message_body}\n")
            else:
                print("No new user message in this update.")
        except Exception as e:
            print("⚠️ Error parsing incoming message:", str(e))
        return "OK", 200

if __name__ == '__main__':
    app.run()
