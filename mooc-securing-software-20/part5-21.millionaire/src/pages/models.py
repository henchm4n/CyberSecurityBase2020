from django.db import models

# Create your models here.

# Storing this in a database is an overkill for this exercise,
# so let's cheat and just store the questions as a hardcoded dictionary.
questions = [
	{
		'name': 'Security',
		'id' : 1,
		'questions' :  [
			{
				'question': 'Python web framework is...',
				'answers': [
					'Django', 'Kill Bill', 'Pulp Fiction', 'Death Proof'
				],
				'correct': 0
			},
			{
				'question': 'XSS is...',
				'answers': [
					'Extra small shirt', 
					'Cross-site scripting',
				],
				'correct': 1
			}
		]
	},
	{
		'name': 'Biology',
		'id' : 2,
		'questions' :  [
			{
				'question': 'What is the airspeed velocity of an unladen swallow?',
				'answers': [
					'42', 'African or European?', 'Potato'
				],
				'correct': 1
			},
			{
				'question': 'The largest rodent in the world is...',
				'answers': [
					'Splinter', 'Wombat', 'Capybara', 'Chupacabra'
				],
				'correct': 2
			}
		]
	}
]
