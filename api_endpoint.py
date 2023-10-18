from flask import Flask, request, jsonify
from data_procession import generate_report, get_reports_in_date_range  
import json
from dateutil.parser import parse

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
    
@app.route('/api/report/<report_name>', methods=['GET'])
def get_report_in_date_range(report_name):
    from_date_str = request.args.get('from')
    to_date_str = request.args.get('to')

    if not from_date_str or not to_date_str:
        return jsonify({"error": "Both 'from' and 'to' dates are required"}), 400

    try:
        from_date = parse(from_date_str)
        to_date = parse(to_date_str)
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    with open(f'{report_name}.json', 'r') as file:
        report_data = json.load(file)

    reports = get_reports_in_date_range(report_data, from_date, to_date)
    return jsonify(reports)

if __name__ == '__main__':
    app.run(debug=True)
