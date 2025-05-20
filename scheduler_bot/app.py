from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule', methods=['POST'])
def schedule():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    date = data.get('date')
    time = data.get('time')
    message = f"Meeting scheduled for {name} on {date} at {time}. Confirmation will be sent to {email}."
    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(debug=True)
