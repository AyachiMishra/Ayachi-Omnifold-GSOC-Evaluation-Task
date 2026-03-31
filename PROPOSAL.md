# GSoC 2026 Proposal: Publication of Omnifold weights
### Standardizing the Publication, Preservation, and Reusability of Omnifold Unfolding Results 

| **Field**    | **Details**                                          |
|--------------|------------------------------------------------------|
| Name         | Ayachi Padmanabh Mishra                              |
| University   | IIT Delhi Abu Dhabi (2nd Year B.Tech. CSE)           |
| Organization | HEP Software Foundation                              |
| Location     | India (UTC+5:30) (Summer 2026)                       |
| Mentors      | Tanvi Wamorkar, Ben Nachman                          |
| CGPA         | 9.01/10                                              |


# Table Of Contents
# 1. About Me
I am Ayachi Padmanabh Mishra, a second-year 4th semester computer science and engineering 
student at IIT Delhi - Abu Dhabi campus. My **CGPA is 9.01/10** and I am among the **top 10% of 
students** of my class. In my current curriculum, I have a fairly good amount of exposure to physics, 
data systems, Software Systems and Machine Learning. **I scored A grades** in the following relevant 
courses: Quantum Physics, Electrodynamics, Linear Algebra, Probability and Stochastic Systems, Data 
Science and Machine Learning.

This background in physics and computer science allows me to understand OmniFold beyond a 
black box workflow which is reflected in my detailed explanations and notes developed during the 
evaluation tasks available in my: task files [5]. 

**Prior Experience:**
- **Domain Immersion**: Studied OmniFold through [Dr. Ben Nachman’s lecture]() (SMU speaker 
series) and reviewed key research papers (mainly the abstract and conclusion and if possible, 
the summary of the methodology used). 

