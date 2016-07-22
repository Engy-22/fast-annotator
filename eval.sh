cd
cd Documents/coreNLP/corenlp_test/
java -Xmx12g -classpath "stanford-ner.jar:lib/*" edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier ner-ESB-ROTJ_model.ser.gz -testFile test_files/SW.tsv