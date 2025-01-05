# Intersect - Personalized job matching

Find the job you actually want - using AI.

Finds jobs based on vibes instead of specific parameters. Uses a similarity search workflow with embedding models to compare your CV with jobs descriptions. Reorders listings based on similarity with the input text, not unlike a [recommendation](https://cookbook.openai.com/examples/recommendation_using_embeddings) algorithm. This is not supposed to substitute manual search, but to make it easier by ordering the results by relevance. This can also be combined with more traditional NLP techniques such as TF-IDF.

Tech stack:

- `uv`: environment and dependency management
- `streamlit`: UI frontend
- `openai`: embedding model
- `pandas`: storing data

Assignment for the Right Word module at LIS.

## Explanations

- OpenAI and Streamlit are the fastest ways to make a prototype.
- There is no need to use the bigger embedding model for this use case.
- There is no need to use SQL yet.
- For a small job like this there is no need for a vector database. 
- For similarity we can use a dot product because OpenAI embeddings are normalized.
- _CV-Library_ is cited by the [UK Government](https://nationalcareers.service.gov.uk/careers-advice/advertised-job-vacancies).
    - https://www.cv-library.co.uk/ai-jobs-in-london?perpage=100&us=1
    - https://www.cv-library.co.uk/job/222849530/AI-Engineer
- Respects robots.txt
- Scraping
    - parsing
        - httpx + selectolax
        - requests + beautiful soup
    - proxy
        - https://techblog.willshouse.com/2012/01/03/most-common-user-agents/
        - https://geonode.com/free-proxy-list
        - https://console.apify.com/sign-up

## TODO

- core
    - [ ] get 10 jobs
    - [ ] add backend
    - [ ] add frontend (streamlit)
    - [ ] add evals (manual x embedding x llm x bm25)
    - [ ] decide name
        - [ ] Navigator
        - [ ] Alignment
        - [ ] Path
        - [ ] Axis
        - [ ] Compass
        - [ ] Trajectory
        - [ ] Shortcut
        - [ ] Intersect
        - [ ] Pathway
        - [ ] Waypoint
- expand
    - [ ] add support for local and open source embedding models. see [MTEB](https://huggingface.co/spaces/mteb/leaderboard). use something like `ollama`
    - [ ] add alternatives for search such as BM25
    - [ ] add caching
    - [ ] add reranking
    - [ ] add clustering viz
    - [ ] add logging
    - [ ] upgrade database to sqlite
    - [ ] add other features to make selection easier (sponsoring, etc)
    - [ ] add reverse mode (employers ordering applicants by relevance)
    - [ ] try using LLMs for this and compare the result
    - [ ] add NLP things (named entity recognition, topic modelling)
    - [ ] add cost tracking
    - [ ] add tracking the bluesky firehose for ai jobs
    - [ ] add support for different platforms
        - Some info on this [here](https://www.techradar.com/best/uk-job-sites) and [here](https://seemehired.com/blog/the-top-uk-job-boards-and-hiring-platforms-to-find-talent-in-2024/)
        - General
            - [ ] CV-Library 
            - [ ] Indeed
            - [ ] Indeed UK
            - [ ] Adzuna
            - [ ] Reed
            - [ ] Monster
            - [ ] Totaljobs
            - [ ] LinkedIn
            - [ ] Jobserve
            - [ ] [r/forhire](https://www.reddit.com/r/forhire/)
            - [ ] https://www.jobsite.co.uk/
            - [ ] https://www.lhh.com/uk/en/
            - [ ] https://www.prospects.ac.uk/
            - [ ] Glassdoor
            - [ ] CWJobs
            - [ ] Guardian Jobs
            - [ ] https://uk.whatjobs.com/
        - Tech
            - [ ] Technojobs
            - [ ] Jobserve
            - [ ] Hackernews
            - [ ] https://wellfound.com/jobs
            - [ ] https://weworkremotely.com/
            - [ ] https://workinstartups.com/
            - [ ] https://www.haystackapp.io/
            - [ ] https://wearetechwomen.com/
            - [ ] https://jobs.revoco-talent.co.uk/jobs.aspx
            - [ ] https://devitjobs.uk/
            - [ ] https://www.cwjobs.co.uk/
            - [ ] https://www.f6s.com/jobs
            - [ ] [Jora](https://uk.jora.com/)
            - [ ] https://remotejobs.careers/job-location/uk/
        - Responsible Tech
            - [ ] [All Tech Is Human](https://alltechishuman.org/responsible-tech-job-board)
            - [ ] [Ethical Tech Job Resources](https://docs.google.com/spreadsheets/d/1dFVoF6f9VU5pjaGhyyvQaBN0n6ae-iLCtlvsO1N2jhA/edit?gid=0#gid=0) 
            - [ ] https://techjobsforgood.com/
            - [ ] [80000h](https://jobs.80000hours.org/)



https://www.cv-library.co.uk/job/222767113/AI-Engineer?hlkw=ai&sid=e07b67b9-2018-4cf6-9959-d52f659097a5
https://www.cv-library.co.uk/job/222743898/Senior-Data-Scientist?hlkw=ai&sid=e07b67b9-2018-4cf6-9959-d52f659097a5
https://www.cv-library.co.uk/job/222843844/Azure-Data-Engineer?hlkw=ai&sid=a0ef12f2-8c51-411c-9952-bc5e834664bc
https://www.cv-library.co.uk/job/222802242/Scrum-Master-GSK0JP00104316?hlkw=ai&sid=a0ef12f2-8c51-411c-9952-bc5e834664bc
https://www.cv-library.co.uk/job/222777460/E-commerce-Solutions-Architect?hlkw=ai&sid=a0ef12f2-8c51-411c-9952-bc5e834664bc
https://www.cv-library.co.uk/job/222785821/Cyber-Security-Engineer?hlkw=ai&sid=a0ef12f2-8c51-411c-9952-bc5e834664bc
https://www.cv-library.co.uk/job/222753572/Full-Stack-Developer?hlkw=ai&sid=a0ef12f2-8c51-411c-9952-bc5e834664bc
https://www.cv-library.co.uk/job/222777451/Data-Scientist?hlkw=ai&sid=a0ef12f2-8c51-411c-9952-bc5e834664bc
https://www.cv-library.co.uk/job/222851557/Domestic-Assistant-Housekeeper
https://www.cv-library.co.uk/job/222851525/Food-Production-Operative-Sauce-packer
https://www.cv-library.co.uk/job/222851732/Funeral-Service-Crew
https://www.cv-library.co.uk/job/218719682/Property-Sales-Consultants-High-Income
https://www.cv-library.co.uk/job/222850521/Aircraft-fitter-Sheet-metal-worker
https://www.cv-library.co.uk/job/222756859/Orthopaedic-Nurse
https://www.cv-library.co.uk/job/222851375/Senior-Flutter-Developer-Outside-IR35-Fully-Remote
https://www.cv-library.co.uk/job/222851502/Business-Travel-Consultant
https://www.cv-library.co.uk/job/222851550/Recruitment-Consultant
