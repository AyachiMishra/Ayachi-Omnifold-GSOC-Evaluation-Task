from omnifold_publication.core import OmniFoldResult

result = OmniFoldResult("multifold_sherpa.h5") # just ensure the dataset stays near your folder at the time of 

result.validate()

result.plot("pT_ll", bins=50)