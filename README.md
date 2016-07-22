# CoreNLP fast annotator and NER scripts

These are a couple scripts that aid in annotating text data in TSV format for custom NER training and testing. The main function is to allow you to type in user dictionaries related to certain classes of words and plug them in on top of the basic NER engine, hopefully speeding up training for your custom NER classifier.


### dependencies
You'll need Stanford's CoreNLP and all its dependencies (java, anything else).  In addition, pycorenlp is a python coreNLP wrapper (as you might have surmised) and should also be installed.  I also use ttab for a fairly small part of the proceedings, so you should either install that or just manually start the coreNLP server each time you want to work with it.  Pandas, re, and time are all python packages used here, easily installed via pip.

These scripts should be placed in the same directory that holds the main coreNLP folder (where the first files are build.gradle, build.xml, etc.)

### a few notes on jar files
So I may have overdone it on the jar files I collected.  If you run into an error with the standard jar files given by the out-of-the-box coreNLP installation, I have run through my exact setup below.  I downloaded some jars externally and copied them into different files to make some things work.  It was a less than scientific process that got things to work at the cost of some (possibly a lot of) redundancy.


All the jars are ignored and I lost track of the ones that were actually necessary at some point but I have the following in the corenlp_test folder:
        - EJML.jar
        - joda-time.jar
        - jollyday-0.4.7.jar
        - slf4j-api.jar
        - slf4j-simple.jar
        - slf4j.jar
        - stanford-corenlp.jar
        - stanford-english-corenlp-2016-01-10-models.jar
        - stanford-english-corenlp-models-current.jar
        - stanford-ner-3.6.0-javadoc.jar
        - stanford-ner-3.6.0-sources.jar
        - stanford-ner-3.6.0.jar
        - stanford-ner-resources.jar
        - stanford-ner.jar
 
    And the following in the lib directory (some are repeated from above, and they are surely not all necessary):
        - ant-contrib-1.0b3.jar
        - appbundler-1.0.jar
        - AppleJavaExtensions.jar
        - commons-lang3-3.1.jar
        - commons-logging.jar
        - ejml-0.23.jar
        - javacc.jar
        - javax.json.jar
        - javax.servlet.jar
        - jflex-1.5.1.jar
        - joda-time.jar
        - jollyday-0.4.7.jar
        - junit.jar
        - log4j-1.2.16.jar
        - lucene-analyzers-common-4.10.3.jar
        - lucene-core-4.10.3.jar
        - lucene-demo-4.10.3.jar
        - lucene-queries-4.10.3.jar
        - lucene-queryparser-4.10.3.jar
        - protobuf.jar
        - slf4j-api.jar
        - slf4j-simple.jar
        - stanford-corenlp.jar
        - stanford-english-corenlp-2016-01-10-models.jar
        - stanford-english-corenlp-models-current.jar
        - stanford-ner-3.6.0-javadoc.jar
        - stanford-ner-3.6.0-sources.jar
        - stanford-ner-3.6.0.jar
        - stanford-ner-resources.jar
        - stanford-ner.jar
        - xom-1.2.10.jar


