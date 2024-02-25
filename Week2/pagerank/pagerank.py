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
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Generates a probability distribution for the next page to visit from a given page.
    
    With a probability equal to the damping_factor, a linked page is chosen at random.
    With a probability of 1 - damping_factor, any page from the entire corpus is chosen at random.
    """
    # Example corpus structure: {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
    # Example return value: {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}

    # If the current page has outgoing links:
    if corpus[page] != set():
        probabilities = {}
        # Assign a base probability for random jumps to any page in the corpus
        for key in corpus.keys():
            probabilities[key] = (1-damping_factor) / len(corpus)
        # Adjust probabilities for pages directly linked from the current page
        for linked_page in corpus[page]:
            if linked_page in probabilities:
                probabilities[linked_page] += damping_factor / len(corpus[page])
            else:
                probabilities[linked_page] = damping_factor / len(corpus[page])
        return probabilities
    # If the current page has no outgoing links:
    else:
        # Distribute probabilities evenly across all pages
        return {key: 1 / len(corpus) for key in corpus.keys()}

    

def sample_pagerank(corpus, damping_factor, n):
    """
    Estimates PageRank values for each page by randomly sampling `n` pages, following
    the transition model for page selection.

    Returns a dictionary with pages as keys and their estimated PageRank as values.
    PageRank values are normalized to sum up to 1.
    """
    # Ensure that the number of samples `n` is positive
    if n >= 1:
        samples_count = 0 # Counter for the number of samples taken
        page_visits = {} # Dictionary to count visits to each page
        current_page = random.choice(list(corpus.keys())) # Start sampling from a random page
        page_visits[current_page] = 1 # Initialize the first visit

        # Sample `n` times based on the transition model
        while samples_count < n:
            samples_count += 1
            # Get the next page's probabilities from the current page's transition model
            pages = list(transition_model(corpus, current_page, damping_factor).keys())
            weights = list(transition_model(corpus, current_page, damping_factor).values())

            # Choose the next page based on the transition probabilities
            current_page = random.choices(pages, weights=weights, k=1)[0]

            # Update visits count for the chosen page
            if current_page in page_visits.keys():
                page_visits[current_page] += 1
            else:
                page_visits[current_page] = 1

        # Normalize visits to probabilities
        for page in page_visits.keys():
            page_visits[page] /= n

        return page_visits


def iterate_pagerank(corpus, damping_factor):
    """
    Estimates PageRank values for each page by iteratively refining
    PageRank values until they converge.

    Returns a dictionary with page names as keys and their estimated
    PageRank values as values, where the sum of all PageRank values is 1.
    """
    epsilon = 0.001  # Convergence threshold
    page_ranks = {page: 1 / len(corpus) for page in corpus}  # Initial uniform distribution of PageRank

    # Continue updating PageRank values until changes are under the threshold
    while True:
        new_page_ranks = {} # Temporary distribution of PageRank
        max_delta = 0  # Track the maximum change between iterations for any single page

        # Calculate new PageRank for each page
        for page in corpus:
            pr_i = (1 - damping_factor) / len(corpus)  # Base probability for random jump to any page
            link_sum = 0  # Sum of PageRank contributions from pages linking to the current page

            # Aggregate contributions from linking pages
            for linking_page, links in corpus.items():
                if page in links:
                    link_sum += damping_factor * (page_ranks[linking_page] / len(links))
                # Handle pages with no outgoing links by redistributing their rank equally
                elif not links:
                    link_sum += damping_factor * (page_ranks[linking_page] / len(corpus))

            # Compute new PageRank
            new_pr = pr_i + link_sum
            new_page_ranks[page] = new_pr

            # Update max_delta if this page's change is the largest so far
            max_delta = max(max_delta, abs(new_pr - page_ranks[page]))

        # Update PageRank values to those calculated in this iteration
        page_ranks = new_page_ranks

        # Break the loop if the maximum change in PageRank values is below the threshold
        if max_delta < epsilon:
            break

    return page_ranks



if __name__ == "__main__":
    main()
