# Reed API Job Details - Curl Test Commands

## Basic Job Details Request

Replace `YOUR_API_KEY` with your actual Reed API key and `JOB_ID` with a valid job ID:

```bash
curl -u "YOUR_API_KEY:" "https://www.reed.co.uk/api/1.0/jobs/JOB_ID"
```

## Example with a sample job ID:

```bash
curl -u "YOUR_API_KEY:" "https://www.reed.co.uk/api/1.0/jobs/12345678"
```

## Pretty-printed JSON response:

```bash
curl -u "YOUR_API_KEY:" "https://www.reed.co.uk/api/1.0/jobs/12345678" | python3 -m json.tool
```

## With headers for better formatting:

```bash
curl -u "YOUR_API_KEY:" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  "https://www.reed.co.uk/api/1.0/jobs/12345678"
```

## To get job IDs first (search for jobs):

```bash
curl -u "YOUR_API_KEY:" \
  "https://www.reed.co.uk/api/1.0/search?keywords=python&locationName=london&resultsToTake=5"
```

## Notes:

-   The API uses Basic Authentication with your API key as the username and empty password
-   Replace `YOUR_API_KEY` with your actual Reed.co.uk API key
-   Replace `JOB_ID` with a valid job ID (you can get these from the search endpoint)
-   The response will be JSON containing detailed job information
-   If the job doesn't exist, you'll get a 404 status code
