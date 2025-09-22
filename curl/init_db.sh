#!/bin/bash

# Base URL of the REST API
BASE_URL="http://localhost:8000"

ADMIN_API_KEY="your_admin_api_key_here"  

# Test GET all resources
curl -X GET "$BASE_URL/" -H "Accept: application/json"
echo -e "\n" 

#add jimothy and johnathy users
# Create jimothy user and extract the api key from the response
JIMAPI_KEY=$(curl -s -X POST "$BASE_URL/accounts/create/" \
    -H "x-api-key: $ADMIN_API_KEY" \
    -d 'username=jimothy' | jq -r '.api_key')

echo "jimothy API key: $JIMAPI_KEY"
echo -e "\n"

JONAPI_KEY=$(curl -s -X POST "$BASE_URL/accounts/create/" \
    -H "x-api-key: $ADMIN_API_KEY" \
    -d 'username=johnathy' | jq -r '.api_key')

echo "johnathy API key: $JONAPI_KEY"
echo -e "\n"

# Create a new project for jimothy

curl -X POST "$BASE_URL/projects/create/" \
    -H "x-api-key: $JIMAPI_KEY" \
    -d 'name=Jimothy Project&description=A project for Jimothy'
echo -e "\n"


curl -X POST "$BASE_URL/projects/create/" \
    -H "x-api-key: $JIMAPI_KEY" \
    -d 'name=Jimothy Project2&description=Another project for Jimothy'
echo -e "\n"

# Create a new project for johnathy

curl -X POST "$BASE_URL/projects/create/" \
    -H "x-api-key: $JONAPI_KEY" \
    -d 'name=Johnathy Project&description=A project for Johnathy'
echo -e "\n"

curl -X POST "$BASE_URL/projects/create/" \
    -H "x-api-key: $JONAPI_KEY" \
    -d 'name=Johnathy Project2&description=Another project for Johnathy'
echo -e "\n"

# List all projects for jimothy
curl -X GET "$BASE_URL/projects/" \
    -H "x-api-key: $JIMAPI_KEY"
echo -e "\n"

# List all projects for johnathy
curl -X GET "$BASE_URL/projects/" \
    -H "x-api-key: $JONAPI_KEY"
echo -e "\n"

# Add johnathy as an associated user to one of jimothy's projects (assuming project ID is 1)
curl -X PUT "$BASE_URL/projects/1/add_user/" \
    -H "x-api-key: $JIMAPI_KEY" \
    -d 'username=johnathy'
echo -e "\n"

# List all projects for johnathy again to see the added project
curl -X GET "$BASE_URL/projects/" \
    -H "x-api-key: $JONAPI_KEY"
echo -e "\n"

# add some hypothesese to jimothy's project (project ID 1)
curl -X POST "$BASE_URL/projects/1/hypotheses/create/" \
    -H "x-api-key: $JIMAPI_KEY" \
    -d 'title=Hypothesis 1 for Jimothy&commit=abc1234&description=This is the first hypothesis for Jimothy'
echo -e "\n"

curl -X POST "$BASE_URL/projects/1/hypotheses/create/" \
    -H "x-api-key: $JONAPI_KEY" \
    -d 'title=Hypothesis 2 from Johnathy&commit=def5678&description=This is the second hypothesis for Johnathy'
echo -e "\n"

# List all hypotheses for jimothy's project (project ID 1)
curl -X GET "$BASE_URL/projects/1/hypotheses/" \
    -H "x-api-key: $JIMAPI_KEY"
echo -e "\n"

# add two experiments to the first hypothesis (hypothesis ID 1)
curl -X POST "$BASE_URL/hypotheses/1/experiments/create/" \
    -H "x-api-key: $JIMAPI_KEY" \
    -d 'title=Experiment 1 for Hypothesis 1&description=This is the first experiment for Hypothesis 1&experiment_type=svm&learning_rate=0.01&batch_size=32&epochs=10'
echo -e "\n"  

curl -X POST "$BASE_URL/hypotheses/1/experiments/create/" \
    -H "x-api-key: $JONAPI_KEY" \
    -d 'title=Experiment 2 for Hypothesis 1 from Johnathy&description=This is the second experiment for Hypothesis 1 from Johnathy&experiment_type=rf&learning_rate=0.01&batch_size=32&epochs=10'
echo -e "\n"

# add two experiments to the second hypothesis (hypothesis ID 2)
curl -X POST "$BASE_URL/hypotheses/2/experiments/create/" \
    -H "x-api-key: $JIMAPI_KEY" \
    -d 'title=Experiment 1 for Hypothesis 2 from Jimothy&description=This is the first experiment for Hypothesis 2 from Jimothy&experiment_type=nn&learning_rate=0.01&batch_size=32&epochs=10'
echo -e "\n"

curl -X POST "$BASE_URL/hypotheses/2/experiments/create/" \
    -H "x-api-key: $JONAPI_KEY" \
    -d 'title=Experiment 2 for Hypothesis 2 from Johnathy&description=This is the second experiment for Hypothesis 2 from Johnathy&experiment_type=nn&learning_rate=0.01&batch_size=32&epochs=10'
echo -e "\n"



# List all project experiments
curl -X GET "$BASE_URL/projects/1/experiments/" \
    -H "x-api-key: $JIMAPI_KEY"
echo -e "\n"

#add results to the first experiment (experiment ID 1)
curl -X POST "$BASE_URL/experiments/1/results/create/" \
    -H "x-api-key: $JIMAPI_KEY" \
    -d 'accuracy=0.95&loss=0.05&ROC=0.9&PR_AUC=0.95&weights_path=s3://pathtoweights.pth&training_time=3600&comment=Great results!'
echo -e "\n"

#add results to the third experiment (experiment ID 3)
curl -X POST "$BASE_URL/experiments/3/results/create/" \
    -H "x-api-key: $JONAPI_KEY" \
    -d 'accuracy=0.085&loss=0.99&ROC=0.0&PR_AUC=0.0&weights_path=s3://pathtoweights.pth&training_time=3600&comment=Very Bad results!'
echo -e "\n"

#list all the results for the project (project ID 1)
curl -X GET "$BASE_URL/projects/1/results/" \
    -H "x-api-key: $JIMAPI_KEYecho -e "\n"