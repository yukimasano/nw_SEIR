# nw_SEIR: SEIR epidemic on temporal network data

This project simulates a influenza-like (SEIR) epidemic on a real temporal network in python. 
As such outbreaks often spread between individuals, network theory can be used for the mathematical representation of the connections and contact patterns between humans (which are represented as nodes) to include important effects of social networks. In this project, we investigate the use of a temporally resolved network dataset of primary school children's contact patterns to model an influenza-like (SEIR) outbreak in a school. We partly reproduce and analyse results of a publication which investigates different simulated interventions to prevent outbreaks [Gemmetto et al](http://www.sociopatterns.org/publications/targeted-class-closure/). Next,  we apply the idea of an effective distance measure between nodes  which was applied in a publication on the spread of SARS and H1N1 virus on global airport flux data [Brockmann et al.](http://science.sciencemag.org/content/342/6164/1337). We construct these effective distances between the individuals and analyze these with regard to a predicted date of infection. 

# Data

We use real contact data of primary school children in France over a two day period. The data is freely available and is provided by the [SocioPatterns Collaboration][http://www.sociopatterns.org/] . The data has a 20 second time resolution of anonymised face-to-face contacts between pupils and teachers. Contacts lasting over 20 seconds are recorded by the RFID infrastructure when the two sensors are in proximity (between 1-1.5m). Of the 242 children, 232 and all 10 teachers have participated in the study. Further details of the methodology and the data usage consent can be found in the first publication of the data [Stehle et al.](http://journals.plos.org/plosone/article?id=10.1371/journal.pone.0023176). In order to reduce computing time, we have aggregated the contact data into 20min windows.

# Methods
## SEIR model
see [Gemmetto et al](http://www.sociopatterns.org/publications/targeted-class-closure/)

## Effective Distance
see [Brockmann et al.](http://science.sciencemag.org/content/342/6164/1337)

# Results

## Single simulation

### 1. One SEIR simulation that leads to a large scale outbreak. Day 0 corresponds to a Monday
<img src="https://user-images.githubusercontent.com/29401818/32862099-d4d64f80-ca4e-11e7-9c44-0e02e8403183.png" height="400">

### 2. Cumulative incidence by school grade cases and prevalence of infected 
<img src="https://user-images.githubusercontent.com/29401818/32862112-e30ab082-ca4e-11e7-85d5-ba7f9799a702.png" height="400">

## Grade closure intervention
### 1. Without intervention
<img src="https://user-images.githubusercontent.com/29401818/32862130-02988fd2-ca4f-11e7-9bab-1531f5de1d57.png" height ="300">

### 2. With targeted grade closure for 3 days
<img src="https://user-images.githubusercontent.com/29401818/32862142-10d65962-ca4f-11e7-8086-fc00072c1fee.png" height ="300">

## Effective distance on the temporal network

### 1, Effective distances matrix
<img src="https://user-images.githubusercontent.com/29401818/32862158-1c23f342-ca4f-11e7-8994-f5decf1d484f.png" height ="300">

### 2. Date of exposure vs effective distance from the initially infected individual
<img src="https://user-images.githubusercontent.com/29401818/32862179-2a3c1c7a-ca4f-11e7-8141-b9b3e57bea27.png" height ="300">

# Conclusion
In this model targeted grade closure was shown be an effective outbreak mitigation strategy. Furthermore, the effective distance measure gives a good relationship between the distance and the exposure date, potentially allowing us to make inference on the origin of the outbreak. I have more Figures and data, contact me, I'll be glad to help.
