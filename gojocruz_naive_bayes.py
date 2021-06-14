'''
* Gojo Cruz, Jamlech Iram N.
* CMSC170 Exercise 05: Naive Bayes
* Exercise for Spam Filtering using Naive Bayes Classifier
* October 30, 2020
'''

from decimal import *	# Decimal function
import os, os.path		# File path
import string 			# String methods
import sys				# System exit
from collections import Counter # Counts unique words


# change this if working with different directory
spam_dir = "data\\spam"
ham_dir = "data\\ham"
classify_dir = "data\\classify"


# -----------------------------------------------------------------------------------------
# Reading the file and tokenize
# the words in the list
#
# @param:	name of file
# -----------------------------------------------------------------------------------------
def read_file(filename):
	wordlist = list()
	try:
		infile = open(filename, "r", encoding = 'iso-8859-1')
	except:
		print("File not found")
		sys.exit()
	for lines in infile:
		for word in lines.split():
			wordlist.append(word)
	#infile.close()
	return(wordlist)


# -----------------------------------------------------------------------------------------
# Word cleaning and returns the
# final list of words
#
# @param:	list of acquired words from
# 			reading the file
# -----------------------------------------------------------------------------------------
def clean(wordlist):
	finallist = list()
	for word in wordlist:
		fwlist = ""
		for char in word:
			if(char in string.ascii_letters or char in string.digits):
				fwlist = fwlist + char
			else:
				continue
		finallist.append(fwlist)

	#remove unecessary blank items in the list
	finallist = [w for w in finallist if w != '']
	#convert every word to lowercase
	finallist = [w.lower() for w in finallist]
	#sort the list in ascending order
	finallist = sorted(finallist)

	return(finallist)


# -----------------------------------------------------------------------------------------
# Counts the number of unique words
# Returns the dictionary of words and
# their frequency
#
# @param:	list of cleaned words
# -----------------------------------------------------------------------------------------
def count(finallist):
	return Counter(finallist)


# -----------------------------------------------------------------------------------------
# Writing in the file
#
# @params:	
#	filename - name of file		
#	dsize_spam - dictionary size of spam BOW		
#	dsize_ham - dictionary size of ham BOW	
#	tsize_spam - total number of words for spam BOW
#	tsize_ham - total number of words for ham BOW
#	classified_email - tuple of email name, classification, and probability			
# -----------------------------------------------------------------------------------------
def write_file(filename, dsize_spam, dsize_ham, tsize_spam, tsize_ham, classified_email):
	outfile = open(filename, "w")

	for line in classified_email:
		for i in line:
			outfile.write(str(i)+" ")
		outfile.write("\n")

	outfile.write("\nHAM\n")
	outfile.write("Dictionary Size: " + str(dsize_ham))
	outfile.write("\n")
	outfile.write("Total Number of Words: " + str(tsize_ham))
	outfile.write("\n")

	outfile.write("\nSPAM\n")
	outfile.write("Dictionary Size: " + str(dsize_spam))
	outfile.write("\n")
	outfile.write("Total Number of Words: " + str(tsize_spam))

	outfile.close()




# -----------------------------------------------------------------------------------------
# Returns the probability of spam and ham
# Formula:
#	P(spam) = count(spam) / count(spam U ham)
#	P(ham) = count(ham) / count(spam U ham)
# -----------------------------------------------------------------------------------------
def prob_of_msg():
	spam_count = (len([name for name in os.listdir(spam_dir) if os.path.isfile(os.path.join(spam_dir, name))]))
	ham_count = (len([name for name in os.listdir(ham_dir) if os.path.isfile(os.path.join(ham_dir, name))]))
	prob_spam = Decimal(spam_count) / (Decimal(spam_count) + Decimal(ham_count))
	prob_ham = Decimal(ham_count) / (Decimal(spam_count) + Decimal(ham_count))
	return (prob_spam, prob_ham)


# -----------------------------------------------------------------------------------------
# Returns the denominator to be used in getting P(message|Spam) or P(message|Ham)
# Formula:
#	P(w|spam) = count(w in spam) / count(total no. of words in spam)
#	P(w|ham) = count(w in ham) / count(total no. of words in ham)
# @params:
#	tsize - total no. of words in BOW
#	wordcount - dictionary of unique words with their corresponding frequency
#	word = the word to be computed
# -----------------------------------------------------------------------------------------
def prob_word_class(tsize, wordcount, word):
	if word in wordcount: 
		return Decimal(wordcount.get(word)) / Decimal(tsize)
	return Decimal(0)


