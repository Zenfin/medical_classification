from collections import OrderedDict
from read_funcs import *
from rating_scales import negative_match, positive_match, existence


FIELDS = OrderedDict([
    ('id', {}),
    ('outcome', {
        'func': outcome,
    }),
    ('marijuana', {
        'func': binary_field("Marijuana"),
    }),
    ('appearance', {
        'func': binary_field("Appearance", "WNL", "Neat and appropriate"),
    }),
    ('Clothing', {
        'func': binary_field("Clothing", "WNL"),
        'BPRS': negative_match([13]),
    }),
    ('Sex', {
        'func': binary_field("Sex", "Female", "Male"),
    }),
    ('age', {
        'func': age,
    }),
    ('interpreter_used', {
        'func': binary_field("Interpreter Used", negative_value="None needed"),
    }),
    ('Other Agency Involvement', {
        'func': binary_field("Other Agency Involvement"),
    }),
    ('Psychiatric Review of Systems DEPRESSION', {
        'func': binary_field("Psychiatric Review of Systems DEPRESSION: Has the patient had periods of time lasting two weeks or longer in which, most of the day on most days, they felt little interest or pleasure in doing things, or they had to push themselves to do things"),
        'BPRS': positive_match([3, 13]),
    }),
    ('DEPRESSION', {
        'func': binary_field("DEPRESSION: Has the patient had periods of time lasting two weeks or longer in which, most of the day on most days, they felt sad, down, or depressed"),
        'BPRS': positive_match([3, 17]),
    }),
    ('Bipolar1', {
        'func':  binary_field('BIPOLAR: Has patient ever had a period of time when he/she felt "up" or "high" without the use of substances'),
        'BPRS': positive_match([7, 21]),
    }),
    ('Bipolar2',  {
        'func': binary_field('BIPOLAR: Has patient ever had periods of being persistently irritable for several days, or had verbal/physical fights that seemed clearly out of characterBIPOLAR: Has patient ever had periods of being persistently irritable for several days, or had verbal/physical fights that seemed clearly out of character'),
        'BPRS': positive_match([6]),
    }),
    ('PSYCHOSIS1',  {
        'func': binary_field('PSYCHOSIS: Has the patient had unusual experiences that are hard to explain'),
        'BPRS': positive_match([10, 12]),
    }),
    ('PSYCHOSIS2',  {
        'func': binary_field('PSYCHOSIS: Does the patient often have thoughts that make sense to them, but that other people say are strange'),
        'BPRS': positive_match([11, 15]),
    }),
    ('GAD',  {
        'func': binary_field('GAD: Has the patient had times when they worried excessively about day to day matters for most of the day, more days than not'),
        'BPRS': positive_match([2]),
    }),
    ('PANIC',  {
        'func': binary_field('PANIC: Has the patient had episodes of sudden intense anxiety with physical sensations such as heart palpitations, trouble breathing, or dizziness that reached a peak very quickly and presented without warning'),
        'BPRS': positive_match([2]),
    }),
    ('ANXIETY SPECTRUM DISORDERS',  {
        'func': binary_field('ANXIETY SPECTRUM DISORDERS: Does the patient have persistent fear triggered by specific objects (phobias) or situations (social anxiety) or by thought of having a panic attack'),
        'BPRS': positive_match([1, 2]),
    }),
    ('OCD',  {
        'func': neg_ternary_field('OCD: Does the patient struggle with repetitive unwanted thoughts or behaviors for at least one hour per day'),
        'BPRS': positive_match([12]),
    }),
    ('OBSESSIVE COMPULSIVE SPECTRUM DISORDERS',  {
        'func': binary_field('Pickls at skin and cutivels when under stress.OBSESSIVE COMPULSIVE SPECTRUM DISORDERS: Does the patient have other repetitive, unwanted thoughts or behaviors that are non-functional and difficult to stop (e.g. excessive preoccupation with appearance, hairpulling/skin picking, motor or vocal tics'),
        'BPRS': positive_match([12, 13]),
    }),
    ('ADHD',  {
        'func': binary_field('ADHD: Does the patient have longstanding problems sustaining their attention in activities that are of mediocre interest to them'),
        'BPRS': positive_match([22]),
    }),
    ('PTSD1',  {
        'func': binary_field('PTSD: Does the patient experience trauma related flashbacks or recurrent dreams/nightmares'),
        'BPRS': positive_match([5]),
    }),
    ('PTSD2',  {
        'func': binary_field('PTSD: Does the patient feel themselves getting very upset whenever they are reminded of their traumatic experience'),
        'BPRS': positive_match([5, 6]),
    }),
    ('EATING DISORDERS1',  {
        'func': neg_ternary_field('EATING DISORDERS: Has the patient had periods of time during which they were concerned about eating or their weight'),
        'BPRS': positive_match([1]),
    }),
    ('EATING DISORDERS2',  {
        'func': neg_ternary_field('EATING DISORDERS: Does the patient think they have an eating disorder'),
        'BPRS': positive_match([1]),
    }),
    ('DEMENTIA1',  {
        'func': binary_field('DEMENTIA: Has anyone told the patient they are concerned the patient has memory problems'),
        'BPRS': positive_match([15]),
    }),
    ('DEMENTIA2',  {
        'func': binary_field('DEMENTIA: Does the patient have trouble learning new information'),
        'BPRS': positive_match([15]),
    }),
    ('COMPLICATED GRIEF',  {
        'func': binary_field('COMPLICATED GRIEF: Has it been more than 6 months since the loss of a loved one, and does grief continue to significantly interfere with the patients daily living'),
        'BPRS': positive_match([3, 5]),
    }),
    ('Alcohol1',  {
        'func': pos_ternary_field('Alcohol Use: How often did you have a drink containing alcohol in the past year', 'monthly', 'two to four times', 'never'),
    }),
    ('Cocaine',  {
        'func': binary_field('Cocaine'),
    }),
    ('Sedative-Hypnotics',  {
        'func': binary_field('Sedative-Hypnotics'),
    }),
    ('Stimulants',  {
        'func': binary_field('Stimulants'),
    }),
    ('Opiates',  {
        'func': binary_field('Opiates'),
    }),
    ('Hallucinogens',  {
        'func': binary_field('Hallucinogens'),
    }),
    ('Prescription medications',  {
        'func': binary_field('rescription medications for non-medical purposes'),
    }),
    ('ReadingLearning Disabilities',  {
        'func': binary_field('ReadingLearning Disabilities'),
    }),
    ('Employment',  {
        'func': binary_field('Employment Currently employed'),
    }),
    ('Financial Stress',  {
        'func': binary_field('Financial Stress'),
    }),
    ('safe in current living situation',  {
        'func': binary_field('Does patient feel safe in current living situation'),
    }),
    ('risk of losing current housing',  {
        'func': binary_field('Is Patient at risk of losing current housing'),
    }),
    ('Military Service',  {
        'func': binary_field('Hx of Military Service'),
    }),
    ('normal-Mental Status Exam',  {
        'func': binary_field('normal-Mental Status Exam Was the exam performed? (If not, indicate reason)'),
    }),
    ('Divorce',  {
        'func': word_count('divorce'),
    }),
    ('Effexor',  {
        'func': word_count('effexor'),
    }),
    ('Suicide',  {
        'func': word_count('suicid'),
        'BPRS': existence([4]),
    }),
    ('hypomani',  {
        'func': word_count('hypomani'),
        'BPRS': existence([23]),
    }),
    ('bupropion',  {
        'func': word_count('bupropion'),
    }),
    ('QHS',  {
        'func': word_count('QHS'),
    }),
    ('Hospitalization',  {
        'func': word_count(['Admission','Signing in the patient','Sign in', 'Baker act', 'Hospitalization','Hospitalized','ER','Emergency Room','Sectioned','Section','Committed','Court commitment','Placement','Institutionalize','Institutionalization','hospital','center']),
    }),
# LETA APLIT THIS UP
    ('major consequences',  {
        'func': word_count(['Hurt themselves','Hurt others','Homicide']),
        'BPRS': existence([6, 9]),
    }),
    ('attempted_suicide',  {
        'func': word_count(['Attempt Suicide']),
        'BPRS': existence([4]),
    }),
    ('cant take care of self',  {
        'func': word_count(['Inability to take care of self','Homelessness','Unemployment','On disability']),
    }),
    ('isolation',  {
        'func': word_count(['Social Isolation','Estrangement','Disenfranchised']),
        'BPRS': existence([9]),
    }),
    ('progressing_illness', {
        'func': word_count(['Progression of illness','Chronicity of mental illness']),
    }),
    ('opiate',  {
        'func': word_count('opiate'),
    }),
    ('poly-substance',  {
        'func': word_count('poly-substance'),
    }),
    ('toxicology',  {
        'func': word_count('toxicology'),
    }),
    ('single',  {
        'func': word_count('single'),
    }),
    ('white',  {
        'func': word_count('white'),
    }),
    ('post-traumatic',  {
        'func': word_count('post-traumatic'),
    }),
    ('stress disorder',  {
        'func': word_count('stress disorder'),
    }),
    ('anxiety',  {
        'func': word_count('anxiety'),
        'BPRS': existence([2]),
    }),
    ('bulimia',  {
        'func': word_count('bulimia'),
        'BPRS': existence([1]),
    }),
    ('nervosa',  {
        'func': word_count('nervosa'),
        'BPRS': existence([2]),
    }),
    ('endometriosis',  {
        'func': word_count('endometriosis'),
    }),
    ('Suboxone',  {
        'func': word_count('Suboxone'),
    }),
    ('cocaine',  {
        'func': word_count('cocaine'),
    }),
    ('crack cocaine',  {
        'func': word_count('crack cocaine'),
    }),
    ('illicit',  {
        'func': word_count('illicit'),
    }),
    ('Percocet',  {
        'func': word_count('Percocet'),
    }),
    ('oxycodone',  {
        'func': word_count('oxycodone'),
    }),
    ('Dilaudid',  {
        'func': word_count('Dilaudid'),
    }),
    ('violence',  {
        'func': word_count('violence'),
        'BPRS': existence([6]),
    }),
    ('self-injurious',  {
        'func': word_count('self-injurious'),
        'BPRS': existence([13]),
    }),
    ('sexual trauma',  {
        'func': word_count('sexual trauma'),
    }),
    ('anxious',  {
        'func': word_count('anxious'),
        'BPRS': existence([2]),
    }),
    ('drive',  {
        'func': word_count('drive'),
    }),
    ('seizures',  {
        'func': word_count('seizures'),
    }),
    ('firearms',  {
        'func': word_count('firearms'),
    }),
    ('addiction',  {
        'func': word_count('addict'),
    }),
    ('arrest',  {
        'func': word_count(['arrest', 'jail', 'cop', 'police', 'sheriff']),
    }),
    ('Outpatient',  {
        'func': word_count('Recommendations / Plan Level of Care: Outpatient'),
    }),
    ('Addiction Treatment',  {
        'func': word_count('Addiction Treatment'),
    }),
    ('Medication Treatment',  {
        'func': word_count('Medication Treatment'),
    }),
    ('Cognitive Behavioral Therapy (CBT)',  {
        'func': word_count(['Cognitive Behavioral Therapy', 'CBT)']),
    }),
    ('Group Therapy',  {
        'func': word_count('Group Therapy'),
    }),
    ('Psychiatric History Hx of Inpatient Treatment',  {
        'func': binary_field('Psychiatric History Hx of Inpatient Treatment'),
    }),
    ('Outpatient Treatment',  {
        'func': binary_field('Outpatient Treatment'),
    }),
    ('support group',  {
        'func': word_count('support group'),
    }),
    ('case mgt services',  {
        'func': word_count('case mgt services'),
    }),
    ('therapy',  {
        'func': word_count('therapy'),
    }),
    ('chronic risk',  {
        'func': binary_field('Does patient have chronic high risk'),
    }),
    ('Hx of Outpatient Treatment',  {
        'func': binary_field('Hx of Outpatient Treatment'),
    }),
    ('Suicidal Behavior Hx of Suicidal Behavior',  {
        'func': binary_field('Suicidal Behavior Hx of Suicidal Behavior'),
        'BPRS': positive_match([4]),
    }),
    ('Hx of Non Suicidal Self Injurious Behavior',  {
        'func': binary_field('Hx of Non Suicidal Self Injurious Behavior'),
        'BPRS': positive_match([6]),
    }),
    ('Violent Behavior Hx of Violent Behavior',  {
        'func': binary_field('Violent Behavior Hx of Violent Behavior'),
        'BPRS': positive_match([6]),
    }),
    ('further medical or neurological assessments',  {
        'func': binary_field('Is the patient being referred for further medical or neurological assessments (Please specify)'),
    }),
    ('Did patient endorse thoughts of harm to self or others',  {
        'func': binary_field("Did patient endorse thoughts of harm to self or others during today's session"),
        'BPRS': positive_match([6, 15]),
    }),
    ('History of drug use',  {
        'func': binary_field('History of drug use'),
    }),
    ('Referral/Treatment Needed',  {
        'func': binary_field('Referral/Treatment Needed'),
    }),
    ('History of physical fights when drinking',  {
        'func': binary_field('History of physical fights when drinking and prior to service'),
        'BPRS': positive_match([6]),
    }),
    ('sober',  {
        'func': word_count(['sober', 'sobriet']),
    }),
    ('detox',  {
        'func': word_count('detox'),
    }),
    ('iop',  {
        'func': word_count(['iop', 'intensive outpatient']),
    }),
    ('program',  {
        'func': word_count(['program', 'service']),
    }),
    ('depend',  {
        'func': word_count('depend'),
    }),
    ('none',  {
        'func': word_count(['none','no','nwl','NWL','No']),
    }),
    ('no',  {
        'func': word_count('no'),
    }),
    ('yes',  {
        'func': word_count('yes'),
    }),
    ('Independent',  {
        'func': word_count('Independent'),
    }),
    ('psychotheraphy',  {
        'func': word_count('psychotheraphy'),
    }),
    ('couples theraphy',  {
        'func': word_count('couples theraphy'),
    }),
    ('group thearphy',  {
        'func': word_count('group thearphy'),
    }),
    ('short-term thearphy',  {
        'func': word_count('short-term thearphy'),
    }),
    ('cancer thearphy',  {
        'func': word_count('cancer thearphy'),
    }),
    ('pharmacotheraphy',  {
        'func': word_count('pharmacotheraphy'),
    }),
    ('aganist therapy',  {
        'func': word_count('aganist therapy'),
    }),
    ('family theraphy',  {
        'func': word_count('family theraphy'),
    }),
    ('sleep',  {
        'func': word_count('sleep'),
    }),
    ('insomnia',  {
        'func': word_count('insomnia'),
    }),
    ('moniter',  {
        'func': word_count('moniter'),
    }),
    ('motivated',  {
        'func': word_count('motivated'),
    }),
    ('ADHD2',  {
        'func': word_count(['Hypertensive','hyperactivity','academic','learning','deficit']),
        'BPRS': existence([22]),
    }),
    ('mood',  {
        'func': word_count('mood'),
    }),
    ('depression',  {
        'func': word_count(['depression', 'depressive']),
        'BPRS': existence([3]),
    }),
    ('cognitive',  {
        'func': word_count('cognitive'),
    }),
    ('cyclic disorder', {
        'func': word_count('cyclic disorder'),
    }),
])
