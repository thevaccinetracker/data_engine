import  string
from sklearn.metrics.pairwise import   cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus    import   stopwords

stopwords = stopwords.words('english')

sentance = [
    'Phase III',
    'Phase 2'
    # 'this is a foo bar sentence.',
    # 'this sentence is similar to foo bar sentence.',
    # 'this is another string, but it is not quite similar to have previous ones.',
    # 'i am also just another string.'
]

def clean_string(text):
    text = ''.join([word for word in text if word not in string.punctuation])
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stopwords])
    return text

cleaned = list(map(clean_string, sentance))

vectorizer = CountVectorizer().fit_transform(cleaned)
vectors = vectorizer.toarray()

csim = cosine_similarity(vectors)

def cosine_sim_vectors(vec1, vec2):
    vec1 = vec1.reshape(1,-1)
    vec2 = vec2.reshape(1,-1)
    return  cosine_similarity(vec1, vec2)[0][0]

print cosine_sim_vectors(vectors[0], vectors[1])

