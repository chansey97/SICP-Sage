import re
from orgparse import load, loads

data_path = '/mnt/data/'
# data_path = './'

# SICP_BOOK_ROOT = load('sicp-book.org')
# SICP_BOOK_ROOT = load('/mnt/data/sicp-book.org')
SICP_BOOK_ROOT = load(data_path + 'sicp-book.org')

INDEX = SICP_BOOK_ROOT.children[11]
CHAPTER_1 = SICP_BOOK_ROOT.children[5]
CHAPTER_2 = SICP_BOOK_ROOT.children[6]
CHAPTER_3 = SICP_BOOK_ROOT.children[7]
CHAPTER_4 = SICP_BOOK_ROOT.children[8]
CHAPTER_5 = SICP_BOOK_ROOT.children[9]

def find_exercise(exercise_number):
    result = {'heading': '', 'properties': '', 'body': ''}
    for node in SICP_BOOK_ROOT:
        if "Exercise " + exercise_number in node.heading:
            result = {'heading': node.heading, 'properties': node.properties, 'body': node.body}
            break
    return result

def find_concept_contexts(keyword):

    concept_contexts = find_concept_contexts_via_index(keyword)
    if concept_contexts:
        return concept_contexts
    else:
        return find_concept_contexts_via_full_text(keyword)

def find_concept_contexts_via_index(keyword):

    def find_ref_kw_s_in_index(keyword):
        items = str(INDEX).splitlines()[2:]
        pattern = r'- \[\[(i.+)\]\[(.*' + re.escape(keyword) + r'.*)\]\]'
        matches = re.findall(pattern, '\n'.join(items), re.IGNORECASE)
        return matches

    ref_kw_s = find_ref_kw_s_in_index(keyword)
    if ref_kw_s:
        contexts = []
        for ref, kw in ref_kw_s:
            for node in SICP_BOOK_ROOT:
                ctxs = extract_contexts("<<" + ref + ">>", node)
                for ctx in ctxs:
                    ctx["ref"] = ref
                    ctx["keyword"] = kw
                contexts += ctxs
        return contexts
    else:
        return find_concept_contexts_via_full_text(keyword)

def find_concept_contexts_via_full_text(keyword):
    concept_contexts = []
    for node in CHAPTER_1:
        concept_contexts.extend(extract_contexts(keyword, node))
    for node in CHAPTER_2:
        concept_contexts.extend(extract_contexts(keyword, node))
    for node in CHAPTER_3:
        concept_contexts.extend(extract_contexts(keyword, node))
    for node in CHAPTER_4:
        concept_contexts.extend(extract_contexts(keyword, node))
    for node in CHAPTER_5:
        concept_contexts.extend(extract_contexts(keyword, node))
    return concept_contexts

def extract_contexts(keyword, node, context_range=500, jump_range=250):

    def calc_location(node):
        headings = []
        while node.parent != None:
            headings.append(node.heading)
            node = node.parent
        headings.reverse()
        return '\n'.join(["- " + heading for heading in headings])

    text = node.body
    contexts = []
    position = 0
    location = calc_location(node)
    while position < len(text):
        found_position = text.find(keyword, position)
        if found_position != -1:
            start = max(0, found_position - context_range)
            end = min(len(text), found_position + len(keyword) + context_range)
            context = {'keyword':keyword, 'content':text[start:end], 'location':location}
            contexts.append(context)
            position = found_position + len(keyword) + jump_range
        else:
            break
    return contexts

# exercise_number = "3.78"
# exercise = find_exercise(exercise_number)
# print(exercise)

# concept = "stream"
# concept = "abstraction barriers"
# concept = "monad"
# concept = "object"
# concept_contexts = find_concept_contexts(concept)
# print(concept_contexts)


