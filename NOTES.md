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


# 8-30-16

Because the words are notuseful in predition, try bigrams, trigrams.  
Also try adding length of article, each cateogry, etc.
Could also do number of lines in the file.
Or even number of blank lines in a file
Could also do number of lines in the file.
Or even number of blank lines in a file.


# 8-31-16

Compare the refactored data to the previous data.  Just roll back a commit.

Develop a scale to predict with the PANNS scale.
http://www.ncbi.nlm.nih.gov/books/NBK169692/


# 9-6-16

TODO:

Cascading each category
Going through manually classifying EHRs using various scales, then checking if the evaulation matches.
Extracting more information from the data that seems important but is not included
Write a readme


# 9-25-16

Exploring records:

## Severe

### Steps to take:

1. See if you can extract history of ___ from each and then see if they are the bad ones.
2. Using parsy mcparse face or something to find negatives for history and suidcide for example no intent to harm
3. Get positivity of sentence

- Having a history of an illness: history of ____ , h/o, hx (ignore History of Present Illness and Precipitating Events)
no prior psychiatric history

- Suicide Attempts
attempted suicide
SA or suicide attempt
kill himself, kill herself
SI/HI
No thought, desire, or intent to harm herself or others. No si/sx of mania, psychosis, OCD

Number of drugs in the diagnosis

denies symptoms/ denies any symptoms
denying

PTSD: Symptoms: intrusive thoughts, nightmares, emotional and physical distress, avoidance, loss of interest, detachment, numbing, poor concentration, sleep disturbance (5 hrs interrupted), anger/irritability, exaggerated startle, hypervigilance

long-term psychiatric care / long-term care

alcohol dependence

sexually abused

major depression, psychotic features, alcohol dependence

Other ategories:
- Unstable Thoughts:  Nightmares, panic attacks, suicidal thoughts

psychotic

## Moderate

optimistic
enjoy
pleasure
