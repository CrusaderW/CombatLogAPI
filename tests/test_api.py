import json
from combatLogAPI import create_app, masterDF

def test_masterDF_is_Singleton(client):
        masterDF1=masterDF.masterDF()
        masterDF2=masterDF.masterDF()
        assert masterDF1 == masterDF2

def test_streamLogs(client):
	response = client.post('/streamLogs', json=json.dumps(json_Molan))
	json_response = response.get_json()
	assert json_response == {"username": "GeneralMolan",
				 "lines_parsed":4,
				 'lines_skipped': 0,
  			      	 "parsed_logs": {'damage_done':
					   		{'GeneralMolan': 616.0},
                                                 'damage_recieved':
                                                        {'Practice Dummy': 616.0},
					         'healing_done': {},
					         'healing_recieved': {},
    			        		}
				}

	response = client.post('/streamLogs', json=json.dumps(json_Crusader))
	json_response = response.get_json()
	assert json_response == {"username": "CrusaderW",
				 "lines_parsed":7,
				 'lines_skipped': 0,
  			      	 "parsed_logs": {'damage_done':
					   		{'GeneralMolan': 616.0,
					   		 'CrusaderW': 910.0},
					      	 'damage_recieved':
                                                        {"Practice Dummy":1526.0},
					         'healing_done': {},
					         'healing_recieved': {},
    			        		}
				}

json_Molan = {
  "username": "GeneralMolan",
  "filename": "test",
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

json_Crusader = {
  "username": "CrusaderW",
  "filename": "test",
  "logs": [
    {
      "Key": "2019-09-02T23:18:50.522Z",
      "Value": "2019-09-02T23:18:50.522Z INFO    COMBAT    - Combat _||_ Event=[Your Basic Shot hit Practice Dummy for 438  damage.] "
    },
    {
      "Key": "2019-09-02T23:18:55.459Z",
      "Value": "2019-09-02T23:18:55.459Z INFO    COMBAT    - Combat _||_ Event=[Your Ricochet Shot hit Practice Dummy for 106  damage.] "
    },
    {
      "Key": "2019-09-02T23:18:55.628Z",
      "Value": "2019-09-02T23:18:55.628Z INFO    COMBAT    - Combat _||_ Event=[Your Ricochet Shot hit Practice Dummy for 106  damage.] "
    },
    {
      "Key": "2019-09-02T23:18:55.759Z",
      "Value": "2019-09-02T23:18:55.759Z INFO    COMBAT    - Combat _||_ Event=[Your Ricochet Shot hit Practice Dummy for 136  damage (Critical).] "
    },
    {
      "Key": "2019-09-02T23:19:01.765Z",
      "Value": "2019-09-02T23:19:01.765Z INFO    COMBAT    - Combat _||_ Event=[Your Fire Wall hit Practice Dummy for 40  damage.] "
    },
    {
      "Key": "2019-09-02T23:19:01.765Z",
      "Value": "2019-09-02T23:19:01.765Z INFO    COMBAT    - Combat _||_ Event=[Your Fire Wall hit Practice Dummy for 43  damage.] "
    },
    {
      "Key": "2019-09-02T23:19:01.766Z",
      "Value": "2019-09-02T23:19:01.766Z INFO    COMBAT    - Combat _||_ Event=[Your Fire Wall hit Practice Dummy for 41  damage.] "
    },
  ]
}
