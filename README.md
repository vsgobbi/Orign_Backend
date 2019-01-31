**Orign back end using Django and Django Rest Frameworks

***Github assignment link: https://gist.github.com/joaodepaula/4aef541ef5ad115eb8514dbec4cb9f38




***How to run it:
	
	1 - Install necessary lib on virtual enviroment:

		cd Orign_BackEnd/
		virtualenv -p pythonversion venv/
		source venv/bin/activate
		pip install -r requirements.txt

	1 - Use the script ./runserver.sh
		
		cd orign/
		chmod +x runserver.sh
		./runserver.sh

	2 - Use the REST Framework API frontend in any browser acessing:
		http://localhost:8000 
		or you can use httpie 
		pip install httpie
		or curl


***How to execute some tests:
	
	1.0 - Create personal information with curl or with API router on http://localhost:8000/clients:

		curl -X POST http://127.0.0.1:8000/clients/ -d '{"age": 35, "dependents": 2, "income": 0, "marital_status": "married"}' -H "Content-Type: application/json"
	
	1.1 - Update the cliente information with "PUT" method at the current client ID=1: 
		
		curl -X PUT http://127.0.0.1:8000/clients/1/ -d '{"houses": [{"key": 1, "ownership_status": "owned"}, {"key": 2, "ownership_status": "mortgaged"}], "vehicles": [{"key": 1, "year": 2018}],"risk_questions": [0, 1, 0]}' -H "Content-Type: application/json"
	

	2.0 - Create or check existing Houses and Vehicles instances on model:
		Use the POST method for 'houses' in:
		"http://localhost:8000/houses/",
	2.1 - The same for 'vehicles':
		"http://localhost:8000/vehicles/",

	2.2 - Creating client full profile adding all dict data and its additional attributes:

		curl -X POST http://127.0.0.1:8000/updated_clients/ -d '{"age": 35, "dependents": 2, "houses": [{"key": 1, "ownership_status": "owned"},{"key": 2, "ownership_status": "mortgaged"}],"income": 0,"marital_status": "married","risk_questions": [0, 1, 0],"vehicles": [{"key": 1, "year": 2018}]}' -H "Content-Type: application/json"

	3 - Check created full data:

		curl http://localhost:8000/clients/json
		or:
		http http://localhost:8000/clients/json


	4 - Process payload data and receive POST as Json with curl command:

		curl -X POST http://127.0.0.1:8000/clients/ -d '{"age":"35", "dependents":"2", "income":"0", "marital_status":"married", "risk_questions":"regular"}' -H "Content-Type: application/json"

	4.1 - Retrieve Json Updated Client data:

		curl http://127.0.0.1:8000/clients/json

	4.2 - Retrieving Risk Score evaluated data:

		curl -X POST http://127.0.0.1:8000/riskscore/ -d '{"client": {"age": 35,"dependents": 2,"houses": [{"key": 1, "ownership_status": "owned"},{"key": 2, "ownership_status": "mortgaged"}],"income": 0,"marital_status": "married","risk_questions": [0, 1, 0],"vehicles": [{"key": 1, "year": 2018}]}}' -H "Content-Type: application/json"

	4.3 - RiskScore Json evaluated data:

		curl http://localhost:8000/riskscore/ -H "Content-Type: application/json"
		
		or on browser:
		
		http://localhost:8000/riskscore/?format=json

****Note:

	Check the python version on creating the virtualenv, it is necessary Python 3.6.4
	with installed libs described on requirements

	To delete the database and recreate migrations use the following scripts:
	rmdb.sh
	Then:
	runserver.sh
