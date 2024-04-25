"""
Test the parsers are still working (HTML has not changed) with a demo list and a demo
watched movies. Only retrieve the first page for each.
"""

import utils

user_id = '861134'

print('Checking user ID ...')
utils.check_user(user_id)

print('Retrieving user lists ...')
lists = utils.get_user_lists(user_id, max_page=1)

print('Retrieving list movies ...')
_ = utils.get_list_movies(list(lists.values())[0], max_page=1)

print('Retrieving watched movies ...')
_ = utils.get_watched_movies(user_id, max_page=1)

print('Tests successfully passed!')
