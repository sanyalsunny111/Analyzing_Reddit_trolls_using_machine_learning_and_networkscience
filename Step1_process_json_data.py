import bz2
import json
import pandas as pd 
import sys
import lzma



subreddits_dict = dict('politics',[]) 

# In this finction, we filter and extract the required features we use for further downstream processing. 
# We use a dictionary to be able to add support for other subreddits like The_Donald if needed.

def process_zip_file(file_location):

	df_troll = pd.read_csv('lib/troll_user_labels.csv')
	df_troll.columns = ['id','unn']
	troll_list = df_troll['id'].values.tolist()
	if file_location[-3:] == 'bz2':
		with bz2.BZ2File(file_location, 'rb') as file:
			write_to_csv_buffer = []
			
			for line in file:
				loaded_line = json.loads(line)
				subreddit = loaded_line['subreddit']
				if subreddit == 'politics' and loaded_line['author'] != '[deleted]'  and loaded_line['author'] != '[removed]'and loaded_line['body'] != '[deleted]'  and loaded_line['body'] != '[removed]':
					
					user_id = loaded_line['author']
					parent_id = loaded_line['parent_id']
					timestamp = loaded_line['created_utc']
					content = loaded_line['body']
					
					score = loaded_line['score']
					link_id = loaded_line['link_id']
					
					gilded = loaded_line['gilded']
					
					if 'num_comments' in loaded_line:
						num_comments = loaded_line['num_comments']
					else:
						num_comments = 0
					
					if 'over_18' in loaded_line:
						over_18 = loaded_line['over_18']
					else:
						over_18 = 'False'
					
					if 'downs' in loaded_line:
						downs = loaded_line['downs']
					
					else:
						downs = 0
					
					
					if 'quarantine' in loaded_line:
						quarantine = loaded_line['quarantine']
					else:
						quarantine = 'False'
					if 'ups' in loaded_line:
						ups = loaded_line['ups']
					else:
						ups = 0
				    # Boolean variable to indicate existence in 944 Russian troll list provided by reddit
					russian = int(loaded_line['author'] in troll_list)	
					subreddits_dict[subreddit].append((subreddit, user_id, parent_id, timestamp, content,  score, link_id,gilded, num_comments, over_18, downs,    quarantine, ups, russian ))
			
	elif file_location[-2:] == 'xz':
		with lzma.open(file_location) as file:
			write_to_csv_buffer = []
			counter = 0
			for line in file:
				loaded_line = json.loads(line)
				subreddit = loaded_line['subreddit']
				if subreddit == 'politics' and loaded_line['author'] != '[deleted]'  and loaded_line['author'] != '[removed]'and loaded_line['body'] != '[deleted]'  and loaded_line['body'] != '[removed]':
					
					user_id = loaded_line['author']
					parent_id = loaded_line['parent_id']
					timestamp = loaded_line['created_utc']
					content = loaded_line['body']
					
					score = loaded_line['score']
					link_id = loaded_line['link_id']
					]
					gilded = loaded_line['gilded']
					
					if 'num_comments' in loaded_line:
						num_comments = loaded_line['num_comments']
					else:
						num_comments = 0
					
					if 'over_18' in loaded_line:
						over_18 = loaded_line['over_18']
					else:
						over_18 = 'False'
					
					if 'downs' in loaded_line:
						downs = loaded_line['downs']
					
					else:
						downs = 0
					
					
					if 'quarantine' in loaded_line:
						quarantine = loaded_line['quarantine']
					else:
						quarantine = 'False'
					if 'ups' in loaded_line:
						ups = loaded_line['ups']
					else:
						ups = 0
					# Boolean variable to indicate existence in 944 Russian troll list provided by reddit
					russian = int(loaded_line['author'] in troll_list)
					subreddits_dict[subreddit].append((subreddit, user_id, parent_id, timestamp, content, score, link_id,  gilded,  num_comments, over_18, downs,    quarantine, ups, russian ))
			

column_names = ['subreddit', 'author', 'parent_id', 'created_utc', 'body', 'score', 'link_id', 'gilded' , 'num_comments', 'over_18', 'downs',   'quarantine', 'ups', 'russsian']
process_zip_file('RC_2016-09.bz2')
csv_file_name = 'politicsnormies.csv'
table_pol = subreddits_dict['politics']
df = pd.DataFrame(table_pol, columns = column_names)
print(df.head(5))
df.to_csv('politicsnormies.csv')


