# Intersect - Personalized job matching

Find the job you actually want using AI.

Access here: https://intersect.streamlit.app

_Intersect_ ([web app](https://intersect.streamlit.app/)) is a job-searching tool that uses NLP to reorder job postings based on semantic similarity rather than traditional keyword searches. Unlike lexical search (BM25), which relies on exact word matches, semantic search uses dense vectors to represent meaning (Boykis, 2023; Mitchell, 2019; Schmidt, 2015), providing more personalized results when used with user-provided text. By providing the user with different information retrieval methods (semantic search, lexical search, reranking), the purpose of _Intersect_ is to enhance job discovery and reduce manual effort.

_Intersect_ uncovers non-obvious job opportunities by enhancing traditional search methods with NLP. The varied outcomes suggest a hybrid approach—combining keyword, semantic, and reranking techniques—could yield optimal results.

It involves

-   Scraping job listings and vectorizing results with OpenAI's `text-embedding-3-small`.
-   Generating word clouds with TF-IDF.
-   Capturing user input and reordering results by computing similarity via dot product.
-   Visualizing clusters using PCA and KMeans.
-   Reordering results using BM25 (lexical search).
-   Reranking with Cohere’s cross-encoder.

## Implementation details:

-   web development
    -   `uv`: environment and dependency management
    -   `streamlit`: web framework (frontend and backend) and hosting
    -   `pypdf`: pdf cv parsing
-   data science
    -   semantic search: OpenAI's `text-embedding-3-small`
    -   lexical search: `bm25s` (Lucene method)
        -   preprocessing (tokenizer, stemmer, stop words)
    -   visualization: PCA+KMeans `scikit-learn` (Might be more appropriate to use other algorithms such as t-SNE, LSA, mean-shift and dbscan)
    -   reranker: Cohere's reranking model

## References

-   Boykis, V. (2023). _What are embeddings?_. Retrieved from https://github.com/veekaybee/what_are_embeddings
-   Mitchell, M. (2019). _Artificial Intelligence: A Guide for Thinking Humans_. Pelican Books.
-   Sanseviero, O. (2024). Sentence Embeddings. Cross-encoders and Re-ranking. hackerllama. Retrieved from https://osanseviero.github.io/hackerllama/blog/posts/sentence_embeddings2/
-   Schmidt, B. (2015). _Vector Space Models for the Digital Humanities_. Bookworm. Retrieved from https://bookworm.benschmidt.org/posts/2015-10-25-Word-Embeddings.html
-   Sun, W., Yan, L., Ma, X., Wang, S., Ren, P., Chen, Z., Yin, D., & Ren, Z. (2024). _Is ChatGPT Good at Search? Investigating Large Language Models as Re-Ranking Agents_ (No. ArXiv: 2304.09542). ArXiv. [https://doi.org/10.48550/arXiv.2304.09542](https://doi.org/10.48550/arXiv.2304.09542)

## TODO

-   new features

-   add LDA for better clustering
-   add DBSCAN (HDBSCAN?) for clustering
-   add t-SNE for visualization
-   am i just recreating bertopic?

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

---

## Job boards

-   With API
    -   https://publicapi.dev/category/jobs
        -   https://api.theirstack.com/#tag/jobs/post/v1/jobs/search
            -   rate 300 per minute
            -   200 credits free, $100/5k credits
        -   https://fantastic.jobs/api
            -   https://rapidapi.com/fantastic-jobs-fantastic-jobs-default/api/active-jobs-db/pricing
            -   https://rapidapi.com/fantastic-jobs-fantastic-jobs-default/api/linkedin-job-search-api/pricing
            -   https://rapidapi.com/fantastic-jobs-fantastic-jobs-default/api/internships-api/pricing
            -   free 250 per month / 25 requests per month
            -   https://rapidapi.com/fantastic-jobs-fantastic-jobs-default/api/free-y-combinator-jobs-api/pricing
                -   free
            -   https://rapidapi.com/fantastic-jobs-fantastic-jobs-default/api/upwork-jobs-api2/pricing
                -   free 500 per month
        - https://rapidapi.com/techmap-io-techmap-io-default/api/daily-international-job-postings/pricing
            - 1000 free p month
        -   https://publicapi.dev/jobdata-api
            - However, please note that there's an hourly rate limit with a handful of requests without a valid API key
        -   https://www.reed.co.uk/developers/Jobseeker
            -   no terms
        -   https://publicapi.dev/adzuna-api
            -   https://developer.adzuna.com/docs/terms_of_service
                -   25 hits per minute 250 day, 1000 week, 2500 month
                -   display logo

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

Other sources: https://theirstack.com/en/docs/data/job/sources#job-data-sources
