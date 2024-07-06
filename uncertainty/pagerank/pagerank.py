from random import choice, choices

import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Set the distribution to (1 - damping_factor) / corpus size.
    distribution = dict()
    corpus_size = len(corpus)
    random_page = 1 - damping_factor
    for pg in corpus:
        distribution[pg] = random_page / corpus_size

    # Get the links branching off of the given page.
    links = corpus[page]

    # Add to the distribution (damping_factor / links size) for each link.
    link_weight = damping_factor / len(links)
    for link in links:
        distribution[link] += link_weight

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize the counter for where the page surfer ends up.
    surfer_tally = dict()
    for page in corpus:
        surfer_tally[page] = 0

    # Pick a random page to begin surfing from.
    sample = choice([k for k in corpus])
    for _ in range(n):
        distribution = transition_model(corpus, sample, damping_factor)
        # Pick one page to surf to, bearing in mind the probability of going there.
        values, probabilities = list(), list()
        for page in distribution:
            values.append(page)
            probabilities.append(distribution[page])
        sample = choices(values, weights=probabilities, k=1)[0]
        surfer_tally[sample] += 1

    # Adjust for the sample size.
    for page in surfer_tally:
        surfer_tally[page] /= n
    return surfer_tally


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    all_links = set()
    for links in corpus.values():
        for link in links:
            all_links.add(link)

    # Determine all the pages which link to a given page.
    inbound_sources = dict()
    for page in corpus:
        outgoing_links = corpus[page]
        # When a page has no outgoing links, we treat it as being linked to everything.
        if outgoing_links == []:
            # TODO remove this print()
            print("Wahoo I have been triggered and look, no links")
            outgoing_links = all_links
        for link in outgoing_links:
            try:
                inbound_sources[link].append(page)
            except KeyError:
                inbound_sources[link] = [page]

    # Setup PageRank to be all equal in the beginning.
    corpus_size = len(corpus)
    base = 1 - damping_factor
    pagerank = {page: base / corpus_size for page in corpus}
    deviation = 1

    while deviation > 0.001:
        deviation = 0
        new_pagerank = dict()
        for page in pagerank:
            summation = 0
            for source in inbound_sources[page]:
                innard = pagerank[source] / len(corpus[source])
                summation += innard
            modded = damping_factor * summation
            new_pagerank[page] = base + modded
            page_deviation = abs(pagerank[page] - new_pagerank[page])
            if page_deviation > deviation:
                deviation = page_deviation
        pagerank = new_pagerank

    # Bully into becoming 1.
    current_total = sum(pagerank.values())
    for page in pagerank:
        pagerank[page] /= current_total

    return pagerank


if __name__ == "__main__":
    main()
