
#WORK IN PROGRESS

from typing import TypedDict
from langgraph.graph import  StateGraph


class BlogPostState(TypedDict):
    topic:str
    keywords:list[str]
    title:str
    meta_description:str
    blog_style:str
    content_intent:str
    tone:str
    seo_score:int
    readability_score:int
    keyword_density:float
    word_count:int
    read_time:int
    images_list:list[str]
    slug:str
    internal_links:list[str]
    internal_links_count:int
    external_links:list[str]
    external_links_count:int
    canonical_url:str
    tone:str
    title_score:int
    meta_description_score:int
    outline_score:int
    image_optimization_score:int
    keyword_clustering_score:int
    coherence_score:int
    originality_score:int
    keywords_variance_score:int
    

def researcherNode(state:BlogPostState) -> BlogPostState:
    """
    This Node Takes the Topic and Performs a Web Search.
    Currently it Also Performs a Competing Posts Analysis. (Later it will be moved to a separate node)
    It Will Generate the Title, Meta Description, and Keywords for the Blog Post.
    """




