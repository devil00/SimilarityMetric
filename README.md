Requisites:
 python >= 2.7
 python package stemmer:
    Installation : pip install stemmer
OS: linux


Further upgradation,
 
 There is still a scope to upgrade the current approach of finidng similarity.
 One might go for tf-idf weighted model to obtain key vector, since, this model
 compute the frequencey distribution of a word in the document, it would
 impove the metric further.

 Specifically, the task is to find similarity amongst poems and poem are
 written wth some mood and sentiment. Therefore, I would rather prefer to apply
 semnatic analysis to compute the similarity metric.

 I can opt for LSA(Latent Semantic Analysis). This algorithm assumes that words 
 that are close in meaning will occur in similar pieces of text and it also
 takes into account the syntatic ambiguity which has it's oen advantages and
 disadvantages.







