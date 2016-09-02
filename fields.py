from collections import OrderedDict
from read_funcs import *


FIELDS = OrderedDict([
    ('id', None),
    ('outcome', outcome),
    ('marijuana', binary_field("Marijuana")),
    ('appearance', binary_field("Appearance", "WNL", "Neat and appropriate")),
    ('Clothing', binary_field("Clothing", "WNL")),
    ('Sex', binary_field("Sex", "Female", "Male")),
    ('age', age),
    ('interpreter_used', binary_field("Interpreter Used", negative_value="None needed")),
    ('Other Agency Involvement', binary_field("Other Agency Involvement")),
    ('Psychiatric Review of Systems DEPRESSION', binary_field("Psychiatric Review of Systems DEPRESSION: Has the patient had periods of time lasting two weeks or longer in which, most of the day on most days, they felt little interest or pleasure in doing things, or they had to push themselves to do things")),
    ('DEPRESSION', binary_field("DEPRESSION: Has the patient had periods of time lasting two weeks or longer in which, most of the day on most days, they felt sad, down, or depressed")),
    ('Bipolar1', binary_field('BIPOLAR: Has patient ever had a period of time when he/she felt "up" or "high" without the use of substances')),
    ('Bipolar2', binary_field('BIPOLAR: Has patient ever had periods of being persistently irritable for several days, or had verbal/physical fights that seemed clearly out of characterBIPOLAR: Has patient ever had periods of being persistently irritable for several days, or had verbal/physical fights that seemed clearly out of character')),
    ('PSYCHOSIS1', binary_field('PSYCHOSIS: Has the patient had unusual experiences that are hard to explain')),
    ('PSYCHOSIS2', binary_field('PSYCHOSIS: Does the patient often have thoughts that make sense to them, but that other people say are strange')),
    ('GAD', binary_field('GAD: Has the patient had times when they worried excessively about day to day matters for most of the day, more days than not')),
    ('PANIC', binary_field('PANIC: Has the patient had episodes of sudden intense anxiety with physical sensations such as heart palpitations, trouble breathing, or dizziness that reached a peak very quickly and presented without warning')),
    ('ANXIETY SPECTRUM DISORDERS', binary_field('ANXIETY SPECTRUM DISORDERS: Does the patient have persistent fear triggered by specific objects (phobias) or situations (social anxiety) or by thought of having a panic attack')),
    ('OCD', neg_ternary_field('OCD: Does the patient struggle with repetitive unwanted thoughts or behaviors for at least one hour per day')),
    ('OBSESSIVE COMPULSIVE SPECTRUM DISORDERS', binary_field('Pickls at skin and cutivels when under stress.OBSESSIVE COMPULSIVE SPECTRUM DISORDERS: Does the patient have other repetitive, unwanted thoughts or behaviors that are non-functional and difficult to stop (e.g. excessive preoccupation with appearance, hairpulling/skin picking, motor or vocal tics')),
    ('ADHD', binary_field('ADHD: Does the patient have longstanding problems sustaining their attention in activities that are of mediocre interest to them')),
    ('PTSD1', binary_field('PTSD: Does the patient experience trauma related flashbacks or recurrent dreams/nightmares')),
    ('PTSD2', binary_field('PTSD: Does the patient feel themselves getting very upset whenever they are reminded of their traumatic experience')),
    ('EATING DISORDERS1', neg_ternary_field('EATING DISORDERS: Has the patient had periods of time during which they were concerned about eating or their weight')),
    ('EATING DISORDERS2', neg_ternary_field('EATING DISORDERS: Does the patient think they have an eating disorder')),
    ('DEMENTIA1', binary_field('DEMENTIA: Has anyone told the patient they are concerned the patient has memory problems')),
    ('DEMENTIA2', binary_field('DEMENTIA: Does the patient have trouble learning new information')),
    ('COMPLICATED GRIEF', binary_field('COMPLICATED GRIEF: Has it been more than 6 months since the loss of a loved one, and does grief continue to significantly interfere with the patients daily living')),
    ('Alcohol1', pos_ternary_field('Alcohol Use: How often did you have a drink containing alcohol in the past year', 'monthly', 'two to four times', 'never')),
    ('Cocaine', binary_field('Cocaine')),
    ('Sedative-Hypnotics', binary_field('Sedative-Hypnotics')),
    ('Stimulants', binary_field('Stimulants')),
    ('Opiates', binary_field('Opiates')),
    ('Hallucinogens', binary_field('Hallucinogens')),
    ('Prescription medications', binary_field('rescription medications for non-medical purposes')),
    ('ReadingLearning Disabilities', binary_field('ReadingLearning Disabilities')),
    ('Employment', binary_field('Employment Currently employed')),
    ('Financial Stress', binary_field('Financial Stress')),
    ('safe in current living situation', binary_field('Does patient feel safe in current living situation')),
    ('risk of losing current housing', binary_field('Is Patient at risk of losing current housing')),
    ('Military Service', binary_field('Hx of Military Service')),
    ('normal-Mental Status Exam', binary_field('normal-Mental Status Exam Was the exam performed? (If not, indicate reason)')),
    ('Divorce', word_count('divorce')),
    ('Effexor', word_count('effexor')),
    ('Suicide', word_count('suicid')),
    ('hypomani', word_count('hypomani')),
    ('bupropion', word_count('bupropion')),
    ('QHS', word_count('QHS')),
    ('Hospitalization', word_count(['Admission','Signing in the patient','Sign in', 'Baker act', 'Hospitalization','Hospitalized','ER','Emergency Room','Sectioned','Section','Committed','Court commitment','Placement','Institutionalize','Institutionalization','hospital','center'])),
    ('major consequences', word_count(['Hurt themselves','Hurt others','Homicide','Attempt Suicide','Progression of illness','Chronicity of mental illness','Inability to take care of self','Homelessness','Unemployment','On disability','Social Isolation','Estrangement','Disenfranchised'])),
    ('opiate', word_count('opiate')),
    ('poly-substance', word_count('poly-substance')),
    ('toxicology', word_count('toxicology')),
    ('single', word_count('single')),
    ('white', word_count('white')),
    ('post-traumatic', word_count('post-traumatic')),
    ('stress disorder', word_count('stress disorder')),
    ('anxiety', word_count('anxiety')),
    ('bulimia', word_count('bulimia')),
    ('nervosa', word_count('nervosa')),
    ('endometriosis', word_count('endometriosis')),
    ('Suboxone', word_count('Suboxone')),
    ('cocaine', word_count('cocaine')),
    ('crack cocaine', word_count('crack cocaine')),
    ('illicit', word_count('illicit')),
    ('Percocet', word_count('Percocet')),
    ('oxycodone', word_count('oxycodone')),
    ('Dilaudid', word_count('Dilaudid')),
    ('violence', word_count('violence')),
    ('self-injurious', word_count('self-injurious')),
    ('sexual trauma', word_count('sexual trauma')),
    ('anxious', word_count('anxious')),
    ('drive', word_count('drive')),
    ('seizures', word_count('seizures')),
    ('firearms', word_count('firearms')),
    ('addiction', word_count('addict')),
    ('arrest', word_count(['arrest', 'jail', 'cop', 'police', 'sheriff'])),
    ('Outpatient', word_count('Recommendations / Plan Level of Care: Outpatient')),
    ('Addiction Treatment', word_count('Addiction Treatment')),
    ('Medication Treatment', word_count('Medication Treatment')),
    ('Cognitive Behavioral Therapy (CBT)', word_count(['Cognitive Behavioral Therapy', 'CBT)'])),
    ('Group Therapy', word_count('Group Therapy')),
    ('Psychiatric History Hx of Inpatient Treatment', binary_field('Psychiatric History Hx of Inpatient Treatment')),
    ('Outpatient Treatment', binary_field('Outpatient Treatment')),
    ('support group', word_count('support group')),
    ('case mgt services', word_count('case mgt services')),
    ('therapy', word_count('therapy')),
    ('chronic risk', binary_field('Does patient have chronic high risk')),
    ('Hx of Outpatient Treatment', binary_field('Hx of Outpatient Treatment')),
    ('Suicidal Behavior Hx of Suicidal Behavior', binary_field('Suicidal Behavior Hx of Suicidal Behavior')),
    ('Hx of Non Suicidal Self Injurious Behavior', binary_field('Hx of Non Suicidal Self Injurious Behavior')),
    ('Violent Behavior Hx of Violent Behavior', binary_field('Violent Behavior Hx of Violent Behavior')),
    ('further medical or neurological assessments', binary_field('Is the patient being referred for further medical or neurological assessments (Please specify)')),
    ('Did patient endorse thoughts of harm to self or others', binary_field("Did patient endorse thoughts of harm to self or others during today's session")),
    ('History of drug use', binary_field('History of drug use')),
    ('Referral/Treatment Needed', binary_field('Referral/Treatment Needed')),
    ('History of physical fights when drinking', binary_field('History of physical fights when drinking and prior to service')),
    ('sober', word_count(['sober', 'sobriet'])),
    ('detox', word_count('detox')),
    ('iop', word_count(['iop', 'intensive outpatient'])),
    ('program', word_count(['program', 'service'])),
    ('depend', word_count('depend')),
    ('none', word_count(['none','no','nwl','NWL','No'])),
    ('no', word_count('no')),
    ('yes', word_count('yes')),
    ('Independent', word_count('Independent')),
    ('psychotheraphy', word_count('psychotheraphy')),
    ('couples theraphy', word_count('couples theraphy')),
    ('group thearphy', word_count('group thearphy')),
    ('short-term thearphy', word_count('short-term thearphy')),
    ('cancer thearphy', word_count('cancer thearphy')),
    ('pharmacotheraphy', word_count('pharmacotheraphy')),
    ('aganist therapy', word_count('aganist therapy')),
    ('family theraphy', word_count('family theraphy')),
    ('sleep', word_count('sleep')),
    ('insomnia', word_count('insomnia')),
    ('moniter', word_count('moniter')),
    ('motivated', word_count('motivated')),
    ('ADHD2', word_count(['Hypertensive','hyperactivity','academic','learning','deficit'])),
    ('mood', word_count('mood')),
    ('depression', word_count(['depression', 'depressive'])),
    ('cognitive', word_count('cognitive')),
    ('cyclic disorder', word_count('cyclic disorder')),
])