#!/bin/bash

# Reed API Job Details Test
# This script demonstrates how to use curl to test the Reed.co.uk API job details endpoint

# Set your API key here (replace with your actual API key)
API_KEY="your_reed_api_key_here"

# Example job ID (you can replace this with any valid job ID)
JOB_ID="12345678"

echo "🔍 Testing Reed API Job Details Endpoint"
echo "========================================"
echo "API Key: ${API_KEY:0:8}..."  # Show first 8 chars for security
echo "Job ID: $JOB_ID"
echo ""

# Test 1: Basic job details request
echo "📋 Test 1: Fetching job details for job ID $JOB_ID"
echo "curl -u \"$API_KEY:\" \"https://www.reed.co.uk/api/1.0/jobs/$JOB_ID\""
echo ""

# Execute the curl command
curl -u "$API_KEY:" "https://www.reed.co.uk/api/1.0/jobs/$JOB_ID" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -w "\n\nHTTP Status: %{http_code}\nResponse Time: %{time_total}s\n" \
  -s

echo ""
echo "========================================"
echo ""

# Test 2: Pretty-printed JSON response
echo "📋 Test 2: Pretty-printed JSON response"
curl -u "$API_KEY:" "https://www.reed.co.uk/api/1.0/jobs/$JOB_ID" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -s | python3 -m json.tool

echo ""
echo "========================================"
echo ""

# Test 3: Extract specific fields using jq (if available)
if command -v jq &> /dev/null; then
    echo "📋 Test 3: Extract specific fields using jq"
    curl -u "$API_KEY:" "https://www.reed.co.uk/api/1.0/jobs/$JOB_ID" \
      -H "Accept: application/json" \
      -H "Content-Type: application/json" \
      -s | jq '{jobId, jobTitle, employerName, locationName, minimumSalary, maximumSalary, currency}'
else
    echo "📋 Test 3: jq not available, skipping field extraction"
fi

echo ""
echo "========================================"
echo ""

# Instructions for using different job IDs
echo "💡 To test with different job IDs:"
echo "1. Replace the JOB_ID variable in this script"
echo "2. Or run: curl -u \"YOUR_API_KEY:\" \"https://www.reed.co.uk/api/1.0/jobs/JOB_ID_HERE\""
echo ""
echo "💡 To get job IDs, first search for jobs:"
echo "curl -u \"YOUR_API_KEY:\" \"https://www.reed.co.uk/api/1.0/search?keywords=python&locationName=london&resultsToTake=5\"" 