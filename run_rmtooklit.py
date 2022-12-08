import sys
sys.path.insert(0, '/scratch/rat0022/RMtoolkit/')
import rm
import numpy as np
import pypulse
from pypulse import Archive
import pylab as plt
import pandas as pd
import glob

path ='./all/'
burst_bw_ts = pd.read_csv('indices.csv')
burst = burst_bw_ts['#burst']
flow = burst_bw_ts['flow']
fhigh =burst_bw_ts['fhigh']
tlow = burst_bw_ts['tlow']
thigh = burst_bw_ts['thigh']
for burst,flow,fhigh,tlow,thigh in zip(burst,flow,fhigh,tlow,thigh):
	ar = Archive(path+burst,prepare=False)
	data = ar.getData()
 	#print(data.shape)
	Iburst = data[0,flow:fhigh,tlow:thigh]
	Qburst = data[1,flow:fhigh,tlow:thigh]
	Uburst = data[2,flow:fhigh,tlow:thigh]
	Vburst = data[3,flow:fhigh,tlow:thigh]
	idata = np.average(Iburst,axis=1)
	qdata= np.average(Qburst,axis=1)
	udata = np.average(Uburst,axis=1)
	vdata = np.average(Vburst,axis=1)
	F = ar.getFreqs()
	freq_hz = F[flow:fhigh]*10**(6) #in Hz
	p = rm.PolObservation(freq_hz,(idata,qdata,udata))
	phi_axis = np.arange(-50000,50000,1)
	p.rmsynthesis(phi_axis)
	p.rmclean(cutoff=1.)
	p.plot_fdf(plot_rmsf=False,save=burst+'.pdf')
	p.get_fdf_peak()
