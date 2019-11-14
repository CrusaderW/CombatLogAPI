from combatLogAPI import create_app

json_streamLogs = {
  "username": "GeneralMolan",
  "datetimeStart": "2019-10-23T11:18:33.232Z",
  "datetimeEnd": "2019-10-23T11:18:33.232Z",
  "logs": [
    {
      "Key": "2019-10-23T11:18:33.232Z",
      "Value": "2019-10-23T11:18:33.232Z INFO    COMBAT    - Combat _||_ Event=[Your Vicious Stomp hit Practice Dummy for 196  damage.] "
    },
    {
      "Key": "2019-10-23T11:10:35.896Z",
      "Value": "2019-10-23T11:10:35.896Z INFO    COMBAT    - Combat _||_ Event=[Your Strong Swing hit Practice Dummy for 65  damage.] "
    },
    {
      "Key": "2019-10-23T11:10:36.029Z",
      "Value": "2019-10-23T11:10:36.029Z INFO    COMBAT    - Combat _||_ Event=[Your Strong Swing hit Practice Dummy for 31  damage.] "
    },
    {
      "Key": "2019-10-23T11:10:36.97Z",
      "Value": "2019-10-23T11:10:36.970Z INFO    COMBAT    - Combat _||_ Event=[Your Crushing Overhead hit Practice Dummy for 324  damage (Critical).] "
    },
  ]
}

def test_streamLogs(client):
    response = client.post('/streamLogs', json=json_streamLogs)
    json_response = response.get_json()
    assert json_response == {"lines_parsed":4}

