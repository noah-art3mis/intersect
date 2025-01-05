# Intersect - Personalized job matching

Find the job you actually want - using AI.

Finds jobs based on vibes instead of specific parameters. Uses a similarity search workflow with embedding models to compare your CV with jobs descriptions. Reorders listings based on similarity with the input text. This is not supposed to substitute manual search, but to make it easier by ordering the results by relevance. This can also be combined with more traditional NLP techniques such as TF-IDF.

Uses `uv`, `streamlit`, `openai`.

Assignment for the Right Word module at LIS.

## TODO

- [ ] add frontend (streamlit)
- [ ] add support for local and open source embedding models. see [MTEB](https://huggingface.co/spaces/mteb/leaderboard). use something like `ollama`
- [ ] add alternatives for search such as BM25
- [ ] add reranking
- [ ] add other features to make selection easier (sponsoring, etc)
- [ ] add reverse mode (employers ordering applicants by relevance)
- [ ] try using LLMs for this and compare the result
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
- [ ] add support for different platforms
    - General
        - [ ] CV-Library 
        - [ ] Indeed
        - [ ] Indeed UK
        - [ ] Reed
        - [ ] Totaljobs
        - [ ] LinkedIn
        - [ ] Jobserve
        - [ ] [r/forhire](https://www.reddit.com/r/forhire/)
        - [ ] https://www.jobsite.co.uk/
        - [ ] https://www.lhh.com/uk/en/
        - [ ] https://www.prospects.ac.uk/
        - [ ] Glassdoor
        - [ ] Monster
        - [ ] Adzuna
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

Also some info regarding some of these:
- https://www.techradar.com/best/uk-job-sites
- https://seemehired.com/blog/the-top-uk-job-boards-and-hiring-platforms-to-find-talent-in-2024/
