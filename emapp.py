
from flask import Flask, request, render_template, jsonify
from twilio.rest import Client

app = Flask(__name__)

# Your Twilio credentials
account_sid = 'ACf1ae244afec95466bc2efb92e4ea0091'
auth_token = '97ce5defe63d5ccb93ec45fdf519b1a9'
twilio_phone_number = '+16188674613'

client = Client(account_sid, auth_token)

registered_users = {}
user_locations = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    name = data.get('name')
    number = data.get('number')

    registered_users[name] = number
    return jsonify({"message": f"User '{name}' registered with number '{number}'."}), 201

@app.route('/send_location', methods=['POST'])
def send_location():
    data = request.json
    user_name = data.get('name')

    if user_name in registered_users:
        if user_name in user_locations:
            location_data = user_locations[user_name]
            send_location_to_recipients(user_name, location_data)
            return jsonify({"message": "Location information sent to registered contacts."}), 200
        else:
            return jsonify({"error": "Location information not available for the user."}), 404
    else:
        return jsonify({"error": "User not registered."}), 404

def send_location_to_recipients(user_name, location_data):
    recipient_numbers = [number for name, number in registered_users.items() if name != user_name]
    for number in recipient_numbers:
        send_location_to_number(number, location_data)

def send_location_to_number(recipient_number, location_data):
    message_body = f"Emergency: {location_data}"
    message = client.messages.create(
        body=message_body,
        from_=twilio_phone_number,
        to=recipient_number
    )
    print(f"SMS sent to '{recipient_number}': {message.sid}")

if __name__ == '__main__':
    app.run(debug=True)

