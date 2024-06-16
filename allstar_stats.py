import json


def main(allstar_stats):
	(ss_stat, any_stat, level_stat, one_off_ss_stat, one_off_any_stat, one_off_level_stat, total_leaderboard_stat,
	 total_one_off_leaderboard_stat, total_leaderboards, total_levels) = count_stats(allstar_stats)

	# Print Basic Stats
	print(f'{ss_stat} SS leaderboards have been allstared'
		  f'\n{any_stat} any% leaderboards have been allstared'
		  f'\n{total_leaderboard_stat} leaderboards out of {total_leaderboards} total leaderboards have been allstared'
		  f'\n{level_stat} levels have been out of {total_levels} levels have been fully allstared'
		  f'\n{one_off_ss_stat} SS leaderboards are one off allstar'
		  f'\n{one_off_any_stat} any% leaderboards are one off allstar'
		  f'\n{total_one_off_leaderboard_stat} leaderboards out of {total_leaderboards} total leaderboards are one '
		  f'off of being allstared'
		  f'\n\n!! We are about {round((level_stat/total_levels) * 100, 2)}% to allstaring all levels on dustkid !!')

	one_off_levels = generate_one_off_list(allstar_stats)

	with open('one_off_levels.json', 'w') as file:
		json.dump(one_off_levels, file, indent=3)



def count_stats(allstar_stats):
	# Base Variables
	ss_stat = 0
	any_stat = 0
	level_stat = 0
	one_off_ss_stat = 0
	one_off_any_stat = 0
	one_off_level_stat = 0
	total_leaderboards = len(allstar_stats.keys()) * 2
	total_levels = len(allstar_stats.keys())

	# Loop over keys to find stats
	for level_id in allstar_stats.keys():
		# Full allstar leaderboards
		if allstar_stats[level_id]['allstar_ss']:
			ss_stat += 1
		if allstar_stats[level_id]['allstar_any']:
			any_stat += 1
		if allstar_stats[level_id]['allstar_ss'] and allstar_stats[level_id]['allstar_any']:
			level_stat += 1
		# One off allstar leaderboards
		if allstar_stats[level_id]['one_off_ss']:
			one_off_ss_stat += 1
		if allstar_stats[level_id]['one_off_any']:
			one_off_any_stat += 1
		if allstar_stats[level_id]['one_off_ss'] and allstar_stats[level_id]['one_off_any']:
			one_off_level_stat += 1

	total_leaderboard_stat = ss_stat + any_stat
	total_one_off_leaderboard_stat = one_off_ss_stat + one_off_any_stat

	return (ss_stat, any_stat, level_stat, one_off_ss_stat, one_off_any_stat, one_off_level_stat,
			total_leaderboard_stat, total_one_off_leaderboard_stat, total_leaderboards, total_levels)


def generate_one_off_list(allstar_stats):
	one_off_levels = {}
	for level_id in allstar_stats.keys():
		if allstar_stats[level_id]['one_off_ss'] or allstar_stats[level_id]['one_off_any']:
			one_off_levels[allstar_stats[level_id]['levelname']] = allstar_stats[level_id]['leaderboard']

	return one_off_levels


if __name__ == '__main__':
	with open('allstar_index.json', 'r') as f:
		json_data = json.load(f)

	main(json_data)