# -----------------------------------------------------------------------------------------
# Returns the P(message|Spam) or P(message|Ham)
# Formula:
#	P(message|Spam) = P(w0|Spam) * ... * P(wn|Spam)
#	P(message|Ham) = P(w0|Ham) * ... * P(wn|Ham)
# @params:
#	tsize - total no. of words in BOW
#	wordcount - dictionary of unique words with their corresponding frequency
#	classifylist = dictionary of words in the classify BOW
# -----------------------------------------------------------------------------------------
def prob_msg_class(tsize, wordcount, classifylist):
	p_msg_class = 1
	for key in classifylist:
		p_msg_class = Decimal(p_msg_class) * (prob_word_class(tsize, wordcount, key))
	return (p_msg_class)


# -----------------------------------------------------------------------------------------
# Returns the P(Spam|message). If denominator results to 0, return UNDEFINED. Else, return 1.
# Formula:
#	P(Spam|message) = P(message|Spam) P(Spam) / P(message)
#	where, P(message) = P(message|Spam) P(Spam) + P(message|Ham) P(Ham)
# @params:
#	p_msg_spam = probability of message given spam
#	p_msg_ham = probability of message given ham
#	p_spam = probability of spam
#	p_ham = probability of ham
# -----------------------------------------------------------------------------------------
def prob_spam_msg(p_msg_spam, p_msg_ham, p_spam, p_ham):
	denominator = ((Decimal(p_msg_spam) * Decimal(p_spam)) + (Decimal(p_msg_ham) * Decimal(p_ham)))
	if denominator > 0:
		p_spam_msg = (Decimal(p_msg_spam) * Decimal(p_spam)) / Decimal(denominator)
	else:
		p_spam_msg = "UNDEFINED"
	return (p_spam_msg)


# -----------------------------------------------------------------------------------------
# Returns the classification of the email, given the probability
# Threshold is set to 50%
# @params:
#	p_spam_msg = probability of spam given message
# -----------------------------------------------------------------------------------------
def classify_email(p_spam_msg):
	if p_spam_msg == "UNDEFINED":
		return ""
	else:
		probability = p_spam_msg * 100
		if(probability < 50):
			return "HAM"
		else:
			return "SPAM"


# Main function
def main():

	print("Making bag of words...")
	wordlist_spam = list()
	wordlist_ham = list()

	# Read and tokenize words in spam and ham
	for i in os.listdir(spam_dir):
		wordlist_spam_tmp = read_file(spam_dir+"\\"+str(i))
		wordlist_spam.extend(wordlist_spam_tmp)

	for i in os.listdir(ham_dir):
		wordlist_ham_tmp = read_file(ham_dir+"\\"+str(i))
		wordlist_ham.extend(wordlist_ham_tmp)

	# Clean words
	finallist_spam = clean(wordlist_spam)
	finallist_ham = clean(wordlist_ham)

	# Count the words
	wordcount_spam = count(finallist_spam)
	wordcount_ham = count(finallist_ham)

	# Size of dictionary is the length of list (dictionary) with unique words
	dsize_spam = len(wordcount_spam)
	dsize_ham = len(wordcount_ham)
	
	# Total number of words from the original word list
	tsize_spam = len(finallist_spam)
	tsize_ham = len(finallist_ham)


	classified_email = list()

	# Make bag of words for each classify email
	print("Classifying emails...")
	for email in os.listdir(classify_dir):
		wordlist_tmp = read_file(classify_dir+"\\"+str(email))
		finallist_tmp = clean(wordlist_tmp)
		wordcount_tmp = count(finallist_tmp)

		# P(Spam) and P(Ham)
		p_spam, p_ham = prob_of_msg()

		# P(message|Spam) && P(message|Ham)
		p_msg_spam = prob_msg_class(tsize_spam, wordcount_spam, wordcount_tmp)
		p_msg_ham = prob_msg_class(tsize_ham, wordcount_ham, wordcount_tmp)

		# P(Spam|message)
		p_spam_msg = prob_spam_msg(p_msg_spam, p_msg_ham, p_spam, p_ham)

		# Email classification
		classification = classify_email(p_spam_msg)

		# List which contains a tupple of the email name, classification, and its probability
		classified_email.append((str(email), "\t", classification, "\t", p_spam_msg))

	# Write the tuple
	write_file("classify.out", dsize_spam, dsize_ham, tsize_spam, tsize_ham, classified_email)
	print("Output succefully written to classify.out")
	



# Invoke main function to execute program
main()