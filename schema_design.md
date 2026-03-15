- "Why I structured it the way I did?":
    - Time invested on a dataset is an important factor. When a scientist thinks of using our dataset, he should be quick to dismiss our dataset if it does not align with his experiment. We don't want wasted efforts and time. This would also make it easier for scientists to trust on our proposed convention.
    - That is why i first added importatn specifics like process specifications, event selection criteria and software setup
    - Information after these (like observables' dictionary, weight normalisation and details about the weights) will only be needed if the scientist actually decides to use our dataset.




- I added a dictionary to decode the observable abbreviations along with its units. They can be published in the accompanying paper, but since we didn't do that and since this is so important hence i added it in the metadata

- "What i chose to include vs leave out and why?" :
    - Including information 
        - This is easy as we already discussed in gap_analysis.md what are the absolute essentials so that there are no misconceptions (to avoid loss of time and effort)
        - I also included Purpose of the dataset as it naturally would help anyone to understand what the dataset is for
        - Other information which was nice to include like observable_dictionary and weights_structure would help the scientist to easily know these and is just nice to have.

    - Excluding information:
        - The info about neural network training like hyperparameters, activation functions and other specifics are not that relevant here. They could be mentioned somewhere else but not really necessary/relevant here as not much harm can happen by not knowing this.
        - Excluded lower level details about the detector that got simulated like the scientist wouldn't really be interested in that full story, he just need to know the state

- "How I would expect a user who didn't run the original analysis to interact with this file?"

    - He would first understand the purpose of the dataset
    - If he decides to continue he would first get aware about all important information (before starting) like the process, event selection details, software details 
    - If after that he continues then he could read all factual information about the dataset like normalisation of weights, observables and weight info
    - Overall I think this much would suffice and shouldnt create mcuh problem....


