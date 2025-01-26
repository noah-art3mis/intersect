# Intersect - Personalized job matching

Find the job you actually want - using AI.

Access here: https://intersect.streamlit.app

Possible alternative product names: axis, compass, pathway, waypoint

Assignment for the Right Word module at LIS.

1. extract
2. transform
3. generate descriptions
4. generate embeddings

## Tech stack:

-   `uv`: environment and dependency management
-   `streamlit`: web framework (frontend and backend) and hosting
-   `openai` and `cohere`: embedding and rerank models
-   `proxyscrape` and `curl_cffi`: scraping
-   `pypdf`: pdf parsing
-   `scikit-learn`: PCA, KMeans
-   `bm25s`: fast BM25 implementation

## findings

-   fun pca
-   bm25 looks similar to the semantic displacement and not that much to the semantic search
-   either very different from the original one

## TODO

-   new features

    -   [ ] prompt engineering for the permutation
    -   [ ] turn tables into cards
    -   [ ] add sponsor column by comparing to the ukvi excel spreadsheet
    -   [ ] infer keyword and location from the text

    -   [ ] expand database to work in real time. hook up the scraping to the app
    -   find the last page automatically

        <p class="search-header__results">
        Displaying <b>1-100</b> of 562 jobs
        </p>

    -   [ ] add async to openai embedding
    -   [ ] add download button
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
    -   [ ] limit reranker to 1000
    -   [ ] why is drop duplicates not working
    -   [ ] why is ner so slow
    -   [ ] scraping:incremental saving so long tasks are not lost
    -   [ ] careful about limits in reranker

## Job boards

Some info on this [here](https://www.techradar.com/best/uk-job-sites) and [here](https://seemehired.com/blog/the-top-uk-job-boards-and-hiring-platforms-to-find-talent-in-2024/). Each one of these would need a bespoke scraping strategy.

-   General
    -   [x] CV-Library
    -   [ ] Indeed
    -   [ ] Indeed UK
    -   [ ] Adzuna
    -   [ ] Reed
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
