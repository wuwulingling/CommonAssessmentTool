Team TicTech 

Project -- Feature Development Backend: Create CRUD API's for Client

User Story

As a user of the backend API's, we want to call API's that can retrieve, update, and delete information of clients who have already registered with the CaseManagment service so that we more efficiently help previous clients make better decisions on how to be gainfully employed.

Acceptance Criteria
- Provide REST API endpoints so that the Frontend can use them to get information on an existing client.
- Document how to use the REST API
- Choose and create a database to hold client information
- Add tests


This will contain the model used for the project that based on the input information will give the social workers the clients baseline level of success and what their success will be after certain interventions.

The model works off of dummy data of several combinations of clients alongside the interventions chosen for them as well as their success rate at finding a job afterward. The model will be updated by the case workers by inputing new data for clients with their updated outcome information, and it can be updated on a daily, weekly, or monthly basis.

This also has an API file to interact with the front end, and logic in order to process the interventions coming from the front end. This includes functions to clean data, create a matrix of all possible combinations in order to get the ones with the highest increase of success, and output the results in a way the front end can interact with.
