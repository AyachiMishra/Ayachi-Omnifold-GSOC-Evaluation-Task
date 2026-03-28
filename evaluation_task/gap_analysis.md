# <center><u> Gap Analysis </u></center>
<!-- ctrl shift P: choose Markdown : Open Preview to the side (to open preview to the side)  --> 
- " What columns are present, and which are weights vs. observables vs. metadata? "
    -  Columns Present : 
        - The column names are present in **axis0** subfile of each of the .h5 files. 
        - The columns (in multifold.h5 file): 22 different observable columns, 1 weights_nominal column which is the actual column containing output weights of the omnifold algorithm (the unfolding),  columns for quantifying uncertainty which include weights for ensemble learning(for neural network), 25 columns each for weights for bootstrapping the monte carlo simulator data and weights for bootstrapping the data generator and other specific columns related to the process itself (decay of Z boson to mu mu)
    - Metatdata: 
        - The .h5 file contains different parts/ blocks of the big pandas dataframe. BlockManager is used to group different data types (int64, float32, float64) .
        - Each File and associated Subfiles have attributes like Class, title, etc. which give a high level information about the referred file. These are included in object attribute info tab whereas the general object info tab has basic file information like file path, Name, number of associated members, etc.  (In the HDFview app)
    - Observables: 
        - These include pT_ll, pT_trackj1, tau1_trackj2 and like in total 22 different observables
    - Weights:
        - The actual weights are present in the blocknum_values components (where num could be 0,1 or 2). 
        - Apart from the ones already mentioned, other weights include 4 different weights each for muon detection efficiency and muon detection calibration. Then there are tracking and environmental weights too. 
        


- "What information would a physicist need to reuse these weights that is not currently present in the files?"
    - Information about the process itself
        -  Name of the exact process: here it is Z -> mu mu
    - Information about the kinematic cuts
        - While columns list the observables, the don't present the **selection criteria** 
        - Example: Only muons pT > 25GeV were included. The data is specifically trained on these muons and would not work for muons with pT < 25GeV
    - Information about the simulator and particle generator
        - The information should atleast have the generator software name, its version and its tune
    - Information about the detector which got simulated
        - Since the weights correct for detector effects, they are physcially tied to the detector and the version which was being simulated
        - Example:Weights from a perfect/new detector configuration simulation would not correct for effects in a worn out detector
    - Units used for observables:
        - Values for the observables have been given but not their units

- "What challenges do you anticipate in standardizing this kind of output across different experiments or analyses?"
    - Naming Convention: This is one of the most important standardization dilemmas. Different teams in the scientific community could use different abbreviations for same observable. There needs to be a convention or atleast each team should provide a table giving full form of each observable along with units used.
    - Domain Mismatching: Scientists not bothering about the kinematic cuts that the publishers of the data used: They applied the omnifold algorithm for unfolding their detector level data, only to end up realising this was the wrong approach as their data does not match the requirements to be unfolded by these weights and that the unfolded results would be wrong.
    - Data and System Integrity Issues: The simulated detector and the actual detector being different would lead to incorrect unfolding. 
    - Lack Of Structural Visibility: No information about why the blocking was done in that specific way (we know it is to separate int64, float64, float32 values but they don't!). If different teams block in different ways without giving reasons then this is bad. We need to formalise this too.
    - Metadata: Overall Standardizing the metadata, that is the context, is a bigger issue than standardizing the data. Hence the call for a convention to couple the context to the data!  


    
