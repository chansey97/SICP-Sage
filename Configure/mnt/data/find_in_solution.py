from orgparse import load

data_path = '/mnt/data/'
# data_path = './'

# SICP_SOLUTION_ROOT = load('sicp-solution.org')
# SICP_SOLUTION_ROOT = load('/mnt/data/sicp-solution.org')
SICP_SOLUTION_ROOT = load(data_path + 'sicp-solution.org')

def find_solution(exercise_number):
    result = {'heading': '', 'properties': '', 'body': ''}
    for node in SICP_SOLUTION_ROOT:
        if "Exercise " + exercise_number in node.heading:
            result = {'name': node.heading, 'properties':node.properties, 'body': node.body}
            break
    return result

# exercise_number = "1.2"
# solution = find_solution(exercise_number)
# print(solution)
