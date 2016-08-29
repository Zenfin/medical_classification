We could try using Biopython to correlate information with pubmed articles.


# 8-27-16

Exploring freq_filter for bigrams, I found info at the following freqencies
1: Mainly returns values such as "Average", "Memory" that are standard fields in each file.
2: Has more intersting information but still alot of useless combinations like ("I", "am"), ("Not", "Done")
3: We start getting more intersting comboes like ("violent behavior"), ("Suicidal", "Behvior") but may not be noteworthy

Trigrams seem to be useless as they detect fluff like ("Has" "the" "patient"), ("does", "the" "patient").


# 8-28-16

Chief complaint does a very good job retrieving as well as history of prec (HOP).  Some files have no HOP, others
do not terminated in the same manner.  The list order is in order of frequency so that we can avoid grabbing too
much data for as many files as possible.  About 20-30ish files are not caught in the first two items of the lists.


Level of distress as well as strengths and abilities seems to be an error that could indicate a good classification.
Should take a look at the data grabbed by Viveks script to see if it is there.
