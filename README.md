# Intersect - Personalized job matching

Find the job you actually want - using AI.

Access here: https://intersect.streamlit.app

Assignment for the Right Word module at LIS.

## Tech stack:

-   `uv`: environment and dependency management
-   `streamlit`: web framework (frontend and backend) and hosting
-   `openai` and `cohere`: embedding and rerank models
-   `proxyscrape` and `curl_cffi`: scraping
-   `pypdf`: pdf parsing
-   `scikit-learn`: PCA, KMeans
-   `bm25s`: fast BM25 implementation

## TODO

-   new features

    -   [ ] add llm permutation
        -   [ ] sync old indices with new indices
    -   [ ] turn tables into cards
    -   [ ] add sponsor column by comparing to the ukvi excel spreadsheet
    -   [ ] infer keyword and location from the text
    -   [ ] add scraping in real time (~a few minutes)
        -   [ ] add csv download and upload so you dont have to scrape every time
    -   [ ] find the last page automatically
    -   [ ] add async to openai embedding
    -   [ ] add local
        -   semantic search
        -   reranker
        -   llm permutation
    -   [ ] prepend other cols before embedding
    -   [ ] upgrade database to sqlite
    -   [ ] permutation: test yaml
    -   [ ] add tracking the bluesky firehose for ai jobs
    -   [ ] 'tell me who your friends are' mode where you give other peoples cvs and average the vectors

-   fix
    -   [ ] fix spacing issues
    -   [ ] why is drop duplicates not working
    -   [ ] why is ner so slow
    -   [ ] scraping: incremental saving so long tasks are not lost
    -   [ ] careful about limits in reranker and llm

## Job boards

Some info on this [here](https://www.techradar.com/best/uk-job-sites) and [here](https://seemehired.com/blog/the-top-uk-job-boards-and-hiring-platforms-to-find-talent-in-2024/). Each one of these would need a bespoke scraping strategy.

-   General
    -   [x] CV-Library
    -   [ ] Indeed
    -   [ ] Indeed UK
    -   [ ] Adzuna
    -   [ ] Reed
    -   [ ] Google for jobs
    -   [ ] Monster
    -   [ ] Totaljobs
    -   [ ] LinkedIn
    -   [ ] Jobserve
    -   [ ] [r/forhire](https://www.reddit.com/r/forhire/)
    -   [ ] https://www.jobsite.co.uk/
    -   [ ] https://www.lhh.com/uk/en/
    -   [ ] https://www.prospects.ac.uk/
    -   [ ] Glassdoor
    -   [ ] CWJobs
    -   [ ] Guardian Jobs
    -   [ ] https://uk.whatjobs.com/
-   Tech
    -   [ ] Technojobs
    -   [ ] Jobserve
    -   [ ] Hackernews
    -   [ ] https://wellfound.com/jobs
    -   [ ] https://weworkremotely.com/
    -   [ ] https://workinstartups.com/
    -   [ ] https://www.haystackapp.io/
    -   [ ] https://wearetechwomen.com/
    -   [ ] https://jobs.revoco-talent.co.uk/jobs.aspx
    -   [ ] https://devitjobs.uk/
    -   [ ] https://www.cwjobs.co.uk/
    -   [ ] https://www.f6s.com/jobs
    -   [ ] [Jora](https://uk.jora.com/)
    -   [ ] https://remotejobs.careers/job-location/uk/
-   Responsible Tech
    -   [ ] [All Tech Is Human](https://alltechishuman.org/responsible-tech-job-board)
    -   [ ] [Ethical Tech Job Resources](https://docs.google.com/spreadsheets/d/1dFVoF6f9VU5pjaGhyyvQaBN0n6ae-iLCtlvsO1N2jhA/edit?gid=0#gid=0)
    -   [ ] https://techjobsforgood.com/
    -   [ ] [80000h](https://jobs.80000hours.org/)
