from combatLogAPI import create_app

json_streamLogs = {
  "username": "GeneralMolan",
  "datetimeStart": "2019-10-23T11:18:33.232Z",
  "datetimeEnd": "2019-10-23T11:18:33.232Z",
  "logs": [
    {
      "Key": "2019-10-23T11:18:33.232Z",
      "Value": "2019-10-23T11:18:33.232Z INFO    COMBAT    - Combat _||_ Event=[Your Vicious Stomp hit Practice Dummy for 196  damage.] "
    }
  ]
}

def test_streamLogs(client):
    response = client.post('/streamLogs', json=json_streamLogs)
    json_response = response.get_json()
    assert json_response == {
            "friendly":[
                {
                    "username": "GeneralMolan",
                    "total_damage": 196,
                }
            ]
    }

