BASE_URL="http://localhost:8000"

ADMIN_API_KEY="your_admin_api_key_here"  


# preamble to get the api keys for the two users so we can use them in the tests
#test should be started from the init db state 

# GET user api keys for the two users so we can use them in the tests
KEYS=$(curl -X GET "http://localhost:8000/accounts/" -H "x-api-key:$ADMIN_API_KEY" -H "Accept: application/json")
echo $KEYS
JIMAPI_KEY=$(echo $KEYS | jq -r '.[] | select(.username=="jimothy") | .api_key')
JONAPI_KEY=$(echo $KEYS | jq -r '.[] | select(.username=="johnathy") | .api_key')

echo "jimothy API key: $JIMAPI_KEY"
echo "johnathy API key: $JONAPI_KEY"
echo -e "\n"

#create a new project for jimothy to hold the hypotheses, experiments, and results we will be testing
response=$(curl -s -X POST "$BASE_URL/projects/create/" \
    -H "x-api-key: $JIMAPI_KEY" \
    -d 'name=Jimothy Test Project newnewnnewewnewnew&description=Project for hypothesis/experiment/results testing'| jq -S .)
echo -e $response

PROJECT_ID=$(echo $response | jq -r '.project_id')
echo "Project ID for testing: $PROJECT_ID"
echo -e "\n"


# Create three hypotheses to use in the tests
HID1R=$(curl -s -X POST "$BASE_URL/projects/$PROJECT_ID/hypotheses/create/" -H "x-api-key:$JIMAPI_KEY" -H "Content-Type: application/x-www-form-urlencoded" -d 'title=Test Hypothesis 1&description=svm good.&commit=abc123' | jq -S .)
HID2R=$(curl -s -X POST "$BASE_URL/projects/$PROJECT_ID/hypotheses/create/" -H "x-api-key:$JIMAPI_KEY" -H "Content-Type: application/x-www-form-urlencoded" -d 'title=Test Hypothesis 2&description=random forest good.&commit=def456' | jq -S .)
HID3R=$(curl -s -X POST "$BASE_URL/projects/$PROJECT_ID/hypotheses/create/" -H "x-api-key:$JIMAPI_KEY" -H "Content-Type: application/x-www-form-urlencoded" -d 'title=Test Hypothesis 3&description=neural network good at biology&commit=ghi789' | jq -S .)

echo "Hypothesis creation responses:"
echo $HID1R | jq -S .
echo $HID2R | jq -S .
echo $HID3R | jq -S .

HID1=$(echo $HID1R | jq -r '.hypothesis_id')
HID2=$(echo $HID2R | jq -r '.hypothesis_id')
HID3=$(echo $HID3R | jq -r '.hypothesis_id')
echo "Hypothesis IDs for testing: $HID1, $HID2, $HID3"
echo -e "\n"

#list hypotheses to verify they were created correctly
curl -s -X GET "$BASE_URL/projects/$PROJECT_ID/hypotheses/" -H "x-api-key:$JIMAPI_KEY" -H "Accept: application/json" |  jq -S .
echo -e "\n"

#list the detaills of HID3
curl -s -X GET "$BASE_URL/hypotheses/$HID3/" -H "x-api-key:$JIMAPI_KEY" -H "Accept: application/json" |  jq -S .
#edit HID3

curl -s -X PUT "$BASE_URL/hypotheses/$HID3/edit/" -H "x-api-key:$JIMAPI_KEY" -H "Content-Type: application/x-www-form-urlencoded" -d 'title=Updated Hypothesis 3' |  jq -S .
#list the details of HID3 again to verify the edit worked
curl -s -X GET "$BASE_URL/hypotheses/$HID3/" -H "x-api-key:$JIMAPI_KEY" -H "Accept: application/json" |  jq -S .
echo -e "\n"

# Hypotheses: list, search, filter

