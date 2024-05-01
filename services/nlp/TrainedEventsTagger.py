import re
import numpy as np
import pickle 
#from gensim.models import Word2Vec


# trained events tagger class that takes in pretrained parameters 
class TrainedEventsTagger:
  def __init__(self, pkl_file):
    with open(pkl_file, 'rb') as f:
      model_data = pickle.load(f)
    
    #print("model loaded")

    self.keyword_embeddings = model_data['keyword_embeddings']
    self.word_vectors = model_data['word_vectors']
    self.V = model_data['V']
    self.W1 = model_data['W1']
    self.topic_names_dict = model_data['topic_names_dict']
    self.custom_keywords_dict = model_data['custom_keywords_dict']
    self.keywords_to_visible_tags = model_data['keywords_to_visible_tags']
    #self.keywords = model_data['keywords']

    #print("done with other variables")

    #self.word2vec_model = Word2Vec.load(word2vec_model)




  # code that cleans events
  def clean_event(self, desc):
    clean_desc = desc.lower()
    clean_desc = re.sub('[^a-zA-Z]', ' ', clean_desc)
    clean_desc=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",clean_desc)
    clean_desc=re.sub("(\\d|\\W)+"," ",clean_desc)
    clean_desc = clean_desc.replace('\n', '')
    clean_desc = clean_desc.replace('\Terminate\\', '\n')
    clean_desc = clean_desc.replace('Subject: ', '')
    return clean_desc

  # tags events
  def tag(self, event):
    # all the helper functions are subfunctions so that we only need one thing

    # redundant, but this is the same code that we use to clean the events
    def clean_event(desc):
      import re # !!!!!
      clean_desc = desc.lower()
      clean_desc = re.sub('[^a-zA-Z]', ' ', clean_desc)
      clean_desc=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",clean_desc)
      clean_desc=re.sub("(\\d|\\W)+"," ",clean_desc)
      clean_desc = clean_desc.replace('\n', '')
      clean_desc = clean_desc.replace('\Terminate\\', '\n')
      clean_desc = clean_desc.replace('Subject: ', '')
      return clean_desc

    # gets similarities between keywords
    def get_keyword_similarities(event):
      event_description = clean_event(event).split()

      # calculate similarity between event description and each keyword
      similarity_scores = {}
      for keyword, embedding in self.keyword_embeddings.items(): #!!!!!
        keyword_similarity = []
        for word in event_description:
          if word in self.word_vectors.key_to_index: #!!!!!
            word_embedding = self.word_vectors.get_vector(word)
            similarity = self.word_vectors.cosine_similarities(embedding, [word_embedding])
            keyword_similarity.append(max(similarity))
            if keyword_similarity:
              similarity_scores[keyword] = max(keyword_similarity)

      # return the top keywords and their probabilities
      sorted_keywords = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
      top_keywords = sorted_keywords[:10]
      return top_keywords

    # vectorize a doc for topic modeling
    def vectorize_doc(cleaned_doc):
      word_to_index = {word: index for index, word in enumerate(self.V)} #!!!!
      word_counts = {}
      words = cleaned_doc.split()
      for word in words:
        if word in word_to_index:
          word_index = word_to_index[word]
          word_counts[word_index] = word_counts.get(word_index, 0) + 1

      document_vector = [word_counts.get(index, 0) for index in range(len(self.V))]
      return document_vector

    # list topics above a certain pmi proportion for topic modeling
    def list_topics_above_proportion(topic_distribution, threshold):
      topics_above_threshold = []

      for topic_index, proportion in enumerate(topic_distribution):
        if proportion > threshold:
            topics_above_threshold.append(topic_index + 1)
      return topics_above_threshold

    # get the topic numbers given a pmi threshold
    def get_topic_numbers(cleaned_doc, threshold=0.5):
      import numpy as np
      document_vector = vectorize_doc(cleaned_doc)
      document_topic_distribution = np.dot(document_vector, self.W1) #!!!!
      topics_above_threshold = list_topics_above_proportion(document_topic_distribution, threshold)
      topics_sorted_by_proportion = sorted(topics_above_threshold, key=lambda topic_index: document_topic_distribution[topic_index - 1], reverse=True)
      return topics_sorted_by_proportion

    # map the topics to the tags
    def get_topics(doc):
      cleaned_doc = clean_event(doc)
      topic_numbers = get_topic_numbers(cleaned_doc)
      tags = [self.topic_names_dict.get(topic) for topic in topic_numbers] #!!!
      if tags == []:
        return []
      else:
        return tags

    # main function
    tags = []

    # tag based on keyword similarity
    keyword_similarities = get_keyword_similarities(event)
    for (keyword, score) in keyword_similarities:
      if score < 0.97:
        break
      else:
        tags.append(keyword)

    #print(tags)

    # define a set of custom keywords for tagging
    clean_event_desc = clean_event(event)


    for tag, lst in self.custom_keywords_dict.items():
      added_tag = False
      for word in lst:
        if word in clean_event_desc:
          added_tag = True
          tags.append(tag)
          break
      # if we already added the tag no need to continue looking through the words
      if added_tag == True:
        continue

    # get the topics and add them to the set of tags
    topics = get_topics(event)

    all_tags = tags + topics

    # transforming into a set of visible tags
    visible_tags = set()

    for tag in all_tags:
      visible_tags.update(self.keywords_to_visible_tags.get(tag, []))

    return list(visible_tags)



