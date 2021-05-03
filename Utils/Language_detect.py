from spacy_langdetect import LanguageDetector
import spacy
nlp = spacy.load('en')  
nlp.add_pipe(LanguageDetector(), name='language_detector', last=True) 

# Only One Language
text_content = "Er lebt mit seinen Eltern und seiner Schwester in Berlin."
doc = nlp(text_content) 
detect_language = doc._.language 
print(detect_language)

# Multiple Language text - 1
text_content = "How are you doing. Er lebt mit seinen Eltern und seiner Schwester in Berlin."
doc = nlp(text_content) 
detect_language = doc._.language 
print(detect_language)

# Multiple Language text - 2
text_content = " How are you doing. ola"
doc = nlp(text_content) 
detect_language = doc._.language 
print(detect_language)

