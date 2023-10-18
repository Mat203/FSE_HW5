from flask import Flask, request, jsonify
from data_procession import generate_report  

app = Flask(__name__)

@app.route('/api/report/<report_name>', methods=['POST'])
def generate_report_endpoint(report_name):
    if request.method == 'POST':
        data = request.get_json()

        if 'metrics' not in data or 'users' not in data:
            return jsonify({"error": "Metrics and users are required."}), 400

        metrics = data['metrics']
        users = data['users']

        generate_report(report_name, metrics, users)
        return jsonify({"message": f"Report '{report_name}' successfully created."}), 200

if __name__ == '__main__':
    app.run(debug=True)
