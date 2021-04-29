
from fuzzywuzzy import fuzz
    
def search(results, text, field, limit = 20, threshhold = 50):

    matches = []
    for result in results:
        match = fuzz.partial_ratio(text, result[field])
        if match > threshhold:
            matches.append((fuzz.partial_ratio(result, text), result))
    
    matches.sort(key = lambda x : x[0], reverse = True)
    matches = [match[1] for match in matches]

    if limit < len(matches):
        matches = matches[:limit]

    return matches


