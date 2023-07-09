import requests
import json


def send_sms(token_id, token, recipient, message, send_at=None):
    base_url = "https://api.sipgate.com/v2"
    sms_id = "s0"

    url = base_url + "/sessions/sms"

    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    data = {
        "smsId": sms_id,
        "message": message,
        "recipient": recipient,
    }

    if send_at:
        data["sendAt"] = send_at

    response = requests.post(
        url, headers=headers, auth=(token_id, token), data=json.dumps(data)
    )

    if response.status_code != 200:
        print(f"Failed to send SMS: {response.content}")
    else:
        print(
            f"SMS sent successfully. Status: {response.status_code}, Body: {response.json()}"
        )

    return response


# Example usage:
# token_id = "YOUR_TOKEN_ID"
# token = "YOUR_TOKEN"
# recipient = "YOUR_RECIPIENT_NUMBER"
# message = "YOUR_MESSAGE"
# send_sms(token_id, token, recipient, message)