- **Protocol & Schema Design**: In a specialized hackathon for Mashreq Bank, I developed a 
multiple-module Python pipeline  and architecture, and designed a JSON-based governance 
schema to ensure data consistency and safe handling across workflows (it primarily used a 
waterfall model where the json schema grows module after module until the final 4th 
module). This is available in my [project repository](https://github.com/AyachiMishra/Mashreq_Bank_Social_Intelligence_System_With_Agentic_Workflow) [6]. 

- **Experience With Neural Networks**: In my academic project in data science, I have built a 
system to predict heating load of buildings. Inspired by physics, I redefined new building 
features like “compression ratio” and “glazing area distribution” which were fed to the neural 
network. Such features help the ANN, to have smoother convergence in the learning phase. 
This project also helped me understand how to test for convergence and procedures to 
formally evaluate neural networks. I have used the dataset from the university of California
Irvine. This project is available in my repository [9]. 

- **Complex Software Design and Proven Innovation**- I had spent the summer of 2025 in my 
village in India. I observed that agriculture is being done without proper technology. Inspired 
by physics and requirement of farmers, I invented an AI device and software platform in the 
cloud that reduces agricultural costs and incresae  . **I have 
filed a patent** [4] (India Patent No- 202541093222, and PCT Application No – 
PCT/IB2025/061635) at [Intellectual Property India Patent Portal](https://iprsearch.ipindia.gov.in/publicsearch). The Software architecture of the server component was complex 
because it was interacting with hardware and hundreds of end users. While implementing 
this invention, I had used **neural networks** to model relationships between sensor inputs 
and future soil performance. This experience helped me understand practical aspects of 
model’s training on structured, time-dependent data. 

These experiences enable me with skill, the technical depth and the physics intuition needed to 
design a publication and validation standard that is usable by OmniFold analysts. 
# 2. Executive Summary
High dimensional detector data from the Large Hadron Collider is distorted by detector inaccuracies.  Unfolding is the process of recovering underlying true particle-level distributions by correcting these inaccuracies. The standard way to visualize an observable (eg, Jet Mass) without detector effects is 
through histogram unfolding, where the scientist chooses a quantity to unfold and a particular binning rule. He then computes the histogram. While this works for that quantity, we lose much information about other observables in this process. Also, unfolding all observables together is not 
feasible, as it requires matrix inversion, which has high computational costs. 

OmniFold solves this at the event level by using neural networks to output weights attached to each 
event. Because OmniFold unfolds the entire phase space, its main advantage is that binning bias gets 
removed entirely. Hence, once unfolded, we can conveniently multiply each event by its OmniFold 
weight to approximate the correct truth-level data, free of detector effects. However, these weights 
are tied to the experimental setup, including the specific physical process (Eg, Z+ jets), the specific 
detector setup being corrected for (Atlas, CMS, etc.), the model training details, and hence are not universally reusable. Due to the lack of a standardized convention for describing these conditions, these weights are most often unusable, as they are risky for any scientist who is not aware of all the conditions. This was also noted by Canelli et al. [1] in their paper on unbinned unfolding. 

The main objective of this project is to bridge the gap between what OmniFold promises: full phase space unfolding of observables, and what scientists expect: easy publishing and preservation of results, and their efficient reuse.

Firstly, I aim to formalize the specification of these conditions into a derived YAML metadata schema coupled with the OmniFold weights dataset. This will involve defining a minimal specification, such 
as the process name, fiducial cuts, and detector configurations, versus a full specification that 
includes training details (e.g., hyperparameters, model architecture, such as the number of layers and 
neurons, activation functions, etc.). I will also include validation tests and the enforcement of this 
metadata using schemas and schema python library. 

The second aim of this process is to release a Python API on OmniFold to apply/compute weights in a standardized format, computing observables and plotting histograms, and references on how to 
integrate this data with HEPData Archives.  

Lastly, I will be adding an example Jupyter Notebook that explains end to end workflows. As a 4th
semester computer science student with a growing background and experience designing schemas 
and data pipelines, my, I aim to make OmniFold results easier to use not just for their original authors, but for the wider community that wants to build on them. 


# 3. Project Core
This section is organized in following subsections – (i) Background and motivation (ii) Design Philosophy And Critical Decisions 
(iii) Tasks and Deliverables (iv) Project Roadmap and Milestone

## 3.1. Background And Motivation

Unfolding is the process of correcting distortions in detector measurement to recover truth 
distributions that are comparable to theoretical predictions. 

Traditional unfolding is based on the **bin method**, where an analyst chooses a set of observables and 
bin edges in advance, then corrects those histograms based on the detector response. This approach 
has three major limitations: Firstly, **information is lost** because the unfolding is tied to the fixed bins and a small number of observables. Secondly, it is **not reusable** because even a small change in bin size or in observable definitions may require re doing the unfolding. Thus, published results are often limited to a few specific histograms. Last but not least, once data is binned for an analysis, it is **challenging to use the same bin** for new observables. 

OmniFold addresses this by removing the binning process. It performs high-dimensional unfolding 
using machine-learning-based reweighting of simulated events. Under the hood, OmniFold adjusts 
the event weights in full phase space over multiple iterations to match detector-level simulation to 
data. Thus, the resulting truth-level distribution can be used to derive any observable. This makes 
OmniFold very powerful: a single unfolding can be reused to study many different observables, and 
analyses without retraining. 

However, this flexibility comes with its own challenges: OmniFold outputs event level weights whose 
interpretation depends on detailed metadata including event selection, preprocessing, iteration 
count, training details and system encoding. Presently, there is no standard for packaging these 
weights, their associated datasets, and their metadata such that they are easily validated, shared or 
integrated with tools like HEPData. Therefore, much of the method’s potential remains locked within 
individual analyses. There are many other critical struggles occurring in the scientific community such as:

1. The popular Atlas Z+ jets study, which used OmniFold, only had information about the 
generator in their name and had no information about the selection criteria, the model 
parameters, etc. This made it unusable for others who lacked context unless they were willing 
to review the full paper. 

2. Papers such as ‘tools for unbinned unfolding’ by Milton et al. faced heavy documentation 
burdens, requiring the detailed description of preprocessing, model training, weight 
definitions, etc. in narrative form despite being better suited to machine readable metadata 
format. 

3. OmniFold outputs do not fit into existing HEPData workflows, which are designed around 
fixed, binned observables. 

    3.1.  OmniFold produces flexible, high-dimensional results where observables can be 
defined after unfolding. Bridging this mismatch requires defining structured datasets, 
metadata and validation so that results remain both interpretable and compatible with 
existing infrastructure. 

    3.2. HEPData has strict file limits (<100MB) which prevents direct upload of omnifold 
results. 

These challenges highlight the need for standardized publication and preservation of omnifold 
results, forming the core motivation for this project. 


## 3.2. Design Philosophy
I will treat OmniFold results as a well-defined data product with attributes that capture provenace(origin), correctness and reusability. That said, there are some critical decisions and design philosophies I want to highlight about the system before any elaboration on proposed deliverables.

**HDF or Parquet?**   
CERN scientists are more accustomed to the HDF5 format whereas Parquet’s unique columnar approach, storage efficiency and high speeds make it beneficial for large scale analytics. However, since data in OmniFold is inherently hierarchical (different weights and sub-weights), it makes sense to use HDF5 due to its hierarchical structure. Other factors include HDF5’s native support for N-dimensional arrays and tight integration with NumPy and h5py libraries. Ultimately, this decision should be taken by the mentors and the scientific community who will understand their needs better. We can also discuss a hybrid approach which is not in the scope of this paragraph.

**The Master Schema:**  
I will be defining different schemas which include 1 each for model training details, observable definition format and dataset identification to separate our concerns and for clarity. However, there will be a master schema that will be linking to each of these schemas.

**The API:**  
Even without a CLI, the python api’s user-facing entry points will be limited to 3 or 4, avoiding the users from navigating any code complexity. The Python API I will be making uses the schemas designed in the early weeks of the GSoC project to stress test the data and metadata against our defined conventions.

**Documentation:**  
I will be providing detailed and carefully structured Jupyter Notebook demos for this entire OmniFold Ecosystem, which I am sure will be very beneficial for the users. However, I will also provide individual scripts showing each major step of the workflow so that interested users can understand/experiment with a single step at a time

----
## 3.3. Tasks And Proposed Deliverables
These deliverables are the separate components that will make up the standardized OmniFold ecosystem. We first start with setting our conventions for the overall dataset descriptions, weights, and observable definitions and schemas. These will then lead to the Python API that will use these conventions and schemas to standardize the use of OmniFold results. The validation suite will then be built to validate the reinterpretation results (Unfolded observables which use OmniFold weights). Lastly, we will be adding examples and documentation for users to learn from.
We first go to the metadata system for formalizing metadata conventions through machine-readable schemas.

### 3.3.1. Metadata_system (For Metadata and Naming Conventions) [Time: 1 week ]

This is a structured metadata system based on YAML files and a versioned JSON schema, used to describe OmniFold datasets, including the dataset provenance, event selection, and weight definitions.  

**Objective**: To enforce the schema on metadata by throwing errors and giving warnings if they don't follow the proposed schema
Deliverables: A schema.json with a version with clearly defined Required vs Optional fields. A validation module to check whether required fields are present, the schema is being enforced, and type consistency. I will provide metadata conventions in a table format before coding the schema. The schema.py file will be responsible for enforcing it. Providing the proposed metadata conventions in a table format will be the best way to go through. Below is an example of the table and its format. For the YAML schema I had designed during the evaluation task, please refer to the GitHub repo for the same.  

Table 1: Prototype of Proposed Metadata Conventions Presentation(YAML)
### Table 1: Prototype of Proposed Metadata Conventions (YAML)

| Category    | Key             | Type     | Requirement | Description                                              |
|-------------|-----------------|----------|------------|----------------------------------------------------------|
| Provenance  | generator       | string   | Required   | MC Generator (e.g., Pythia_8.3)                          |
| Weights     | w_nominal       | float64  | Required   | Central OmniFold weight for the event                    |
| Structure   | iteration_step  | int      | Required   | The OmniFold iteration index (e.g., 1, 2, 3...)          |
| Physics     | luminosity_fb   | float64  | Optional   | Target data integrated luminosity in fb⁻¹                |

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "OmniFold Metadata Schema v1.0",
  "type": "object",
  "required": ["dataset_identification", "weights", "schema_version"],
  "properties": {
    "schema_version": { "type": "string" },
    "dataset_identification": {
      "type": "object",
      "required": ["process_name", "center_of_mass_energy"],
      "properties": {
        "process_name": { "type": "string" },
        "center_of_mass_energy": { "type": "number" }
      }
    },
    "weights": {
      "type": "object",
      "required": ["w_nominal"],
      "properties": {
        "w_nominal": { "type": "number" },
        "w_systematic": { "type": "array", "items": { "type": "number" } }
      }
    },
    "luminosity_fb": { "type": "number" }
  }
}
```
**How do we check whether a given metadata file follows our schema?**

Below is validate_metadata.py. It is a minimal prototype to show feasibility of the enforcement. This function validates the enforcing of the schema, the detailed validation suite will come later in this proposal, where we will have physics, semantic, and other validation levels. The main work to reach this milestone is to completely define the schema.

```python
import yaml, json
from jsonschema import validate
def verify_metadata(config_path, schema_path):
    # Load human-readable YAML and the formal JSON contract
    with open(config_path) as f: config = yaml.safe_load(f)
    with open(schema_path) as f: schema = json.load(f)
    validate(instance=config, schema=schema) #throws an error if metadata not matching the schema
    return True
```

**Success criteria**:  Given an example OmniFold output,
- validate_metadata("metadata.yaml") either: 
Returns a success report with all required sections present, or Fails with precise error messages pointing to missing/incorrect fields.
- At least two independent test metadata files: one valid, one intentionally broken, both covered by unit tests.


### 3.3.2. Elaborate Weight Naming Convention and Observable Defintions: [2 Weeks]

We still have more standardizations to do in the features of our dataset like weights, observables, etc. This is explained by the fact that having a huge number of weights and observables needs careful structuring enforcement for modularity of the dataset. This will involve ensuring consistency in naming (both weights and observables) and descriptions of the observables.

**Description**: I will present a naming convention for the structural specification of weights and observables. We will standardize the container format of weights to hdf5 and provide an observable description format.  

**Deliverables**: Description of proposed Weight Naming format with documentation on design rationale, examples and lastly Indexing definitions. We now divide the type of deliverable into weight and observables system and discuss them in detail as following:

- **Weight System Deliverables (Kept Minimal):** Proposed naming convention: (type)-(cateogory)-(subcategory)-(name)-(index) Python Utilities (functions) to load, filter(using regex) and validate weights Rules for indexing through weight variations and event indice and a small walkthrough on how to filter for the required weight using regex (a small python file to demonstrate this). (wt_demo.py)  

- **Observable Definition System (Kept Minimal here too):** Here I will provide a schema for observable definitions which will have important fields like name, description, formula, units, phase space and optionally binning. There will again be a validator function solely to verify the observable definitions file against the defined observables schema. An example prototype given below:
```yaml
# This is a prototype of the schema I have made defining observables in OmniFold datasets (could alternatively be defined on JSON too.)(it is machine readable)
type: object
required:
  - observables

properties:
  observables:
    type: array
    items:
      type: object
      required:
        - name
        - description
        - definition
        - units
      properties:
        name:
          type: string
          pattern: "^obs__.+"
#and so on having other fields

```
**Success Criteria:**
- Weight System:
    - For a test HDF5 file having weights such as nominal-1, bootstrap-10, and systematic variations-10, list_weights correctly returns 16 structured entries with correct parsed fields.
- Observable Definition
    - At at least 3 fields which are fully specified and validated by tests (name, definitions, unit).
    - If we are able to check whether Observable definitions in analysis scripts/histograms match those defined in the observable schema.

Having standardized most of the dataset within first 2.5 weeks, we will turn our focus towards getting the minimal product ready straight away by the end of week 4. This involves having a python api ready which will be using validations through our schemas and additional programs that will mask the core routines that take place in reinterpretation.

### 3.3.3. A Unified Pip Installable Python API with CLI  (a stretch goal): [Time: 2 weeks]
**End Result**: Users will be able to publish weights, plot histogram and do reinterpretation of their datasets. This could also be done right from the Command Line Interface (CLI) itself too if it gets completed. (It is just a stretch goal). The api will have not more 3-4 entry points to ensure low apparent complexity. At the end of the 2 weeks, we will be having an api package that can be used to easily run reinterpretation on the dataset using few commands of the api.

```python
import OmniFold as of
# 1. Initialize from a record (e.g., a HEPData entry) or give the path to the file if held locally
analysis = of.Analysis("multifold.h5")
# 2. Load the heavy weights(greatly internal optimisations 
analysis.load()
# 3. Apply to a local 'events' array (NumPy or Awkward)
dist, weights = analysis.apply(my_events, "jet_pt")
# 4. Plot with automatic uncertainty propagation
of.plot_unfolded(dist, weights, label="OmniFold Unfolded")
```
Being able to do the above is in fact the core motivation from these weeks. The deliverable will be the python api and its subprograms.

### 3.3.4. Model & Training Details Standardization [1 Week]

For both reinterpretation and full reproduction of results, a certain number of model parameters need to be known so that we can accurately describe the Neural network model that our dataset learnt from.  For reinterpretation, we only need some information about the neural network to check if it is fine to reinterpret or not. However, for full training, additional information will be required.


**Deliverables**: A formal metadata schema with a helper function for validating the dataset. 
To ensure OmniFold results are both reusable and reproducible, I propose two publication tiers:
- Minimal (Reinterpretation): final weights, feature definitions, preprocessing details → allows direct usage without retraining
- Full (Reproducibility): architecture definitions, training hyperparameters, iteration strategy, and model checkpoints → allows full retraining and pipeline reconstruction

The metadata schema will standardize the description and also what is Required and Not Required for the description of the model and its configuration:
- Model Architecture: layer structure, activations, input/output dimensions
Training hyperparameters: batch size, optimizer, learning rate, early stopping
- Unfolding configuration: number of iterations, step-1/step-2 setup, weight update logic
- Preprocessing (strict): feature ordering, transformations (e.g. angular encodings), normalization parameters

Additional components that I will include for full reproducibility: random seeds (to reduce stochastic variation), ensembling configuration (number of models, aggregation method), dataset references and selection definitions, etc.

This defines a practical reproducibility standard where the full pipeline can be reconstructed with high accuracy, while still supporting lightweight reinterpretation use-cases.

**Success Criteria:**
- A user can reproduce a reference unfolded distribution from a provided OmniFold example dataset by running one short script or one CLI command sequence.
- Unit tests for each public function at least one integration test that runs the full “load → validate → unfold → plot” chain.



### 3.3.5. Validation Suite [2 Weeks]
In this suite, we have to ensure that any dataset that gets produced is physically sound and meaningful and can be trusted by the community. This involve checking against our metadata schemas, ensuring the dataset is sound semantically and physically. And then also doing checks from practical side of things like checking the convergence trend of the training

**My strategy:** I propose Validation be performed at 5 levels, each with clearly defined checks and explicit pass/fail criteria (defining these criteria will be a core part of this deliverable). The validation will be a fail first criterion whereas the dataset is only checked meaningfully if its structurally sound and has no errors in following metadata or in its contents itself.

**Deliverables:** Validation.py which will have a class with all 5 of the below validations as methods and also a GOLDEN dataset which will always pass the validation suite. (This will be helpful while testing the validators)  

We have the 5 levels of validations with the tasks as follows:
1. **Structural Validation:** Ensure metadata schema is enforced,
2. **Semantic Validation:** Ensure observable scales and ranges are consistent
3. **Physics-Level Validation:** Verify that all events satisfy fiducial cuts defined in metadata and ensure no observables violate selection criteria while still being present in the dataset
4. **Neural Network-Level Validation:** Check that OmniFold output weights are physically valid (e.g. non-negative given final activation) and Stability across iterations (detect oscillations or divergence)
5. **Final Output-Level Validation:** This is the most important level which is only run if the dataset passed all the checks from the above levels. The rigorous tests in this are as follows:
    - Closure tests (reco vs unfolded comparisons)
    - Normalization checks (preservation of total cross-section)
    - Consistency of unfolded distributions across iterations and ensembles

Below is a prototype implementation of validation suite. Here we only used 1 method but in the actual suite, we will be using separate methods.
```python
import numpy as np

class OmniFoldValidator:
    def __init__(self, data, metadata):
        self.data = data  # HDF5 or Array-like
        self.meta = metadata
        self.report = {}

    def validate(self):
        # 1. Structural: Check for NaNs/Infs
        weights = self.data.get('weights', np.array([]))
        self.report['structural'] = not np.isnan(weights).any() and len(weights) > 0

        # 2. Physics: Check if pT satisfies the cut defined in metadata
        pt_cut = self.meta.get('pt_min', 0)
        self.report['physics'] = np.all(self.data.get('pt', 0) >= pt_cut)

        # 3. NN Health: Ensure no extreme non-physical weight spikes
        self.report['nn_health'] = np.max(np.abs(weights)) < 1e5 

        return all(self.report.values()), self.report


# Usage
# success, status = OmniFoldValidator(data, meta).validate()

```

**Success Criteria:**
- Structural level catches missing required metadata fields, NaNs/Inf, empty datasets.
- Physics level catches events violating fiducial cuts, inconsistent selection vs metadata.
- NN level detects negative weights when final activation should be non‑negative, or extreme spikes.
- Output level correctly performs at least one closure test and one normalization check on a known example.


### 3.3.6. Example implementations and notebooks [1 week]:
Even with all the above facets of these projects, it will still be incomplete if we don’t actually show to our users how to actually use the project. Hence we keep a folder just for example implementations and notebook. These are files which will be having user centric programs to show how to make the best out of the package. 

**Deliverables:**
1. Jupyter notebooks showing the full workflows unfolding → publication → validation → reinterpretation.
2. We also be providing individual scripts that will handle one task only (publish, validate, reproduce, reinterpret, upload), so users can follow the pipeline at each step too

**Success Criteria:**  
- A new user can follow README and examples to run an end‑to‑end workflow without needing to read internal code.


### 3.3.7. HEP DATA Integration Layer [Stretch Goal] (2 Weeks):
I have designed a minimal tier of this project which is very easy to implement for the timebeing.  It involves the following steps:
- Create a table object and use its add_additional_resource method to link the zenodo link of the dataset to this. 
- While our dataset is not technically integrated with the HEPData, it still has got its own HEPData record id.

This creates an HEPData record Id for the dataset making our dataset become searchable in HEP Data’ s records. However, this is not the desirable full integration. Hepdata is inherently binned whereas omnifold results are unbinned. Figuring out a way to do the core integration (if possible) will take more time though and will need application of more engineering behind it. 

**Success Criteria:**
- For a test dataset, successfully generate a HEPData‑style YAML table for one unfolded observable that passes hepdata_lib validation locally.
- If feasible and allowed, one real or mock record created in a HEPData‑like environment (to be coordinated with mentors).



## 3.4. Project Roadmap and Milestone

### 3.4.1. Community Bonding Period (May 4 – May 24) and Timeline
During the community bonding period, I will complete the necessary groundwork to hit the ground running on Day 1. This involves the following steps to get fully primed for the development phase. It involves the following tasks to be completed:
- **Codebase Audit:** Study hep-lbdl/OmniFold and ViniciusMikuni/OmniFold codebases alongside ATLAS Z+jets GitLab implementations to finalize publication boundaries. Also study current codebases
- **Infrastructure:** Set up the package skeleton (PEP 621), CI/CD development environment, and collect representative OmniFold outputs for testing.
- **Mentor And HSF Community Alignment:** Align with mentors and community on schema field priorities and the user-facing API design and expectations.



### 3.4.2. 12-13 Week Development Phase
### Project Timeline & Milestones

| Week  | Dates                  | Deliverable / Milestone                                                                 | Key Actions to Achieve |
|-------|-----------------------|-----------------------------------------------------------------------------------------|------------------------|
| 1     | May 25 – May 31       | Schema v1.0 & Metadata Validators (Schema enforced on data)                            | 1. Implement YAML loader logic.<br>2. Define machine-readable constraints in `schema.json`.<br>3. Implement schema validators |
| 2–3   | June 1 – June 14      | Weight and Observable Managers                                                          | 1. Build `weights__<cat>__...` string parser.<br>2. Enable programmatic weight discovery.<br>**Artifacts:**<br>- Weights schema & observable definitions schema<br>- `observable_validator.py`, `weights_validator.py`, `weights_loader.py` |
| 4–5   | June 15 – June 28     | Minimal Working API                                                                     | 1. Build minimal API for reinterpretation.<br>2. Combine validators and schemas from previous phases.<br>**Artifacts:**<br>- Minimal API<br>- `minimal_validator.py` |
| 6     | June 28 – July 5      | Midterm Evaluation Prep (July 6: Midterm)                                               | 1. Define Minimal (reinterpretation) vs Full (reproducibility) requirements.<br>2. Standardize architecture & hyperparameter storage.<br>3. Implement preprocessing state serialization.<br>**Artifacts:**<br>- Training schema<br>- `validate_model.py` |
| 7     | July 6 – July 12      | Structural & Semantic Validation                                                        | 1. Build NaN/empty-data detectors.<br>2. Implement unit and scale consistency checks.<br>3. Create pass/fail logic for metadata completeness.<br>**Artifacts:**<br>- Structural & semantic validator methods of     `Validate.py` class|
| 8     | July 13 – July 19     | Physics, NN & Final Output Validation                                                   | 1. Implement fiducial cut enforcement.<br>2. Build weight sanity (non-negativity) checks.<br>3. Develop iteration stability/convergence trackers.<br>**Artifacts:**<br>- Unified validation class<br>- Golden dataset for testing (passes all validations) |
| 9–11  | July 20 – Aug 10      | Documentation & HEPData Integration                                                     | 1. Bridge schema to HEPData-ready YAML (stretch goal).<br>2. Finalize end-to-end “analysis-to-archive” scripts.<br>**Artifacts:**<br>- Workflow example notebooks<br>- Minimal HEPData integration |
| 12-13    | Aug 11 – Aug 23       | Final Audit & Peer Review (Includes ~5-day buffer)                                      | 1. Conduct rigorous peer review with mentors/colleagues.<br>2. Finalize bug fixes and stabilization |


### 3.4.3. Continuous Feedback & Quality Control
I will maintain a Progress & Delta reporting cycle to ensure full alignment with HSF standards. Every Thursday morning, I will submit a mid-week status report detailing current roadblocks and logic changes. After incorporating mentor feedback, I will finalize the week's deliverable by Sunday morning (India Time). This schedule allows mentors to inspect the project quality during their Saturday evening (US), ensuring the following week begins with a peer-reviewed foundation. 

I will also keep a centralised regularly updated document with a 'currently working on' and 'last updated' sections sp that my mentors stay in the loop without the need for direct communication. 

# 4. Contributions
Following are my contributions so far. 
## 4.1. ROOT (RooFit) – Numerical Stability Fix 
Identified a division-by-zero issue in RooPlot::chiSquare when bins have zero error (e.g., expected data errors), leading to NaN values in pull calculations. 
1.	Implemented a safeguard to handle zero-error bins and added a user-facing warning.
2.	Contributed as an interim fix while the method transitions toward RooAbsReal::createChi2
3. Through this, I learned to align closely with maintainer discussions before implementation and to prioritize statistical correctness over superficial fixes

https://github.com/root-project/root/pull/21710


## 4.2. Model Reuse in Omnifold Iterations

**Clarification On Intended Behaviour:** Investigated the training behavior in the official repo for OmniFold examples (GaussianExample.ipynb). 
1.	Observed that the same neural network instance is reused across steps and iterations without weight reinitialization. 
2.	Raised a technical query on whether this reuse is intentional (e.g., for efficiency) or deviates from the expected independence in iterative density ratio estimation. 
3.	Highlighted potential implications for convergence and correctness.  

https://github.com/hep-lbdl/OmniFold/issues/18 


# 5. Logistics: Time Commitment and Availability
I am committing to a 45hour-50hour/week professional immersion for the duration of the 11-week GSoC period. While the core development is estimated at 175 hours, I have allocated a significant "Research and Validation Buffer" to account for the deep literature review required for HEPData schema mapping and rigorous edge-case testing.

My schedule is designed for high-intensity deep-work blocks, typically involving 8–9 hours on weekdays and 3–4 hours on weekends. This flexibility ensures I can investigate deeply before starting work on the proposed deliverable. This is my exclusive professional commitment for the summer; I have no conflicting engagement, summer school or any travel plans.


# 6. Communication Strategy
I am actually comfortable with any mode of communication that the mentors prefer. However, I will suggest avoiding email threads as a mode of communication, as emails can easily get lost in our inboxes.
Some suggestions:
1.	For face-to-face communication: Google Meet, Zoom, etc.
2.	For messaging communication: Mattermost, Slack, or anything other than an email thread.
3.	Code-centric discussions: These can be done through issues/pull requests at the GitHub repo.

The "Thursday Delta": I will provide a weekly summary of progress, current issues, and next steps every Thursday to ensure the project remains on track before the weekend.


# 7. References
1.	Canelli, Florencia, Kyle Cormier, Andrew Cudd, Dag Gillberg, Roger G. Huang, Weijie Jin, Sookhyun Lee et al. "A practical guide to unbinned unfolding." The European Physical Journal C 86, no. 2 (2026): 106.  https://arxiv.org/html/2507.09582v1 
2.	My GitHub Repository:   https://github.com/AyachiMishra 
3.	My LinkedIn profile: https://www.linkedin.com/in/ayachi-p-mishra-8ab952298/ 
Ayachi P. Mishra  “Agricultural Recommendation System and Method using handhelled soiled monitoring with geo-tagged data.” India Patent No- 202541093222 and PCT Application No – PCT/IB2025/061635 
4.	My evaluation Tasks: https://github.com/AyachiMishra/Ayachi-Omnifold-GSOC-Evaluation-Task/tree/main/evaluation_task 
5.	Masreq Bank project repository: 
https://github.com/AyachiMishra/Mashreq_Bank_Social_Intelligence_System_With_Agentic_Workflow
6.	PR: Guard against zero bin errors in chiSquare calculation (#21710)  https://github.com/root-project/root/pull/21710 
7.	Issue: Model reuse across iterations in OmniFold (#18)	https://github.com/hep-lbdl/OmniFold/issues/18 
8.	Academic Project: Heating Load prediction, https://github.com/AyachiMishra/Neural-Network-Based-Prediction-Of-Building-s-Heating-Load- 

