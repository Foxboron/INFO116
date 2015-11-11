

wittgenstein = open("wittgenstein.txt").read().split("\n")



# Prepare soites
import re
sorites = open("sorites.txt").read().strip()
sorites = re.split("[0-9]\. ",sorites)




# rediscover
rediscover = open("rediscover.txt").read().split("\n")


def get_topics(f):

    import numpy as np  # a conventional alias
    import sklearn.feature_extraction.text as text
    from sklearn import decomposition
    vectorizer = text.CountVectorizer(input='content', stop_words='english', min_df=4)

    dtm = vectorizer.fit_transform(f).toarray()

    vocab = np.array(vectorizer.get_feature_names())


    num_topics = len(f)-1

    num_top_words = 60

    clf = decomposition.NMF(n_components=num_topics, random_state=1)


    doctopic = clf.fit_transform(dtm)

    topic_words = []

    for topic in clf.components_:
        word_idx = np.argsort(topic)[::-1][0:num_top_words]
        topic_words.append([vocab[i] for i in word_idx])



    doctopic = doctopic / np.sum(doctopic, axis=1, keepdims=True)


    novel_names = []

    for n,text in enumerate(f):
        novel_names.append(n)


    novel_names = np.asarray(novel_names)

    doctopic_orig = doctopic.copy()

# use method described in preprocessing section
    num_groups = len(set(novel_names))

    doctopic_grouped = np.zeros((num_groups, num_topics))

    for i, name in enumerate(sorted(set(novel_names))):
        doctopic_grouped[i, :] = np.mean(doctopic[novel_names == name, :], axis=0)


    doctopic = doctopic_grouped
    return topic_words



def print_topics(topic_words):
    for t in range(len(topic_words)):
        print("Topic {}: {}".format(t, ' '.join(topic_words[t][:15])))


witt_topics = get_topics(wittgenstein)
print("Main text")
print_topics(witt_topics)




sorites_topics= get_topics(sorites)
print("Sorites text")
print_topics(sorites_topics)

rediscover_topcs = get_topics(rediscover)
print("Rediscover text")
print_topics(rediscover_topcs)




