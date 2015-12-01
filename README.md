# TREC 2005 Ad Hoc Retrieval with SVD 

In this repo, I'm using the TREC 2005 training dataset as the training set for my [master's thesis project](https://github.com/santina/masterthesis) (this repo right now serves mainly as a back-up of my hopefully readable codes). The object of the master thesis is to see if we could use singular value decomposition on a document-term matrix to find similar **biomedical papers**. 

There are the steps I need to go through from text-mining biomedical literature before seeing the results, as summarized in this chart: 

![Work flow](/images/Textmining_flowchart.png)

Blue blocks indicate some kind of raw/intermediate/final data and green are the processes.  

# Problem

There are many choices along the way in the flow chart, such as choices of matrix and amount of information to include (abstract-only? full-text?). 

Would this TREC dataset help me figure those things out? Hopefully, but the dataset is quite small compare to the actual biomedical literature dataset I'm working with. I'll have to see if this experiment is valuable. 


# For more details on this dataset: 
[TREC 2005 Genomics Track Overview](http://trec.nist.gov/pubs/trec14/papers/GEO.OVERVIEW.pdf)

[Final protocol and objectives on TREC 2005 Genomics](http://skynet.ohsu.edu/trec-gen/2005protocol.html)

[Accessing TREC 2005 data](http://skynet.ohsu.edu/trec-gen/2005data.html)

[More info and other TREC Genomics Tracks](http://skynet.ohsu.edu/trec-gen/index.html)