import json
import requests
from bs4 import BeautifulSoup


def main():
	"""Main Program Loop"""
	allstar_index = {}

	# Load Existing JSON file (JSON File Structure {Level_ID: {name: levelname, leaderboard: dustkid_link}}
	with open('map_index.json', 'r') as f:
		level_id_list = json.load(f)

	# Start Request Loop
	for level_id in level_id_list:
		allstar_ss, allstar_any, one_off_ss, one_off_any = grab_all_star(level_id, level_id_list)

		# Sets Base Dictionary Values
		level_name = level_id_list[level_id]['name']
		level_leaderboard = level_id_list[level_id]['leaderboard']
		id_level = level_id

		level_allstar = create_level_dict(level_name, level_leaderboard, id_level, allstar_ss, allstar_any,
										  one_off_ss, one_off_any)
		allstar_index.update(level_allstar)

	# Create JSON File
	with open('allstar_index.json', 'w') as f:
		json.dump(allstar_index, f, indent=3)


def grab_all_star(level_id, level_id_list):
	# Makes request to dustkid leaderboard page
	print(f'Grabbing data from: {level_id_list[level_id]["leaderboard"]}')
	level_page = requests.get(level_id_list[level_id]['leaderboard'])

	# Grabs Full HTML of page
	soup = BeautifulSoup(level_page.content, "html.parser")

	# Finds leaderboard attributes
	leaderboard = soup.findAll('table', {'class': 'leaderboard'})

	# Grab SS leaderboard and check for allstar
	character_ranking_html_ss = leaderboard[0].find_all('img', {'class': 'character'}, limit=4)

	# Grab Any% leaderboard and check for allstar
	character_ranking_html_any = leaderboard[1].find_all('img', {'class': 'character'}, limit=4)

	# Checks for any All stars
	all_star_ss, one_off_ss = check_top4(character_ranking_html_ss)
	all_star_any, one_off_any = check_top4(character_ranking_html_any)

	return all_star_ss, all_star_any, one_off_ss, one_off_any


def check_top4(top4_html):
	"""Checks if all 4 characters appear in html and returns True or False"""
	top4 = []
	for rank_html in top4_html:
		if 'Dustman' in str(rank_html):
			top4.append('Dustman')

		if 'Dustgirl' in str(rank_html):
			top4.append('Dustgirl')

		if 'Dustkid' in str(rank_html):
			top4.append('Dustkid')

		if 'Dustworth' in str(rank_html):
			top4.append('Dustworth')

	if 'Dustman' in top4 and 'Dustgirl' in top4 and 'Dustkid' in top4 and 'Dustworth' in top4:
		return True, False

	else:  # Checks if 3/4 are in top 4 and returns True for one_off
		if 'Dustman' in top4 and 'Dustgirl' in top4 and 'Dustkid' in top4:
			return False, True
		if 'Dustman' in top4 and 'Dustgirl' in top4 and 'Dustworth' in top4:
			return False, True
		if 'Dustman' in top4 and 'Dustkid' in top4 and 'Dustworth' in top4:
			return False, True
		if 'Dustgirl' in top4 and 'Dustkid' in top4 and 'Dustworth' in top4:
			return False, True
		else:
			return False, False


def create_level_dict(level_name, level_leaderboard, level_id, allstar_ss, allstar_any, one_off_ss, one_off_any):
	"""Creates the level dictionary with allstar data and basic level information"""

	# Base Dictionary
	level_allstar = {level_id: {'levelname': level_name, 'leaderboard': level_leaderboard, 'allstar_ss': None,
								  'allstar_any': None, 'one_off_ss': None, 'one_off_any': None}}
	# Add SS to Dictionary
	if allstar_ss:
		level_allstar[level_id]['allstar_ss'] = True

	if not allstar_ss:
		level_allstar[level_id]['allstar_ss'] = False

	if one_off_ss:
		level_allstar[level_id]['one_off_ss'] = True

	if not one_off_ss:
		level_allstar[level_id]['one_off_ss'] = False

	# Add Any% to Dictionary
	if allstar_any:
		level_allstar[level_id]['allstar_any'] = True

	if not allstar_any:
		level_allstar[level_id]['allstar_any'] = False

	if one_off_any:
		level_allstar[level_id]['one_off_any'] = True

	if not one_off_any:
		level_allstar[level_id]['one_off_any'] = False

	return level_allstar


if __name__ == '__main__':
	main()
