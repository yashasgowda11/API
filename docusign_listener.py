# docusign_listener.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/docusign-listener', methods=['POST'])
def docusign_listener():
    data = request.get_json()

    try:
        # Navigate into the structure to find recipients -> signers
        signers = data.get('recipients', {}).get('signers', [])

        contract_number_value = None
        edms_description_value = None

        for signer in signers:
            tabs = signer.get('tabs', {})
            text_tabs = tabs.get('textTabs', [])
            list_tabs = tabs.get('listTabs', [])

            # Find Contract_Number
            for tab in text_tabs:
                if tab.get('tabLabel') == 'Contract_Number':
                    contract_number_value = tab.get('value')

            # Find EDMS_Description
            for tab in list_tabs:
                if tab.get('tabLabel') == 'EDMS_Description':
                    edms_description_value = tab.get('listSelectedValue')

        return jsonify({
            'Contract_Number': contract_number_value,
            'EDMS_Description': edms_description_value
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(port=5000, debug=True)
