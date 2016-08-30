#python
import os

def m_encoding(words,data,fp_w):
	output=0
	fp_w.write(',')
	for word in words:
		if(str(data).find(word)>0):
			output=output+str(data).count(word)
	#fp_w.write(str(output))
	#fp_w.write(str(str(data).find(word)))
	fp_w.write(str(output))
	
	

def process(file_name,output_name):
	#lst = os.listdir("C:/Users/ThinkPad/Box Sync/healthcare/track_2_training/training")
	lst = os.listdir(file_name)
	#C:\Users\vivek4\Desktop\Healthcare-I2B2\track_2_training\training
	fp_w=open(output_name,'w')

	def age(m_file):
		m_fp=open(m_file)
		m_data=m_fp.readlines()
		for m_line in m_data:
			if(str(m_line).find('Sex:')>0):
				m_line=m_line.split('Sex')
				return m_line[0]
	#header
	fp_w.write('id, outcome,marijuana,appearance,Clothing,Sex,age,interpreter_used,Other Agency Involvement,Psychiatric Review of Systems DEPRESSION, DEPRESSION, Bipolar1 ,Bipolar2,PSYCHOSIS1,PSYCHOSIS2,GAD,PANIC,ANXIETY SPECTRUM DISORDERS,OCD,OBSESSIVE COMPULSIVE SPECTRUM DISORDERS,ADHD,PTSD1,PTSD2,EATING DISORDERS1,EATING DISORDERS2,DEMENTIA1,DEMENTIA2,COMPLICATED GRIEF,Alcohol1,Marijuana,Cocaine,Sedative-Hypnotics,Stimulants,Opiates,Hallucinogens,Prescription medications,ReadingLearning Disabilities,Employment,Financial Stress,safe in current living situation,risk of losing current housing,Military Service,normal-Mental Status Exam,Divorce,Effexor,Suicide,hypomani,bupropion,QHS,Hospitalization,major consequences,opiate,poly-substance,toxicology, single,white,post-traumatic, stress disorder, anxiety, bulimia, nervosa, endometriosis, Suboxone, cocaine, crack cocaine, illicit, Percocet,oxycodone,Dilaudid,   violence,suicide, self-injurious, sexual trauma,anxious,drive,seizures,firearms,addiction,arrest,Outpatient,Addiction Treatment,Medication Treatment,Cognitive Behavioral Therapy (CBT),Group Therapy,psychopharm,Psychiatric History Hx of Inpatient Treatment,Outpatient Treatment,support group,case mgt services,therapy,chronic risk,Hx of Outpatient Treatment,Suicidal Behavior Hx of Suicidal Behavior,Hx of Non Suicidal Self Injurious Behavior,Violent Behavior Hx of Violent Behavior,further medical or neurological assessments,Did patient endorse thoughts of harm to self or others,History of drug use,Referral/Treatment Needed,History of physical fights when drinking,sober,detox,iop,program, depend,none,no,yes,Independent,psychotheraphy,couples theraphy,group thearphy,short-term thearphy,cancer thearphy,pharmacotheraphy,aganist therapy,family theraphy,sleep,insomnia,moniter,motivated,ADHD2,mood,depression,cognitive,cyclic disorder\n')	
	for file in lst:
		if(file.endswith('_gs.xml')):
			fp_w.write(str(file))
			fp_w.write(',')
			fp=open(file_name+file)
			data=fp.readlines()
			#tag1- outcome
			if(str(data).find('score=\"MODERATE\"')>0):
				#fp_w.write('MODERATE')
				fp_w.write('2')
			if(str(data).find('score=\"ABSENT\"')>0):
				#fp_w.write('ABSENT')
				fp_w.write('0')
			if(str(data).find('score=\"MILD\"')>0):
				#fp_w.write('MILD')
				fp_w.write('1')
			if(str(data).find('score=\"SEVERE\"')>0):
				#fp_w.write('SEVERE')
				fp_w.write('3')
			
			#marijuana: Yes /No
			fp_w.write(',')
			if(str(data).find('Marijuana: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('Marijuana: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
			
			#appearance: WNL (WNL : Within normal limits)
			fp_w.write(',')
			if(str(data).find('Appearance: WNL')>0):
				#fp_w.write('WNL')
				fp_w.write('0')
			elif(str(data).find('Appearance: Neat and appropriate')>0):
				#fp_w.write('Neat and appropriate')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
				
			
			
			#Clothing: WNL
			fp_w.write(',')
			if(str(data).find('Clothing: WNL')>0):
				#fp_w.write('WNL')
				fp_w.write('0')
			else:
				fp_w.write('-2') #-2 for missing
				
			#Sex: Female
			fp_w.write(',')
			if(str(data).find('Sex: Female')>0):
				#fp_w.write('Female')
				fp_w.write('0')
			elif(str(data).find('Sex: Male')>0):
				#fp_w.write('Male')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
				
			#age
			fp_w.write(',')
			age_m=str(age(file_name+file))[0:2]
			try:
				if(int(age_m)>0 and int(age_m)<150):
					fp_w.write(str(age(file_name+file))[0:2])
				else:
					fp_w.write('-1')
			except:
				fp_w.write('-1')
			
			#interpreter used
			fp_w.write(',')
			if(str(data).find('Interpreter Used: None needed')>0):
				#fp_w.write('None')
				fp_w.write('-1')
			else:
				fp_w.write('-2') #-2 for missing
				
			#Wanda Goff, LICSWOther Agency Involvement: No
			fp_w.write(',')
			#if(str(data).find('Wanda Goff, LICSWOther Agency Involvement: No')>0):
			if(str(data).find('Other Agency Involvement: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			#if(str(data).find('Wanda Goff, LICSWOther Agency Involvement: Yes')>0):
			elif(str(data).find('Other Agency Involvement: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
				
			#Psychiatric Review of Systems DEPRESSION: Has the patient had periods of time lasting two weeks or longer in which, most of the day on most days, they felt little interest or pleasure in doing things, or they had to push themselves to do things: Yes
			fp_w.write(',')
			if(str(data).find('Psychiatric Review of Systems DEPRESSION: Has the patient had periods of time lasting two weeks or longer in which, most of the day on most days, they felt little interest or pleasure in doing things, or they had to push themselves to do things: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			elif(str(data).find('Psychiatric Review of Systems DEPRESSION: Has the patient had periods of time lasting two weeks or longer in which, most of the day on most days, they felt little interest or pleasure in doing things, or they had to push themselves to do things: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			else:
				fp_w.write('-2') #-2 for missing
				
			#DEPRESSION: Has the patient had periods of time lasting two weeks or longer in which, most of the day on most days, they felt sad, down, or depressed: Yes
			fp_w.write(',')
			if(str(data).find('DEPRESSION: Has the patient had periods of time lasting two weeks or longer in which, most of the day on most days, they felt sad, down, or depressed: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			elif(str(data).find('DEPRESSION: Has the patient had periods of time lasting two weeks or longer in which, most of the day on most days, they felt sad, down, or depressed: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			else:
				fp_w.write('-2') #-2 for missing
				
			
			#BIPOLAR: Has patient ever had a period of time when he/she felt "up" or "high" without the use of substances: No
			fp_w.write(',')
			if(str(data).find('BIPOLAR: Has patient ever had a period of time when he/she felt "up" or "high" without the use of substances: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			elif(str(data).find('BIPOLAR: Has patient ever had a period of time when he/she felt "up" or "high" without the use of substances: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			else:
				fp_w.write('-2') #-2 for missing
			
			#BIPOLAR: Has patient ever had periods of being persistently irritable for several days, or had verbal/physical fights that seemed clearly out of character: No
			fp_w.write(',')
			if(str(data).find('BIPOLAR: Has patient ever had periods of being persistently irritable for several days, or had verbal/physical fights that seemed clearly out of character: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			elif(str(data).find('BIPOLAR: Has patient ever had periods of being persistently irritable for several days, or had verbal/physical fights that seemed clearly out of character: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			else:
				fp_w.write('-2') #-2 for missing
				
			
			#PSYCHOSIS: Has the patient had unusual experiences that are hard to explain: No
			fp_w.write(',')
			if(str(data).find('PSYCHOSIS: Has the patient had unusual experiences that are hard to explain: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			elif(str(data).find('PSYCHOSIS: Has the patient had unusual experiences that are hard to explain: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			else:
				fp_w.write('-2') #-2 for missing
			
			#PSYCHOSIS: Does the patient often have thoughts that make sense to them, but that other people say are strange: No
			fp_w.write(',')
			if(str(data).find('PSYCHOSIS: Does the patient often have thoughts that make sense to them, but that other people say are strange: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			elif(str(data).find('PSYCHOSIS: Does the patient often have thoughts that make sense to them, but that other people say are strange: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			else:
				fp_w.write('-2') #-2 for missing
			
			#GAD: Has the patient had times when they worried excessively about day to day matters for most of the day, more days than not: No
			fp_w.write(',')
			if(str(data).find('GAD: Has the patient had times when they worried excessively about day to day matters for most of the day, more days than not: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			elif(str(data).find('GAD: Has the patient had times when they worried excessively about day to day matters for most of the day, more days than not: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			else:
				fp_w.write('-2') #-2 for missing
			
			#PANIC: Has the patient had episodes of sudden intense anxiety with physical sensations such as heart palpitations, trouble breathing, or dizziness that reached a peak very quickly and presented without warning: Yes
			fp_w.write(',')
			if(str(data).find('PANIC: Has the patient had episodes of sudden intense anxiety with physical sensations such as heart palpitations, trouble breathing, or dizziness that reached a peak very quickly and presented without warning: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			elif(str(data).find('PANIC: Has the patient had episodes of sudden intense anxiety with physical sensations such as heart palpitations, trouble breathing, or dizziness that reached a peak very quickly and presented without warning: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			else:
				fp_w.write('-2') #-2 for missing
				
			#ANXIETY SPECTRUM DISORDERS: Does the patient have persistent fear triggered by specific objects (phobias) or situations (social anxiety) or by thought of having a panic attack: No
			fp_w.write(',')
			if(str(data).find('ANXIETY SPECTRUM DISORDERS: Does the patient have persistent fear triggered by specific objects (phobias) or situations (social anxiety) or by thought of having a panic attack: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			elif(str(data).find('ANXIETY SPECTRUM DISORDERS: Does the patient have persistent fear triggered by specific objects (phobias) or situations (social anxiety) or by thought of having a panic attack: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			else:
				fp_w.write('-2') #-2 for missing
				
			#OCD: Does the patient struggle with repetitive unwanted thoughts or behaviors for at least one hour per day: Uncertain
			fp_w.write(',')
			if(str(data).find('OCD: Does the patient struggle with repetitive unwanted thoughts or behaviors for at least one hour per day: Uncertain')>0):
				#fp_w.write('Uncertain')
				fp_w.write('-1')
			elif(str(data).find('OCD: Does the patient struggle with repetitive unwanted thoughts or behaviors for at least one hour per day: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('OCD: Does the patient struggle with repetitive unwanted thoughts or behaviors for at least one hour per day: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
				
			#Pickls at skin and cutivels when under stress.OBSESSIVE COMPULSIVE SPECTRUM DISORDERS: Does the patient have other repetitive, unwanted thoughts or behaviors that are non-functional and difficult to stop (e.g. excessive preoccupation with appearance, hairpulling/skin picking, motor or vocal tics): No
			fp_w.write(',')
			if(str(data).find('Pickls at skin and cutivels when under stress.OBSESSIVE COMPULSIVE SPECTRUM DISORDERS: Does the patient have other repetitive, unwanted thoughts or behaviors that are non-functional and difficult to stop (e.g. excessive preoccupation with appearance, hairpulling/skin picking, motor or vocal tics): No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('Pickls at skin and cutivels when under stress.OBSESSIVE COMPULSIVE SPECTRUM DISORDERS: Does the patient have other repetitive, unwanted thoughts or behaviors that are non-functional and difficult to stop (e.g. excessive preoccupation with appearance, hairpulling/skin picking, motor or vocal tics): Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
				
				
			#ADHD: Does the patient have longstanding problems sustaining their attention in activities that are of mediocre interest to them: No
			fp_w.write(',')
			if(str(data).find('ADHD: Does the patient have longstanding problems sustaining their attention in activities that are of mediocre interest to them: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('ADHD: Does the patient have longstanding problems sustaining their attention in activities that are of mediocre interest to them: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
				
			#PTSD: Does the patient experience trauma related flashbacks or recurrent dreams/nightmares: No
			fp_w.write(',')
			if(str(data).find('PTSD: Does the patient experience trauma related flashbacks or recurrent dreams/nightmares: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('PTSD: Does the patient experience trauma related flashbacks or recurrent dreams/nightmares: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
				
			#PTSD: Does the patient feel themselves getting very upset whenever they are reminded of their traumatic experience: No
			fp_w.write(',')
			if(str(data).find('PTSD: Does the patient feel themselves getting very upset whenever they are reminded of their traumatic experience: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('PTSD: Does the patient feel themselves getting very upset whenever they are reminded of their traumatic experience: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
			
			#EATING DISORDERS: Has the patient had periods of time during which they were concerned about eating or their weight: Uncertain
			fp_w.write(',')
			if(str(data).find('EATING DISORDERS: Has the patient had periods of time during which they were concerned about eating or their weight: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('EATING DISORDERS: Has the patient had periods of time during which they were concerned about eating or their weight: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			elif(str(data).find('EATING DISORDERS: Has the patient had periods of time during which they were concerned about eating or their weight: Uncertain')>0):
				#fp_w.write('Uncertain')
				fp_w.write('-1')
			else:
				fp_w.write('-2') #-2 for missing
				
			#EATING DISORDERS: Does the patient think they have an eating disorder: No
			fp_w.write(',')
			if(str(data).find('EATING DISORDERS: Does the patient think they have an eating disorder: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('EATING DISORDERS: Does the patient think they have an eating disorder: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			elif(str(data).find('EATING DISORDERS: Does the patient think they have an eating disorder: Uncertain')>0):
				#fp_w.write('Uncertain')
				fp_w.write('-1')
			else:
				fp_w.write('-2') #-2 for missing
			
			#DEMENTIA: Has anyone told the patient they are concerned the patient has memory problems: No
			fp_w.write(',')
			if(str(data).find('DEMENTIA: Has anyone told the patient they are concerned the patient has memory problems: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('DEMENTIA: Has anyone told the patient they are concerned the patient has memory problems: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
				
			
			#DEMENTIA: Does the patient have trouble learning new information: No
			fp_w.write(',')
			if(str(data).find('DEMENTIA: Does the patient have trouble learning new information: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('DEMENTIA: Does the patient have trouble learning new information: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
				
			
			#COMPLICATED GRIEF: Has it been more than 6 months since the loss of a loved one, and does grief continue to significantly interfere with the patients daily living: No
			fp_w.write(',')
			if(str(data).find('COMPLICATED GRIEF: Has it been more than 6 months since the loss of a loved one, and does grief continue to significantly interfere with the patients daily living: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('COMPLICATED GRIEF: Has it been more than 6 months since the loss of a loved one, and does grief continue to significantly interfere with the patients daily living: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
				
			
			#Alcohol Use: How often did you have a drink containing alcohol in the past year: Monthly or less (1 point)
			fp_w.write(',')
			
			if(str(data).find('Alcohol Use: How often did you have a drink containing alcohol in the past year: Never (0 Points)')>0):
				fp_w.write('0')
			elif(str(data).find('Alcohol Use: How often did you have a drink containing alcohol in the past year: Monthly or less (1 point)')>0):
				fp_w.write('1')
			elif(str(data).find('Alcohol Use: How often did you have a drink containing alcohol in the past year: Two to four times a month (2 points)')>0):
				fp_w.write('2')
			else:
				fp_w.write('-2') #-2 for missing
				
			
			#Marijuana: No
			fp_w.write(',')
			if(str(data).find('Marijuana: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('Marijuana: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
				
			
			#Cocaine: No
			fp_w.write(',')
			if(str(data).find('Cocaine: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('Cocaine: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
			
			#Sedative-Hypnotics: No
			fp_w.write(',')
			if(str(data).find('Sedative-Hypnotics: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('Sedative-Hypnotics: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
				
			#Stimulants: No
			fp_w.write(',')
			if(str(data).find('Stimulants: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('Stimulants: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
				
			#Opiates: No
			fp_w.write(',')
			if(str(data).find('Opiates: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('Opiates: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
				
			#Hallucinogens: No
			fp_w.write(',')
			if(str(data).find('Hallucinogens: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('Hallucinogens: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
				
			#Prescription medications for non-medical purposes: No
			fp_w.write(',')
			if(str(data).find('rescription medications for non-medical purposes: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('rescription medications for non-medical purposes: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
				
			#add column names from here
			#ReadingLearning Disabilities: No
			fp_w.write(',')
			if(str(data).find('ReadingLearning Disabilities: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('ReadingLearning Disabilities: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
				
			#Employment Currently employed: No
			fp_w.write(',')
			if(str(data).find('Employment Currently employed: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('Employment Currently employed: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
				
			#Financial Stress: No
			fp_w.write(',')
			if(str(data).find('Financial Stress: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('Financial Stress: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
				
			#Does patient feel safe in current living situation: Yes
			fp_w.write(',')
			if(str(data).find('Does patient feel safe in current living situation: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('Does patient feel safe in current living situation: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
				
			#Is Patient at risk of losing current housing: Yes
			fp_w.write(',')
			if(str(data).find('Is Patient at risk of losing current housing: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('Is Patient at risk of losing current housing: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
				
			#Hx of Military Service: No
			fp_w.write(',')
			if(str(data).find('Hx of Military Service: No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('Hx of Military Service: Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
				
			#normal-Mental Status Exam Was the exam performed? (If not, indicate reason): Yes
			fp_w.write(',')
			if(str(data).find('normal-Mental Status Exam Was the exam performed? (If not, indicate reason): No')>0):
				#fp_w.write('No')
				fp_w.write('0')
			elif(str(data).find('normal-Mental Status Exam Was the exam performed? (If not, indicate reason): Yes')>0):
				#fp_w.write('Yes')
				fp_w.write('1')
			else:
				fp_w.write('-2') #-2 for missing
			
			#Divorce
			fp_w.write(',')
			if(str(data).find('Divorce')>0 or str(data).find('divorce')>0):
				
				fp_w.write('1')
			else:
				fp_w.write('0') #-2 for missing
			
			#all encodings
			m_encoding(['Effexor','Effexor'],data,fp_w)
			m_encoding(['Suicidal','Suicidal','Suicide','suicide'],data,fp_w)
			m_encoding(['hypomani','Hypomani'],data,fp_w)
			m_encoding(['bupropion','Bupropion'],data,fp_w)
			m_encoding(['QHS'],data,fp_w)
			m_encoding(['Admission','Signing in the patient','Sign in', 'Baker act', 'Hospitalization','Hospitalized','ER','Emergency Room','Sectioned','Section','Committed','Court commitment','Placement','Institutionalize','Institutionalization','hospital','center'],data,fp_w)
			m_encoding(['Hurt themselves','Hurt others','Homicide','Attempt Suicide','Progression of illness','Chronicity of mental illness','Inability to take care of self','Homelessness','Unemployment','On disability','Social Isolation','Estrangement','Disenfranchised'],data,fp_w)
			m_encoding(['opiate'],data,fp_w)
			m_encoding(['poly-substance'],data,fp_w)
			m_encoding(['toxicology'],data,fp_w)
			#from here
			
			m_encoding(['single'],data,fp_w)
			m_encoding(['white'],data,fp_w)
			m_encoding(['post-traumatic'],data,fp_w)
			m_encoding(['stress disorder'],data,fp_w)
			m_encoding(['anxiety'],data,fp_w)
			m_encoding(['bulimia'],data,fp_w)
			#nervosa
			m_encoding(['nervosa'],data,fp_w)
			#endometriosis
			m_encoding(['endometriosis'],data,fp_w)
			#Suboxone
			m_encoding(['Suboxone'],data,fp_w)
			#cocaine
			m_encoding(['cocaine'],data,fp_w)
			#crack cocaine
			m_encoding(['crack cocaine'],data,fp_w)
			#illicit
			m_encoding(['illicit'],data,fp_w)
			#Percocet
			m_encoding(['Percocet'],data,fp_w)
			#oxycodone
			m_encoding(['oxycodone'],data,fp_w)
			#Dilaudid
			m_encoding(['Dilaudid'],data,fp_w)
			#violence
			m_encoding(['violence'],data,fp_w)
			#suicide
			m_encoding(['suicide'],data,fp_w)
			#self-injurious
			m_encoding(['self-injurious'],data,fp_w)
			#sexual trauma
			m_encoding(['sexual trauma'],data,fp_w)
			#anxious
			m_encoding(['anxious'],data,fp_w)
			# drive, driving
			m_encoding(['drive', 'driving'],data,fp_w)
			#seizures
			m_encoding(['seizures'],data,fp_w)
			#firearms
			m_encoding(['firearms'],data,fp_w)
			#addiction
			m_encoding(['addiction','addict','addicted'],data,fp_w)
			#arrest, jail, cop, AA
			m_encoding(['arrest', 'jail', 'cop', 'AA'],data,fp_w)
			#Recommendations / Plan Level of Care: Outpatient
			m_encoding(['Recommendations / Plan Level of Care: Outpatient'],data,fp_w)
			#Addiction Treatment
			m_encoding(['Addiction Treatment'],data,fp_w)
			#Medication Treatment
			m_encoding(['Medication Treatment'],data,fp_w)
			#Cognitive Behavioral Therapy (CBT)
			m_encoding(['Cognitive Behavioral Therapy (CBT)'],data,fp_w)
			
			#Group Therapy
			m_encoding(['Group Therapy'],data,fp_w)
			#psychopharm
			m_encoding(['Group Therapy'],data,fp_w)
			
			#Psychiatric History Hx of Inpatient Treatment: No
			fp_w.write(',')
			if(str(data).find('Psychiatric History Hx of Inpatient Treatment: No')>0):
				
				fp_w.write('0')
			elif(str(data).find('Psychiatric History Hx of Inpatient Treatment: Yes')>0):
				fp_w.write('1') #-2 for missing
			else:
				fp_w.write('-2') #-2 for missing
			
			#Outpatient Treatment:
			
			fp_w.write(',')
			if(str(data).find('Outpatient Treatment: No')>0):
				
				fp_w.write('0')
			elif(str(data).find('Outpatient Treatment: Yes')>0):
				fp_w.write('1') #-2 for missing
			else:
				fp_w.write('-2') #-2 for missing
			
			#support group
			m_encoding(['support group'],data,fp_w)
			#case mgt services
			m_encoding(['case mgt services'],data,fp_w)
			#therapy
			m_encoding(['therapy'],data,fp_w)
			
			#Does patient have chronic high risk:
			fp_w.write(',')
			if(str(data).find('Does patient have chronic high risk: No')>0):
				
				fp_w.write('0')
			elif(str(data).find('Does patient have chronic high risk: Yes')>0):
				fp_w.write('1') #-2 for missing
			else:
				fp_w.write('-2') #-2 for missing
			
			#Hx of Outpatient Treatment: Yes
			fp_w.write(',')
			if(str(data).find('Does patient have chronic high risk: No')>0):
				
				fp_w.write('0')
			elif(str(data).find('Hx of Outpatient Treatment: Yes')>0):
				fp_w.write('1') #-2 for missing
			else:
				fp_w.write('-2') #-2 for missing
				
			#Suicidal Behavior Hx of Suicidal Behavior: No
			fp_w.write(',')
			if(str(data).find('Suicidal Behavior Hx of Suicidal Behavior: No')>0):
				
				fp_w.write('0')
			elif(str(data).find('Suicidal Behavior Hx of Suicidal Behavior: Yes')>0):
				fp_w.write('1') #-2 for missing
			else:
				fp_w.write('-2') #-2 for missing
			
			#Hx of Non Suicidal Self Injurious Behavior: No
			fp_w.write(',')
			if(str(data).find('Hx of Non Suicidal Self Injurious Behavior: No')>0):
				
				fp_w.write('0')
			elif(str(data).find('Hx of Non Suicidal Self Injurious Behavior: Yes')>0):
				fp_w.write('1') #-2 for missing
			else:
				fp_w.write('-2') #-2 for missing
			
			#Violent Behavior Hx of Violent Behavior:
			fp_w.write(',')
			if(str(data).find('Violent Behavior Hx of Violent Behavior: No')>0):
				
				fp_w.write('0')
			elif(str(data).find('Violent Behavior Hx of Violent Behavior: Yes')>0):
				fp_w.write('1') #-2 for missing
			else:
				fp_w.write('-2') #-2 for missing
			
			#Is the patient being referred for further medical or neurological assessments (Please specify): No
			fp_w.write(',')
			if(str(data).find('Is the patient being referred for further medical or neurological assessments (Please specify): No')>0):
				
				fp_w.write('0')
			elif(str(data).find('Is the patient being referred for further medical or neurological assessments (Please specify): Yes')>0):
				fp_w.write('1') #-2 for missing
			else:
				fp_w.write('-2') #-2 for missing
			
			#add labels from here
			#Did patient endorse thoughts of harm to self or others during today's session: No
			fp_w.write(',')
			if(str(data).find('Did patient endorse thoughts of harm to self or others during today\'s session: No')>0):
				
				fp_w.write('0')
			elif(str(data).find('Did patient endorse thoughts of harm to self or others during today\'s session: Yes')>0):
				fp_w.write('1') #-2 for missing
			else:
				fp_w.write('-2') #-2 for missing
			
			#History of drug use: No
			fp_w.write(',')
			if(str(data).find('History of drug use: No')>0):
				
				fp_w.write('0')
			elif(str(data).find('History of drug use: Yes')>0):
				fp_w.write('1') #-2 for missing
			else:
				fp_w.write('-2') #-2 for missing
			
			#Referral/Treatment Needed: No
			fp_w.write(',')
			if(str(data).find('Referral/Treatment Needed: No')>0):
				
				fp_w.write('0')
			elif(str(data).find('Referral/Treatment Needed: Yes')>0):
				fp_w.write('1') #-2 for missing
			else:
				fp_w.write('-2') #-2 for missing
			
			#History of physical fights when drinking and prior to service
			fp_w.write(',')
			if(str(data).find('History of physical fights when drinking and prior to service: No')>0):
				
				fp_w.write('0')
			elif(str(data).find('History of physical fights when drinking and prior to service: Yes')>0):
				fp_w.write('1') #-2 for missing
			else:
				fp_w.write('-2') #-2 for missing
			
			#add
			m_encoding(['sober','sobrieti'],data,fp_w)
			#detox
			m_encoding(['detox'],data,fp_w)
			#iop
			m_encoding(['iop','intensive outpatient program'],data,fp_w)
			#program
			m_encoding(['program','service'],data,fp_w)
			#depend
			m_encoding(['depend'],data,fp_w)
			#none
			m_encoding(['none','no','nwl','NWL','No'],data,fp_w)
			#No
			m_encoding(['No'],data,fp_w)
			#yes
			m_encoding(['Yes'],data,fp_w)
			
			#Independent
			m_encoding(['Independent'],data,fp_w)
			#psychotheraphy
			m_encoding(['psychotheraphy'],data,fp_w)
			#couples theraphy
			m_encoding(['couples theraphy'],data,fp_w)
			#group thearphy
			m_encoding(['group theraphy'],data,fp_w)
			#short-term thearphy
			m_encoding(['short-term theraphy'],data,fp_w)
			#cancer thearphy
			m_encoding(['cancer theraphy'],data,fp_w)
			#pharmacotheraphy
			m_encoding(['pharmacotheraphy'],data,fp_w)
			#aganist therapy
			m_encoding(['aganist therapy'],data,fp_w)
			#family theraphy
			m_encoding(['family theraphy'],data,fp_w)
			#sleep 
			m_encoding(['sleep'],data,fp_w)
			#insomnia
			m_encoding(['insomnia'],data,fp_w)
			#moniter
			m_encoding(['moniter'],data,fp_w)
			#motivated
			m_encoding(['motivated'],data,fp_w)
			
			#new features
			#ADHD2
			m_encoding(['Hypertensive','hyperactivity','academic','learning','deficit'],data,fp_w)
			#mood
			m_encoding(['mood'],data,fp_w)
			#depression
			m_encoding(['depression','depressive'],data,fp_w)
			#cognitive
			m_encoding(['cognitive'],data,fp_w)
			#cyclic disorder
			m_encoding(['cyclic disorder'],data,fp_w)
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
				
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			
			


				
					
			fp_w.write('\n')

	fp_w.close()
			

file_name1="C:/Users/ThinkPad/Desktop/Healthcare-I2B2/track_2_training/training/"
file_name2=file_name1+"annotated_by_one/"
output_name1="C:/Users/ThinkPad/Desktop/Healthcare-I2B2/script/dataAnnotatedBy2_v15.csv"
output_name2="C:/Users/ThinkPad/Desktop/Healthcare-I2B2/script/dataAnnotatedBy1_v15.csv"
			
process(file_name1,output_name1)
process(file_name2,output_name2)
