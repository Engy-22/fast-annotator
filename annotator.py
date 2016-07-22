from pycorenlp import StanfordCoreNLP
import pandas as pd
import re
import os
import time

# This uses ttab to automatically open a tab and call a little script that starts the server in said tab.
os.system('cd')
os.system('ttab exec python3 Documents/coreNLP/server.py')

# Sleep gives the server a second to start.
time.sleep(2)
os.system('cd')

# Here you want to type out your different user dictionaries and their labels.

misc = ["Millennium Falcon", "Sandpeople", "Clone Wars", "Sarlacc", "Wookiees", "Star Destroyer", "Star Destroyers", "Star Destroyer Avenger", "Death Star", "Force", "TIE fighter", "Super Star Destroyer", "Falcon", "Falcon", "hyperdrive", "Bothan", "Bothans", "Hyperdrive", "Jedi", "Jedi Knight", "Jedi Master", "Stormtroopers", "stormtroopers", "stormtrooper", "Wookie", "Wookiee", "X-wing", "dark side", "Tauntaun", "Tauntauns", "Hyperspace", "hyperspace"]
org = ["Rebellion", "Academy", "Old Republic", "Rebel fleet", "Imperial Senate", "Alliance", "Rebel Alliance", "Imperial", "Imperial Fleet", "Rebel", "Rebels", "Empire", "Jedi Knights"]
person = ["General Kenobi", "Tarkin", "Red Ten", "Red Seven", "Red Six", "Red Nine", "Red Eleven", "Red Five", "Governor Tarkin", "Greedo", "Red Leader", "Biggs", "Tank", "Captain Antilles", "Green Leader", "Uncle Owen", "Aunt Beru", "Gray Leader", "Red Three", "Red Two", "Gold Leader", "General Calrissian", "General Madine", "General Solo", "Han", "Admiral Ackbar", "Janson", "General Veers", "Senator Organa", "Organa", "Boba Fett", "Luke", "Leia", "Princess", "Emperor", "Vader", "Threepio", "Solo", "Commander Skywalker", "Darth Vader", "Darth", "Skywalker", "Princess Leia", "Ord Mantell", "Master Luke", "Mistress Leia", "General Rieekan", "Captain Solo", "Chewie", "Chewbacca", "Admiral Ozzel", "Captain Piett", "Lord Vader", "Wedge", "Wedge Antilles", "goldenrod", "Goldenrod", "Artoo", "Yoda", "Ben Kenobi", "Ben", "Obi-Wan Kenobi", "Obi-Wan", "Captain Needa", "Lando", "Lando Calrissian", "Calrissian", "See-Threepio", "Master Yoda", "Jabba", "Jabba the Hutt", "Artoo-Detoo", "Deck Officer", "Rogue Two", "Echo Three", "Echo Seven", "Rogues Ten", "Eleven", "Rogue Three", "Rogue Leader", "Detoowha", "Seethreepiowha"]
place = ["Dagobah", "Toshi Station", "Dantooine", "Beggar's Canyon", "Mos Eisley", "Anchorhead", "Sanctuary Moon", "Sullust", "Endor", "Hoth", "Hoth", "Anoat", "Kessel", "Bespin", "Tibanna", "Tatooine", "Dagobah", "Echo Base", "Alderaan", "Taanab"]

user_dicts = [misc, org, person, place]
match_names = ["MISC", "ORG", "PERSON", "LOCATION"]

# This method takes the list of user dictionaries as input and compiles corresponding lists of regexes to search for later.

def reg_compile(user_dicts):
    regex_list = [[] for i in range(0, len(user_dicts))]
    count_list = 0
    for k in user_dicts:
        for j in k:
            regex_list[count_list].append(re.compile(j)) # LEAVE ON USUALLY?
        count_list = count_list + 1
    return regex_list
    
# Here we lock in the already running NLP server.

nlp = StanfordCoreNLP('http://localhost:9000')

# Here is some sample text.  It's good for simple testing and getting your feet wet, though.

text = (
    """On Sunday, the atm moisture profile of Mars was equal to thirty Rob Schneiders. 
    I'd buy that for a dollar.  At the White House, the soil moisture is as dry as certain
     counties in North Carolina, another reason South Carolina is superior for RapidEye.  
    The sea ice thickness is zero in both.""")


# This method loads the data.  It requires that the data is a csv with only one field per line, no header.
# It also removes those weird percent character issues due to coding (I don't really know the details of this).

def load_and_process(filepath):
    frame = pd.read_csv(filepath, header = -1)
    frame.columns = ['text']
    for i in range(0, len(frame)):
        frame['text'][i] = frame['text'][i].replace("%", "%25")
    return frame

