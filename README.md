# Code-Review-Assessment

## How do Automated Tools and Techniques Differ between Open and Closed Source Systems in Assessing their Code Review Quality? An Empirical Study

## File Structure

* `CRA-Model-data` : contains the training and testing data for both open-source and closed-source systems with all the calculated features.
* `RevHelper` : contains the training and testing data for both open-source and closed-source systems with all the calculated features.
It also contains a subdirectory `manual-analysis-data` that consist the result and script of our various manual experiment. 
* `open-source-data` : contains the raw review comments collected from open-source subject systems for this study.
* `closed-source-data` : contains the raw review comments collected from closed-source subject systems for this study.
* `data-collection-script` : contains the script that we use to curate the open-source review comments.
* `utility` : contains various script for data pre-processing and formatting for the tools and techniques that we used in our study.

## Replicate

In this study we replicate existing five sentiment detection tools and two review usefulness classification tools.
To replicate these tools and techniques, we use the replication package provided by the original author.
The link for the replication package is provided below:

### Sentiment detection tools and techniques
* `Stanford Core NLP`: Please follow this link to download this lexicon-based sentiment detection tool 
and evaluate its performance using our open-source and closed-source dataset.  
* `SentiStrengthSE`: Please follow this link to download this sentiment detection tool [link](https://laser.cs.uno.edu/Projects/Projects.html)
 and follow the instruction to evaluate this in our dataset.
* `Senti4SD` : Download the source code for this sentiment detection tool from this [link](https://github.com/collab-uniba/pySenti4SD) and follow the instruction in their readme to evaluate this in our dataset.
* `SentiCR`:  Download the source code from this [link](https://github.com/senticr/SentiCR) and follow the instruction in their readme to evaluate this in our dataset.
* `SentiMoji`:  Download the source code for this deep-learning based sentiment detection tool from this [link](https://github.com/SEntiMoji/SEntiMoji) and follow the instruction in their readme to evaluate this in our dataset.

### Review usefulness classification techniques
* `RevHelper`: Please  download the source code for this review usefulness classification tool using this [link](https://github.com/masud-technope/RevHelper-Replication-Package-MSR2017/tree/master).
The dataset to evaluate this model is already formatted in our `RevHelper` directory. Use both open-source and closed-source dataset to evaluate its performance.
* `CRA-Model`: Please  download the source code for this review usefulness classification tool using this [link](https://github.com/WSU-SEAL/CR-usefulness-EMSE).
The dataset to evaluate this model is already formatted in our `CRA-Model` directory. Use both open-source and closed-source dataset to evaluate its performance.

