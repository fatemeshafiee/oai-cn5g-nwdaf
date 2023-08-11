import json
import requests
import typer
from flask import Flask, request

app = typer.Typer()

flask_app = Flask(__name__)

@app.command()
def analytics(
    json_file: str = typer.Argument(..., help="JSON analytics request file name"),
):
    # Read JSON file
    with open(json_file) as file:
        data = json.load(file)

    # Extract parameters from JSON
    event_id = data['event-id']
    ana_req = json.dumps(data['ana-req'])
    event_filter = json.dumps(data['event-filter'])
    supported_features = json.dumps(data['supported-features'])
    tgt_ue = json.dumps(data['tgt-ue'])

    # Construct the URL
    base_url = 'http://nwdaf.cnx.eurecom.fr/nnwdaf-analyticsinfo/v1/analytics'
    params = {
        'event-id': event_id,
        'ana-req': ana_req,
        'event-filter': event_filter,
        'supported-features': supported_features,
        'tgt-ue': tgt_ue
    }

    # Send GET request
    response = requests.get(base_url, params=params)

    # Parse the JSON response
    parsed_response = json.loads(response.text)

    # Print the result as formatted JSON
    typer.echo(json.dumps(parsed_response, indent=4))
    
@app.command()
def subscribe(
    subscription_file: str = typer.Argument(..., help="JSON subscription file name"),
):
    # Define the URL to send the subscription request to
    subscription_url = 'http://nwdaf.cnx.eurecom.fr/nnwdaf-eventssubscription/v1/subscriptions'

    # Load subscription data from the JSON file
    with open(subscription_file) as f:
        subscription_data = json.load(f)

    # Send the subscription request
    response = requests.post(subscription_url, json=subscription_data)

    # Print the response status code and content as formatted JSON
    #typer.echo(json.dumps({
    #    'subscription_status_code': response.status_code,
    #    'subscription_headers': dict(response.headers),
    #    'subscription_response': json.loads(response.content)
    #}, indent=4))
    
    @flask_app.route('/notification', methods=['POST'])
    def handle_notification():
        data = request.json
        notif_data = data

        typer.echo(f'\nReceived notification for event: {notif_data["event"]}')
        
        # Print notif_data in JSON format
        typer.echo(json.dumps(notif_data, indent=4))
        
        return 'OK'
      
    flask_app.run(host='0.0.0.0', port=3000, debug=True)    
    
    
if __name__ == '__main__':
    app()