# This method annotates the input text and extracts the named entities.  It outputs a list of dataframes (one for each sentence) with structure [original text, NER] and a string consisting of the entire sentence's text.

def annotate(frame):
    text = frame
    output = nlp.annotate(text, properties={
        'annotators': 'ner',
        'outputFormat': 'json'
        })
    df_list = []
    for x in range(0, len(output['sentences'])):
        test = output['sentences'][x]['tokens']
        test_pd = pd.DataFrame(test)
        df = pd.concat([test_pd.originalText, test_pd.ner], axis=1)    
        df_list.append(df)
    return(df_list, text)

# This method creates a list of lists of matches for each regex list/user dictionary (made earlier).
    
def regexMatch(regex_list, text):
    match_list = [[] for i in range(0, len(regex_list))]
    count_list = 0
    for a in regex_list:
        for j in a:
            try:
                match_list[count_list].append(j.search(text).group(0).split())
            except:
                pass
        count_list = count_list + 1
    return match_list

# This goes through the dataframe of original text and NER and overwrites with the regex tags where necessary.

# This crawls through each dataframe (i.e. sentence), then each row of each dataframe, then each list of matches in the list of lists of matches, then each term in each of these lists, and then compares each of these terms to the dataframe row in question.
# It compares the dataframe word to the first word in the matching phrase from the list. Then it calculates the number of words in the matching phrase, takes the appropriate number of subsequent dataframe word cells, and builds them into a string.
# It then sees if the match continues for the rest of the regex phrase. If so, it then checks the correct label (via the count variable) and inserts that into the appropriate cells in the other column.

def regexAnnotate(df_list, regex_matches):
        for k in df_list:
            for i in range(0, len(k)):
                count = 0
                for r in regex_matches:
                    count = count + 1
                    for l in r:
                        if k['originalText'][i] == l[0]:
                            num = len(l)
                            string = ""
                            for m in range(0, num):
                                string = string + k['originalText'][i+m] + " "
                            string = string.strip()
                            comp = ' '.join(l)
                            if comp == string:
                                for n in range(0, num):
                                    k['ner'][i+n] = match_names[count-1]

# This one writes the data. It takes in two numbers (the beginning and ending index of rows analyzed)
# and outputs one file in approximately correct format for NER training and testing.  

def write_data(filename_list, a = 0, b = 0):
    if b == 0:
        b = len(filename_list)
    output_filepath = 'Documents/coreNLP/output/output' + str(a) + '_' + str(b-1) + '.tsv'
    with open(output_filepath, 'w') as outfile:
        for fname in filename_list:
            with open(fname) as infile:
                outfile.write(infile.read())
    for fname in filename_list:
        os.remove(fname)
    print("Output file (" + output_filepath + ") written to disk")
    return output_filepath

# This method shows the output file.  Nothing fancy.

def show_file(filename):
    os.system('cd')
    os.system('vim ' + filename)

# This is the main method that incorporates the other methods.  Pulls in the frame's text column (and optionally, two numbers describing row indices of the range of the file you want to examine.  
# It merges each row's file into a singular file that eventually writes to disk via the method above.

def formatNER(frame_text, a = 0, b = 0):
    if b == 0:
        b = len(frame_text['text'])
    filenames = []
    regex_list = reg_compile(user_dicts)
    for q in range(a, b):        
        df_list, full = annotate(frame_text['text'][q]) #correct
        regex_matches = regexMatch(regex_list, full)
        regexAnnotate(df_list, regex_matches)
        df_final = df_list[0]
        for z in range(1, len(df_list)):
            df_final = pd.concat([df_final, df_list[z]], axis = 0, ignore_index = True)
        df_final.columns = ['Word', 'Named Entity Type']
        filenames.append("Documents/coreNLP/output/output_" + str(q) + ".txt")
        df_final.to_csv("Documents/coreNLP/output/output_" + str(q) + ".txt", sep = "\t", index = False, header = False)
    output = write_data(filenames)
    show_file(output)
    # This shuts down the server.  The tab doesn't automatically close, though.  Without this, you'll have to shut down the server manually (just close the tab when you're done).  Since it automatically runs a script that always starts the server, it will open another tab and throw an error, but it's not a big deal.
    os.system('lsof -t -i tcp:9000 | xargs kill')

######################################################################################################

abstracts = load_and_process('Documents/SW/SW.csv')

# Arguments are range of rows in CSV and dataframe column with text.

formatNER(abstracts)

with open('Documents/ESB.txt', 'r') as myfile:
    data = myfile.read().replace('\n', '')
formatNER(data, 0, 1)