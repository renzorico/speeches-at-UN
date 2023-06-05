from textblob import TextBlob

sentence = "The sun was setting on the horizon, casting a warm golden glow over the tranquil meadow. Birds chirped their evening songs as a gentle breeze rustled the leaves of the trees. It was a picture-perfect scene, a moment frozen in time"

ngram_object = TextBlob(sentence)

ngrams = ngram_object.ngrams(n=2)
print(ngrams)
