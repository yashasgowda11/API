from flask import Flask, request, jsonify

app = Flask(__name__)  # <-- This must come before any @app.route()

@app.route('/docusign-listener', methods=['POST'])
def docusign_listener():
    data = request.get_json()

    try:
        signers = data.get('recipients', {}).get('signers', [])
        contract_number_value = None
        edms_description_value = None

        for signer in signers:
            tabs = signer.get('tabs', {})
            text_tabs = tabs.get('textTabs', [])
            list_tabs = tabs.get('listTabs', [])

            for tab in text_tabs:
                if tab.get('tabLabel') == 'Contract_Number':
                    contract_number_value = tab.get('value')

            for tab in list_tabs:
                if tab.get('tabLabel') == 'EDMS_Description':
                    edms_description_value = tab.get('listSelectedValue')

        # Print values for Render logs
        print(f"Received Contract_Number: {contract_number_value}")
        print(f"Received EDMS_Description: {edms_description_value}")

        return jsonify({
            'Contract_Number': contract_number_value,
            'EDMS_Description': edms_description_value
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Optional: GET method to check if API is live
@app.route('/', methods=['GET'])
def health_check():
    return "API is Live!", 200
