import os
# This is the directory where all the corenlp stuff should live.
os.chdir('/Users/mmclean/Documents/coreNLP/corenlp_test/')
# This starts the server.
os.system('java -Xmx8g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer')