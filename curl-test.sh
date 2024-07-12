#!/bin/bash

# This script is used to test the Flask API by creating a timeline post, fetching all posts, and deleting the created post.
# Here is what it does:
# 1. Creates a timeline post with test data.
# 2. Fetches all posts to verify the creation.
# 3. Deletes the created post to clean up.

# Set API URL and test data
API_URL="http://localhost:5000/api/timeline_post"
NAME="TestUser$(date +%s)"
EMAIL="test$(date +%s)@example.com"
CONTENT="This is a test post at $(date)."

# We want to check the status of the response
function check_status {
    local status="$1"
    local expected="$2"
    local action="$3"

    if [ "$status" -ne "$expected" ]; then
        echo "Failed to $action. Expected status $expected, got $status."
        exit 1
    else
        echo "Successfully $action."
    fi
}

# Create a timeline post
echo "Creating a timeline post..."
CREATE_OUTPUT=$(curl --silent --write-out "HTTPSTATUS:%{http_code}" --request POST "$API_URL" -d "name=$NAME&email=$EMAIL&content=$CONTENT")

# Extract body and status from output
CREATE_BODY=$(echo $CREATE_OUTPUT | sed -e 's/HTTPSTATUS\:.*//g')
CREATE_STATUS=$(echo $CREATE_OUTPUT | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')

# Check if post creation was successful
check_status "$CREATE_STATUS" 200 "create post"

# Extract post ID from response
POST_ID=$(echo $CREATE_BODY | grep -o '"id":[0-9]*' | grep -o '[0-9]*')
echo "Created post ID: $POST_ID"

# Fetch posts to verify creation
echo "Fetching posts to verify creation..."
VERIFY_OUTPUT=$(curl --silent --write-out "HTTPSTATUS:%{http_code}" "$API_URL")

# Extract body and status from output
VERIFY_BODY=$(echo $VERIFY_OUTPUT | sed -e 's/HTTPSTATUS\:.*//g')
VERIFY_STATUS=$(echo $VERIFY_OUTPUT | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')

# Check if post was created successfully
check_status "$VERIFY_STATUS" 200 "fetch posts"

# Verify that the post was created
if [ -n "$POST_ID" ]; then
    # Check if the post ID is present in the response
    echo "Deleting post ID: $POST_ID..."
    DELETE_OUTPUT=$(curl --silent --write-out "HTTPSTATUS:%{http_code}" --request DELETE "$API_URL/$POST_ID")
    DELETE_STATUS=$(echo $DELETE_OUTPUT | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')

    # Check if post deletion was successful
    check_status "$DELETE_STATUS" 200 "delete post"
else
    echo "No valid post ID found. Cannot delete."
fi

# Exit with success
echo "Script completed successfully."
