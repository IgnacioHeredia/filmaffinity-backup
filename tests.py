"""
Test the parsers are still working (HTML has not changed) with a demo list and a demo
watched movies. Only retrieve the first page for each.
"""

import utils
import pandas as pd

user_id = '861134'

print('Checking user ID ...')
utils.check_user(user_id)

print('Retrieving user lists ...')
lists = utils.get_user_lists(user_id, max_page=1)

print('Retrieving list movies ...')
name, movies = utils.get_list_movies(list(lists.values())[0], max_page=1)
for v in movies.values():
    assert v, "List movies is empty!"
print(pd.DataFrame(movies).iloc[:5])

print('Retrieving watched movies ...')
movies = utils.get_watched_movies(user_id, max_page=1)
for v in movies.values():
    assert v, "Watched movies is empty!"
print(pd.DataFrame(movies).iloc[:5])

print('✅ Tests successfully passed!')
