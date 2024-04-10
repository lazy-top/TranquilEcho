import arxiv



def arxiv_search(query:str):
    search = arxiv.Search(
    query = query,
    max_results = 10,
    sort_by = arxiv.SortCriterion.SubmittedDate
    )
    for result in search.results():
        print(result.entry_id, '->', result.title)
        
        
arxiv_search("heart disease")