import os
import json
import codecs

# Loads User Input
with open('../User_Input.txt', 'r') as f:
    datafile = f.readline().strip()
    subreddit = f.readline().strip()
    keywords = [word.strip() for word in f.readlines()]

# Loads JSON Object Data
with open(datafile, 'r') as f:
    print('Loading JSON Objects')
    object_list = [json.loads(line) for line in f.readlines()]


# Parsing
# Break up data according to subreddit
def subreddit_filter(subreddit_name, data=object_list):
    subreddit_filtered_array = []
    for item in data:
        if item['subreddit'] == subreddit_name:
            subreddit_filtered_array.append(item)
    return subreddit_filtered_array


# Filtering Comments by Keywords
def keyword_filter(data, keywords=keywords):
    # Builds Dictionary acording to number of keywords
    sorted_comments = {}
    for word in keywords:
        if word not in sorted_comments:
            sorted_comments[word] = []

    # Stores comment data in dictionary
    for item in data:
        author = item['author']
        comment = item['body']
        upvotes = item['ups']
        for keyword in keywords:
            if keyword in comment:
                sorted_comments[keyword].append([author, comment, upvotes])

    return sorted_comments


# Write Output to a file
def write_output(dictionary, sub=subreddit):
    path = sub
    try:
        os.mkdir('../data/' + path)
    except OSError:
        print('Creation of the directory %s failed' % path)
        print('The directory already exists')
    else:
        print ("Successfully created the directory %s " % path)
        for key in dictionary:
            with codecs.open('../data/' + sub + '/' + key + '.txt', 'a', 'utf-8-sig') as f:
                f.write('Keyword: ' + key + '\t\t\tNumber of Comments: ' + str(len(dictionary[key])) + '\n')
                for comment in dictionary[key]:
                    f.write('\nAuthor: ' + comment[0] + '\t\t\tUpvotes: ' + str(comment[2]) + '\n')
                    f.write(comment[1])
                    f.write('\n--End of Comment--\n')
        print('Parsing Complete')

# Main
filtered_data = subreddit_filter(subreddit)
final_comments = keyword_filter(filtered_data)
write_output(final_comments)
