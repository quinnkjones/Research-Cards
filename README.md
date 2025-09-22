# Research-Cards
A card database backend intended to solve the problem of storage and organization of machine learning results in a kanban board style arrangement

When I read the prompt the first thing that came to mind when I considered what to make was the cards in project managment systems, and since this role is to Advocate for Research Development what is more relatable in managing an ML project than trying to keep track of all of the various hypotheses, experiments, and results that you and your team churn through in search of high accuracy.  


This project keeps track of ML Projects which are owned by Users and can be collaborated on by other Users in the system.  

Users can add, edit, and remove Hypotheses, Experiments, and Results to the projects which they either own or have been added to by the owner. 

Users can then review the current state of the Projects they are allowed to through the API and see and search through the Hypotheses, Experiments, and Results.  

Users are created, deleted, and viewed by requests that are authenticated by a special admin key which can be set in the backend. 

## Getting Started

Assuming you have a working installation of docker installed 

```
git clone git@github.com:quinnkjones/Research-Cards.git
cd Research-Cards
sudo docker build -t research-cards . #builds the api image 
sudo docker compose up 
#brings online the postgres @localhost:5432 ,the api @localhost:8000, 
#and a DB admin website for inspecting the db purposes if we get curious @ localhost:8080
```

Then we will go to the curl folder to test/demonstrate the API. There we will find `init_db.sh`, `project_and_user_tests.sh`, and `hypotheses_experiement_results.sh`.  The DB is already initialized so avoid init_db but that is the script that I used to do so. 
`project_and_user_tests.sh` tests the creation, deletion of users; adding and removal of associate users onto a project and access rights provisions.  

`hypotheses_experiment_results.sh` covers the topics of the creation, editing , deletion, viewing and searching of projects, hypotheses, experiments, and results.  

They require curl and jq to run, curl to send the requests and jq does a couple of things for us it makes the json response output easy to read by adding spaces and indents and it is also used in some cases to extract api_keys and primary_keys into bash variables for use in commands further down in the script. They can be installed in the following way

```
sudo apt install curl jq
```

Then the scripts can be run 

```
cd Research-Cards/curl
bash project_and_user_test.sh
bash hypotheses_experiment_results.sh
```