echo "Search and filter tests:" 
echo "search for 'updated' in title/description"
curl -s -X GET "$BASE_URL/projects/$PROJECT_ID/hypotheses/search/?q=updated" -H "x-api-key:$JIMAPI_KEY" -H "Accept: application/json" |  jq -S .
echo "search for 'svm' in title/description"
curl -s -X GET "$BASE_URL/projects/$PROJECT_ID/hypotheses/search/?q=svm" -H "x-api-key:$JIMAPI_KEY" -H "Accept: application/json" |  jq -S .
echo "filter by keyword 'biology'"
curl -s -X GET "$BASE_URL/projects/$PROJECT_ID/hypotheses/filter_by_keyword/?keyword=biology" -H "x-api-key:$JIMAPI_KEY" -H "Accept: application/json" |  jq -S .

#delete HID2 to test delete
curl -s -X DELETE "$BASE_URL/hypotheses/$HID2/delete/" -H "x-api-key:$JIMAPI_KEY"
#list hypotheses to verify HID2 was deleted
curl -s -X GET "$BASE_URL/projects/$PROJECT_ID/hypotheses/" -H "x-api-key:$JIMAPI_KEY" -H "Accept: application/json" |  jq -S .
echo -e "\n"


# Experiments: create, detail, edit, delete
curl -s -X POST "$BASE_URL/hypotheses/$HID3/experiments/create/" -H "x-api-key:$JIMAPI_KEY" -H "Content-Type: application/x-www-form-urlencoded" -d 'title=Test Experiment&description=Experiment desc.&experiment_type=nn&learning_rate=0.01&batch_size=32&epochs=10' | jq -S .
curl -s -X POST "$BASE_URL/hypotheses/$HID3/experiments/create/" -H "x-api-key:$JIMAPI_KEY" -H "Content-Type: application/x-www-form-urlencoded" -d 'title=Test Experiment&description=Experiment desc.&experiment_type=svm&learning_rate=0.01&batch_size=32&epochs=10' | jq -S .
curl -s -X POST "$BASE_URL/hypotheses/$HID3/experiments/create/" -H "x-api-key:$JIMAPI_KEY" -H "Content-Type: application/x-www-form-urlencoded" -d 'title=Test Experiment&description=Experiment desc.&experiment_type=rf&learning_rate=0.01&batch_size=32&epochs=10' | jq -S .

curl -s -X POST "$BASE_URL/hypotheses/$HID1/experiments/create/" -H "x-api-key:$JIMAPI_KEY" -H "Content-Type: application/x-www-form-urlencoded" -d 'title=Test Experiment&description=Experiment desc.&experiment_type=nn&learning_rate=0.01&batch_size=32&epochs=10' | jq -S .
curl -s -X POST "$BASE_URL/hypotheses/$HID1/experiments/create/" -H "x-api-key:$JIMAPI_KEY" -H "Content-Type: application/x-www-form-urlencoded" -d 'title=Test Experiment&description=Experiment desc.&experiment_type=svm&learning_rate=0.01&batch_size=32&epochs=10' | jq -S .
curl -s -X POST "$BASE_URL/hypotheses/$HID1/experiments/create/" -H "x-api-key:$JIMAPI_KEY" -H "Content-Type: application/x-www-form-urlencoded" -d 'title=Test Experiment&description=Experiment desc.&experiment_type=rf&learning_rate=0.01&batch_size=32&epochs=10' | jq -S .

#list experiments to verify they were created correctly
curl -s -X GET "$BASE_URL/projects/$PROJECT_ID/experiments/" -H "x-api-key:$JIMAPI_KEY" -H "Accept: application/json" |  jq -S .
EXPERIMENT_ID1=$(curl -s -X GET "$BASE_URL/projects/$PROJECT_ID/experiments/" -H "x-api-key:$JIMAPI_KEY" -H "Accept: application/json" | jq -r '.[0].id')
EXPERIMENT_ID2=$(curl -s -X GET "$BASE_URL/projects/$PROJECT_ID/experiments/" -H "x-api-key:$JIMAPI_KEY" -H "Accept: application/json" | jq -r '.[1].id')

EXPERIMENT_ID3=$(curl -s -X GET "$BASE_URL/projects/$PROJECT_ID/experiments/" -H "x-api-key:$JIMAPI_KEY" -H "Accept: application/json" | jq -r '.[2].id')
echo "Experiment IDs for testing: $EXPERIMENT_ID1, $EXPERIMENT_ID2, $EXPERIMENT_ID3"
echo -e "\n"

