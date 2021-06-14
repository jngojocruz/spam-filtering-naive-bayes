# Exercise for Spam Filtering using Naive Bayes Classifier

## Task
Create a program that will take message files and classify them as spam or ham using a naive bayes classifier.

## Input
Datasets for Spam and Ham are provided in separate folders for this exercise. Another folder for the messages to be classified is also given.

## Required Output
The output of the program is a text file named classify.out which contains the following information per line
- the filename of the file to be classified
- classification of the message in the file
- computed probability

## Reminders
- Naming convention for exercise: surname_naive_bayes.
- Only Python or Java can be used for the exercise.
- Do not forget to put a journal in your README file in Github.
- Lastly, Honor and Excellence.

## Journal
#### The programming language used
Python
#### Problems encountered
I've been struggling with the formulas for probabilities and their proper return values. Division by zero, or very small decimal, also added to these problems. I am a bit confused about the expected output of the program. I am also a bit unsure of what I did in handling very small values in getting the probability of spam given message.
#### How the problems were resolved
I tried to add filters that will determine whether the values are near zero. I check first if the denominator is flat zero, and if so, the program will return "undefined". Else, it will try to compute the probability. If the case is not possible due to the value being very small, it will return 1.
#### Learnings from the exercise
This exercise really needs some patience because aside from numerous data sets, the effort of debugging and analyzing the problem takes time. As I said from the lecture, I love to see how statistics and probability, and AI work together to do some cool stuff that is very useful.
