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
![One SEIR simulation that leads to a large scale outbreak. Day 0 corresponds to a Monday.](https://user-images.githubusercontent.com/29401818/32862099-d4d64f80-ca4e-11e7-9c44-0e02e8403183.png | width=400)

![Cumulative incidence by school grade (top) cases in total and prevalence of infected (bottom)](https://user-images.githubusercontent.com/29401818/32862112-e30ab082-ca4e-11e7-85d5-ba7f9799a702.png)

## Grade closure intervention
![Prevalence curves for the infected without grade closure](https://user-images.githubusercontent.com/29401818/32862130-02988fd2-ca4f-11e7-9bab-1531f5de1d57.png)
![Prevalence curves for the infected with grade closure for 3 days](https://user-images.githubusercontent.com/29401818/32862142-10d65962-ca4f-11e7-8086-fc00072c1fee.png)

## Effective distance on the temporal network
![Effective distances](https://user-images.githubusercontent.com/29401818/32862158-1c23f342-ca4f-11e7-8994-f5decf1d484f.png)
![Date of exposure vs effective distance from the initially infected individual.](https://user-images.githubusercontent.com/29401818/32862179-2a3c1c7a-ca4f-11e7-8141-b9b3e57bea27.png)
