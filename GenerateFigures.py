# Comparison of vaccination rates to political lean

# Import Libraries 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import os
from CalStats import GetStats

# Load in the data
ParLean = pd.read_csv('fivethirtyeight_partisan_lean_STATES.csv')
VacDat = pd.read_csv('us-state-covid-vaccines-per-100.csv')

# Filter data (get rid of territories)
Keepers = VacDat['Entity'].isin(ParLean['state'])
BadStates = Keepers == False
BadIdx = BadStates[BadStates].index

VacDat = VacDat.drop(BadIdx)
Days = VacDat['Day'].unique()
ParLean['2021'] = ParLean['2021']*-1.0  # Flip to Make R+ and D-
ParRange=np.array([np.min(ParLean['2021'])-5,np.max(ParLean['2021'])+5]) # Will be used later


# Make and navigate to new directory
TS = time.strftime('%m%d%H%M', time.localtime()) # Get timestamp
InDir = os.getcwd() + '/'  # Get initial directory
os.mkdir(InDir + TS) # Make new directory
os.chdir(InDir + TS) # Move in to new directory

# Preallocate 
rho = np.zeros(Days.size)
beta = np.zeros([Days.size,2])

for i in range (Days.size):
    States = VacDat[VacDat['Day'] == Days[i]]['Entity']  # Find the states this go-round
    Vax = VacDat[VacDat['Day'] == Days[i]]['total_vaccinations_per_hundred'].to_numpy() # Vaccine nums
    iLean = ParLean['2021'][ParLean['state'].isin(States)].to_numpy()  # Get rid of outliers on ith day
    
    # Calculate correlation data and trendline 
    rho[i], beta[i,:] = GetStats(iLean, Vax)
    
    # Plot Trendline
    plt.plot(ParRange, ParRange*beta[i,0]+np.array([1,1])*beta[i,1], linewidth=3, color=[0,0.0,0])
    plt.scatter(iLean, Vax , c=iLean, alpha=0.6, cmap='coolwarm')
    plt.title(Days[i])
    plt.ylabel('Doses Administered per 100')
    plt.xlabel('Partisan Lean')
    plt.legend(['r={:5f}'.format(rho[i])])
    plt.savefig('CorrPlot'+Days[i]+'.png')
    plt.clf()


plt.plot(rho)
plt.xlabel('Day Number (since ' + Days[i] + ')')
plt.ylabel('Correlation Coefficient')
plt.title('Change in correlation')
plt.savefig('CorrChange.png')
plt.clf()
