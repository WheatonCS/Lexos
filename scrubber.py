import string, re

def scrubber(text):
	text = re.sub('<[^<]+>', "", text)
	text = text.lower()
	text = text.translate(string.maketrans("",""), string.punctuation)
	return text