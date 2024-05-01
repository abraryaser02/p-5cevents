from TrainedEventsTagger import TrainedEventsTagger


tagger = TrainedEventsTagger('events_tagger_model_parameters_new.pkl') 
print("model loaded")

tags = tagger.tag("Come talk to the Computer Science professors in the pannel for understanding computer science course registration")
print(tags)

tags2 = tagger.tag("Fellowship Information Dinner @ Frank Blue Room, Wed, 3/20 from 5:15 - 6:15 PM What exactly is a fellowship? How do you apply for one? When can you apply for one? Get your answers to these questions from the CDO Fellowship Advisor Jason Jeffrey")
print(tags2)