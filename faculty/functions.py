from . import models
import json
from django.db.models import Count, F
from difflib import SequenceMatcher
from django.db.models import Count

def calc_h_index(citation_counts: list):
    h_index = 0
    for i, count in enumerate(citation_counts):
        if count >= i + 1:
            h_index = i + 1
        else:
            break
    return h_index

def update_h_index(publication_ids: list):
    all_authors = set()  # Use a set to avoid duplicates

    # for id in publication_ids:
    #     publication = Publication.objects.get(id=id)
    #     all_authors.update(publication.authors.values_list('fid', flat=True))

    # Using prefetch_related to minimize DB hits when fetching authors and their publications
    publications = models.Publication.objects.filter(id__in = publication_ids).prefetch_related('authors')

    for publication in publications:
        all_authors.update(publication.authors.values_list('fid', flat = True))

    for author_id in all_authors:
        # Get all publications by this author
        author_publications = models.Publication.objects.filter(authors__fid = author_id)

        # Count the number of citations for each publication
        pubs_citations = models.Citation.objects.filter(publication__in = author_publications).values('publication').annotate(citation_count = Count('publication'))

        # Sort citation counts in descending order
        citation_counts = sorted([citation['citation_count'] for citation in pubs_citations], reverse = True)
        print(citation_counts)

        #update author's h_index
        h_index = calc_h_index(citation_counts)

        print(author_id, h_index)

        models.Faculty.objects.filter(fid = author_id).update(h_index = h_index)

def txt_to_json(inp_txt:str,split_by:str):
    inp_list = inp_txt.split(split_by)
    inp_list = [i.strip() for i in inp_list if i]

    return json.dumps(inp_list)

def get_author_objs_list(authors):
    if type(authors) == list:
        authors_list = authors
    elif type(authors) == str:
        authors_list = authors.split(',')
        authors_list = [author.strip() for author in authors_list]

    author_objs_list = [models.Faculty.objects.get(fid = author[2]) for author in authors_list]

    return author_objs_list

def add_citation(citations:list, cited_by_id:int):
    cited_by = models.Publication.objects.get(id = cited_by_id)

    for publication_id in citations:
        try:
            publication = models.Publication.objects.get(id=publication_id)

            if not models.Citation.objects.filter(cited_by = cited_by, publication = publication).exists():
                models.Citation.objects.create(cited_by = cited_by, publication = publication)

            # update citation count of the author(s) of cited publicaton
            for author in publication.authors.all():
                models.Faculty.objects.filter(fid = author.fid).update(citation_count = F('citation_count') + 1)

        except models.Publication.DoesNotExist:
            print(f"Publication with id {publication_id} does not exist.")

def check_redundancy(title, abstract, authors:list, keywords):
    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()

    articles = models.Article.objects.all()
    for article in articles:
        title_similarity = similar(article.title, title)
        desc_similarity = similar(article.abstract, abstract)

        # Check if the title and abstract have high similarity
        if title_similarity > 0.9 or desc_similarity > 0.9:
            return True
        if title_similarity > 0.8 or desc_similarity > 0.8:
            if article.authors.all() == authors and article.keywords == keywords:
                return True

    return False
