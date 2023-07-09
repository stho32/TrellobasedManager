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

    if response.status_code // 100 == 2:
        print(f"SMS sent successfully. Status: {response.status_code}")
    else:
        print(f"Failed to send SMS. Status: {response.status_code}")

    return response
