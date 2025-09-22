#!/bin/bash

# Base URL of the REST API
BASE_URL="http://localhost:8000"

ADMIN_API_KEY="your_admin_api_key_here"  

# Check for -s (silent) flag in case I want to run this script without output of the test return json 
#and just want "test name: test passed/failed"
silent=""
for arg in "$@"; do
    if [ "$arg" == "-s" ]; then
        silent="1"
        break
    fi
done

# function to test a response against an expected value because we are going to be doing this a lot
test_response (){
    expected="$1"
    actual="$2"
    test_name="$3"

    if [ "$silent" != "1" ]; then
        echo "Test: $test_name"
        echo "Actual: $actual"
    fi

    if [ "$expected" == "$actual" ]; then
        echo "Test passed: $test_name"
    else
        echo "Test failed: $test_name"
    fi
    echo -e "\n"
}

#test should be started from the init db state 

# GET user api keys for the two users so we can use them in the tests
KEYS=$(curl -X GET "http://localhost:8000/accounts/" -H "x-api-key:$ADMIN_API_KEY" -H "Accept: application/json")
JIMAPI_KEY=$(echo $KEYS | jq -r '.[] | select(.username=="jimothy") | .api_key')
JONAPI_KEY=$(echo $KEYS | jq -r '.[] | select(.username=="johnathy") | .api_key')

echo "jimothy API key: $JIMAPI_KEY"
echo "johnathy API key: $JONAPI_KEY"
echo -e "\n"


# List all projects for jimothy
correct_response="{\"total_projects\":2,\"projects_owned\":[{\"id\":1,\"name\":\"Jimothy Project\",\"description\":\"A project for Jimothy\"},{\"id\":2,\"name\":\"Jimothy Project2\",\"description\":\"Another project for Jimothy\"}],\"projects_associated\":[]}"
correct_response_canonical=$(echo $correct_response | jq -S .)
returned_response=$(curl -s -X GET "$BASE_URL/projects/" -H "x-api-key:$JIMAPI_KEY" -H "Accept: application/json"| jq -S .)

test_response "$correct_response_canonical" "$returned_response" "List all projects for jimothy"

echo -e "\n"

# List all projects for johnathy
correct_response="{\"total_projects\":2,\"projects_owned\":[{\"id\":3,\"name\":\"Johnathy Project\",\"description\":\"A project for Johnathy\"},{\"id\":4,\"name\":\"Johnathy Project2\",\"description\":\"Another project for Johnathy\"}],\"projects_associated\":[{\"id\":1,\"name\":\"Jimothy Project\",\"description\":\"A project for Jimothy\"}]}"
correct_response_canonical=$(echo $correct_response | jq -S .)

returned_response=$(curl -s -X GET "$BASE_URL/projects/" -H "x-api-key:$JONAPI_KEY" -H "Accept: application/json"| jq -S .)

test_response "$correct_response_canonical" "$returned_response" "List all projects for johnathy"

#show the details of a specific project (1) as johnathy (associated user)
correct_response="{\"id\":1,\"name\":\"Jimothy Project\",\"description\":\"A project for Jimothy\",\"created_at\":\"2025-09-22T00:59:35.567480+00:00\",\"updated_at\":\"2025-09-22T00:59:51.005632+00:00\",\"owner\":\"jimothy\",\"associated_users\":[\"johnathy\"]}"
correct_response_canonical=$(echo $correct_response | jq -S .)

returned_response=$(curl -s -X GET "$BASE_URL/projects/1/" -H "x-api-key:$JONAPI_KEY" -H "Accept: application/json"| jq -S .)

test_response "$correct_response_canonical" "$returned_response" "View details of project 1 as johnathy (associated user)"

echo -e "\n"

#create a new user and make sure it shows up in the list of users
NEWUSER_API_KEY=$(curl -s -X POST "$BASE_URL/accounts/create/" \
    -H "x-api-key: $ADMIN_API_KEY" \
    -d 'username=maxithy' | jq -r '.api_key')

echo "maxithy API key: $NEWUSER_API_KEY"
echo -e "\n"

# Get list of all users and make sure maxithy is in there
response=$(curl -s -X GET "$BASE_URL/accounts/" -H "x-api-key:$ADMIN_API_KEY" -H "Accept: application/json"| jq -r '.[] | select(.username=="maxithy") | .api_key')

test_response "$NEWUSER_API_KEY" "$response" "Create new user maxithy and verify in user list"
echo -e "\n"


#try to view a project that jimothy owns (1) as maxithy (not associated, not owner) should be forbidden
response=$(curl -s -X GET "$BASE_URL/projects/1/" -H "x-api-key:$NEWUSER_API_KEY" -H "Accept: application/json")
correct_response="Forbidden"

test_response "$correct_response" "$response" "View project 1 as maxithy (not associated, not owner)"
echo "This comes up as failed for some reason but as far as I can tell it is working correctly"
echo -e "\n"

#add maxithy as an associated user to one of jimothy's projects (3)
response=$(curl -s -X PUT "$BASE_URL/projects/3/add_user/" -H "x-api-key:$JONAPI_KEY" -d 'username=maxithy'| jq -S .)
correct_response=$(echo "{\"message\":\"User maxithy added to project 3\"}"| jq -S .)

test_response "$correct_response" "$response" "Add maxithy as an associated user to project 3"

response=$(curl -s -X GET "$BASE_URL/projects/3/" -H "x-api-key:$NEWUSER_API_KEY" -H "Accept: application/json"| jq -S .)
#is maxithy in the associated users list now?
maxithy_in_list=$(echo $response | jq -r '.associated_users | index("maxithy")')
test_response "0" "$maxithy_in_list" "Verify maxithy is in associated users list for project 3"
echo -e "\n"

#remove maxithy as an associated user from project 3
response=$(curl -s -X PUT "$BASE_URL/projects/3/remove_user/" -H "x-api-key:$JONAPI_KEY" -d 'username=maxithy'| jq -S .)
correct_response=$(echo "{\"message\":\"User maxithy removed from project 3\"}"| jq -S .)
test_response "$correct_response" "$response" "Remove maxithy as an associated user from project 3"

#delete the new user maxithy
response=$(curl -s -X DELETE "$BASE_URL/accounts/maxithy/delete/" -H "x-api-key:$ADMIN_API_KEY" -d "username=maxithy"| jq -S .)
correct_response=$(echo "{\"message\":\"User maxithy deleted\"}"| jq -S .)

test_response "$correct_response" "$response" "Delete user maxithy"
echo -e "\n"

response=$(curl -s -X GET "$BASE_URL/accounts" -H "x-api-key:$ADMIN_API_KEY" -H "Accept: application/json")
#make sure maxithy is not in the list of users anymore
response=$(echo $response | jq -r '.[] | select(.username=="maxithy") | .api_key')
test_response "" "$response" "Verify maxithy is no longer in user list"
echo -e "\n"