curl -s -X GET "$BASE_URL/experiments/$EXPERIMENT_ID1/" -H "x-api-key:$JIMAPI_KEY" -H "Accept: application/json"

curl -s -X PUT "$BASE_URL/experiments/$EXPERIMENT_ID1/edit/" -H "x-api-key:$JIMAPI_KEY" -H "Content-Type: application/x-www-form-urlencoded" -d 'title=Updated Experiment name&learning_rate=0.02'

#delete EXPERIMENT_ID2 to test delete
curl -s -X DELETE "$BASE_URL/experiments/$EXPERIMENT_ID2/delete/" -H "x-api-key:$JIMAPI_KEY" | jq -S .
#list experiments to verify EXPERIMENT_ID2 was deleted
curl -s -X GET "$BASE_URL/projects/$PROJECT_ID/experiments/" -H "x-api-key:$JIMAPI_KEY" -H "Accept: application/json" |  jq -S .



# Hypotheses: create, detail, edit, delete


R1Response1=$(curl -s -X POST "$BASE_URL/experiments/$EXPERIMENT_ID1/results/create/" -H "x-api-key:$JIMAPI_KEY" -H "Content-Type: application/x-www-form-urlencoded" -d 'accuracy=0.87&loss=0.15&ROC=0.88&PR_AUC=0.86&weights_path=s3://path/to/weights.pth&training_time=3600&comment=Good results!')
R1Response2=$(curl -s -X POST "$BASE_URL/experiments/$EXPERIMENT_ID3/results/create/" -H "x-api-key:$JIMAPI_KEY" -H "Content-Type: application/x-www-form-urlencoded" -d 'accuracy=0.0&loss=1&ROC=0.0&PR_AUC=0.0&weights_path=s3://path/to/weights.pth&training_time=36000&comment=very bad results!')
echo "Result creation responses:"
echo $R1Response1 | jq -S .
echo $R1Response2 | jq -S .
RESULT_ID1=$(echo $R1Response1 | jq -r '.result_id')
RESULT_ID2=$(echo $R1Response2 | jq -r '.result_id')
echo "Result IDs for testing: $RESULT_ID1, $RESULT_ID2"

curl -s -X GET "$BASE_URL/results/$RESULT_ID2/" -H "x-api-key:$JIMAPI_KEY" -H "Accept: application/json" | jq -S .
curl -s -X PUT "$BASE_URL/results/$RESULT_ID2/edit/" -H "x-api-key:$JIMAPI_KEY" -H "Content-Type: application/x-www-form-urlencoded" -d 'comment=utter Failure' | jq -S .
curl -s -X GET "$BASE_URL/results/$RESULT_ID2/" -H "x-api-key:$JIMAPI_KEY" -H "Accept: application/json" | jq -S .

curl -s -X DELETE "$BASE_URL/results/$RESULT_ID2/delete/" -H "x-api-key:$JIMAPI_KEY" | jq -S .


# Results: list
curl -s -X GET "$BASE_URL/projects/$PROJECT_ID/results/" -H "x-api-key:$JIMAPI_KEY" -H "Accept: application/json" | jq -S .

curl -s -X DELETE "$BASE_URL/experiments/$EXPERIMENT_ID3/delete/" -H "x-api-key:$JIMAPI_KEY" | jq -S .

#list experiments to verify EXPERIMENT_ID3 was deleted
curl -s -X GET "$BASE_URL/projects/$PROJECT_ID/experiments/" -H "x-api-key:$JIMAPI_KEY" -H "Accept: application/json" | jq -S .

#delete project to clean up and test delete project
curl -s -X DELETE "$BASE_URL/projects/$PROJECT_ID/delete/" -H "x-api-key:$JIMAPI_KEY" | jq -S .
#list projects to verify the project was deleted
curl -s -X GET "$BASE_URL/projects/" -H "x-api-key:$JIMAPI_KEY" -H "Accept: application/json" | jq -S .
echo -e "\n"


