#!/usr/bin/python3

import shutil
import csv, time
import subprocess
import pandas as pd
from urllib.parse import urlparse

import unicodedata
import re

def slugify(value, allow_unicode=False):
	value = str(value)
	if allow_unicode:
		value = unicodedata.normalize('NFKC', value)
	else:
		value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
		value = re.sub(r'[^\w\s-]', '', value.lower())
	return re.sub(r'[-\s]+', '-', value).strip('-_')

def GetRegistrar(csv_file):
	datafr = pd.read_csv(csv_file, sep=";", quotechar='"')
	if 'WHOIS' not in datafr.columns:
		datafr['WHOIS'] = ""
	if "" in datafr.WHOIS.values:
		for index, row in datafr.iterrows():
			if datafr.loc[index, 'WHOIS'] == "":
				domain = DomainFromURL(row['URL'])
				bashCommand = f"whois {domain}"
				process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
				output, error = process.communicate()
				while 'Your connection limit exceeded.' in str(output):
					time.sleep(5)
					bashCommand = f'whois {domain}'
					process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
					output, error = process.communicate()
				datafr.loc[index, 'WHOIS'] = str(output).replace('\\n','\n')
		datafr.to_csv(csv_file)
	return datafr

def DomainFromURL(url):
	domain = urlparse(url).netloc
	domain = domain.split('.',1)
	try:
		if '.' in domain[1]:
			if domain[1].split('.')[0] not in ['co','com','gob','org']:	#domeny typu bbc.co.uk
				domain = domain[1]
			else: domain = '.'.join(domain)
		else: domain =  '.'.join(domain)
	except: pass
	return domain

def FindMatches(reg, dataframe):
	df_reg = dataframe[dataframe['WHOIS'].str.contains(reg.strip())]
	reg = slugify(reg)
	df_reg.drop(df_reg.columns.difference(['URL','CATEGORY','TYPE','SEVERITY']),1).to_csv(f'REGs/{reg}.csv')
	indexes_to_ignore = df_reg.index.values
	return list(indexes_to_ignore)

#shutil.copyfile('findings.csv', 'findings-sorted.csv')
df = GetRegistrar('findings.csv') 
to_ignore_list = []


with open('REGs/registrars.txt', 'r') as reg_file:
	registrars = reg_file.readlines()
	for reg in registrars:
		to_ignore_list = to_ignore_list + FindMatches(reg, df)
	df.loc[to_ignore_list, 'ignore'] = "true"

registrars = []
for i, row in df.iterrows():
	print(row['ignore'])
	if df.at[i, 'ignore'] != "true":
		print(row['WHOIS'])
		reg = input('Who is the registrar?\n')
		registrars.append(reg)
		to_ignore = FindMatches(reg, df)
		df.loc[to_ignore, 'ignore'] = 'true'

with open('REGs/registrars.txt', 'a+') as reg_file:
	reg_file.writelines(registrars)
