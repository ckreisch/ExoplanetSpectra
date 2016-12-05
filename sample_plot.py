#Created January 13, 2016 to visualize EFTCAMB stability constraints 
import matplotlib
import itertools as it
import matplotlib.pyplot as plt
import numpy as np
from math import *
import matplotlib.ticker as mtick
from decimal import Decimal
from scipy.integrate import quad
from scipy import linalg
from matplotlib import patches
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
import matplotlib.tri as tri
from scipy import stats
from scipy import interpolate
from scipy.interpolate import interp1d

alphaK1_exp3 = np.loadtxt('plots/stab/1_Tensor_Mass_PL_alphaK1_plot_cols.dat', unpack=True, delimiter=',')
alphaKpt01_exp3 = np.loadtxt('plots/stab/1_Tensor_Mass_PL_alphaKpt01_plot_cols.dat', unpack=True, delimiter=',')
reparam = np.loadtxt('plots/stab/1_tensdec_exp_fric_exp_pos_alphaK1.dat', unpack=True, delimiter=',')
reparam2 = np.loadtxt('plots/stab/1_tensder_exp_massder_exp_pos_alphaK1_cols.dat', unpack=True, delimiter=',')
p1 = np.loadtxt('plots/stab/1_Tensor_Mass_PL_alphaKpt1_final_p1_cols.dat', unpack=True, delimiter=',')
p2 = np.loadtxt('plots/stab/1_Tensor_Mass_PL_alphaKpt1_final_p2_cols.dat', unpack=True, delimiter=',')
p3 = np.loadtxt('plots/stab/1_Tensor_Mass_PL_alphaKpt1_final_p3_cols.dat', unpack=True, delimiter=',')
p4 = np.loadtxt('plots/stab/1_Tensor_Mass_PL_alphaKpt1_final_p4_cols.dat', unpack=True, delimiter=',')
tenstest = np.loadtxt('plots/stab/1_Tensdec_Tensder_exp_PL_alphaK1_varall_cols.dat', unpack=True, delimiter=',')
frictest = np.loadtxt('plots/stab/1_fric_Massder_exp_PL_alphaK1_varall_cols.dat', unpack=True, delimiter=',')

tensdect = tenstest[0]
tensdert = tenstest[1]
tensexpt = tenstest[2]

frict = frictest[0]
massdert = frictest[1]
massexpt = frictest[2]

plt.figure()
plt.plot(tensexpt,tensdect,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
#plt.plot(massexp1,tensor1,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
##plt.axhline(y=0.0,c='k',zorder=12)
plt.title('$\\alpha_K=a^3$, sample ln dec values', fontsize=18)
#plt.xlabel('$\ln\\left(10^5\\alpha^M_{\mathrm{dec}}\\right)$', fontsize=18)
plt.ylabel('$\ln\\left(10^{19}\\alpha^T_{\mathrm{dec}}\\right)$', fontsize=18)
#plt.savefig('plots/tensdec_fric_alphaK1_allexp.png')
#plt.xlabel('$M_{0,exp}$', fontsize=18)
plt.xlabel('$\\alpha_{T,exp}$', fontsize=18)
#plt.savefig('plots/Mexp_tensor_alphaK1_all.png')
plt.show()

plt.figure()
plt.plot(massexpt,frict,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
#plt.plot(massexp1,tensor1,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
##plt.axhline(y=0.0,c='k',zorder=12)
plt.title('$\\alpha_K=a^3$, sample ln dec values', fontsize=18)
plt.ylabel('$\ln\\left(10^5\\alpha^M_{\mathrm{dec}}\\right)$', fontsize=18)
#plt.xlabel('$\ln\\left(10^{19}\\alpha^T_{\mathrm{dec}}\\right)$', fontsize=18)
#plt.savefig('plots/tensdec_fric_alphaK1_allexp.png')
plt.xlabel('$M_{0,exp}$', fontsize=18)
#plt.ylabel('$\\alpha_{T,0}$', fontsize=18)
#plt.savefig('plots/Mexp_tensor_alphaK1_all.png')
plt.show()

tensdec = reparam[0]
tensexp = reparam[1]
fric = reparam[2]
massexp = reparam[3]

tensder = reparam2[0]
tensderexp = reparam2[1]
massder = reparam2[2]
massderexp = reparam2[3]

tensor1 = alphaK1_exp3[0]
tensorexp1 = alphaK1_exp3[1]
mass1 = alphaK1_exp3[2]
massexp1 = alphaK1_exp3[3]

tensor01 = alphaKpt01_exp3[0]
tensorexp01 = alphaKpt01_exp3[1]
mass01 = alphaKpt01_exp3[2]
massexp01 = alphaKpt01_exp3[3]

tens1 = p1[0]
tensexp1 = p1[1]
mass1 = p1[2]
massexp1 = p1[3]

neg_count=0
while (tens1[neg_count]<0):
	neg_count=neg_count+1

tens1_neg = tens1[:neg_count]
tensexp1_neg = tensexp1[:neg_count]
mass1_neg = mass1[:neg_count]
massexp1_neg = massexp1[:neg_count]

tens1_pos = tens1[neg_count:]
tensexp1_pos = tensexp1[neg_count:]
mass1_pos = mass1[neg_count:]
massexp1_pos = massexp1[neg_count:]

tens2 = p2[0]
tensexp2 = p2[1]
mass2 = p2[2]
massexp2 = p2[3]

neg_count=0
while (tens2[neg_count]<0):
	neg_count=neg_count+1

tens2_neg = tens2[:neg_count]
tensexp2_neg = tensexp2[:neg_count]
mass2_neg = mass2[:neg_count]
massexp2_neg = massexp2[:neg_count]

tens2_pos = tens2[neg_count:]
tensexp2_pos = tensexp2[neg_count:]
mass2_pos = mass2[neg_count:]
massexp2_pos = massexp2[neg_count:]

tens3 = p3[0]
tensexp3 = p3[1]
mass3 = p3[2]
massexp3 = p3[3]

neg_count=0
while (tens3[neg_count]<0):
	neg_count=neg_count+1

tens3_neg = tens3[:neg_count]
tensexp3_neg = tensexp3[:neg_count]
mass3_neg = mass3[:neg_count]
massexp3_neg = massexp3[:neg_count]

tens3_pos = tens3[neg_count:]
tensexp3_pos = tensexp3[neg_count:]
mass3_pos = mass3[neg_count:]
massexp3_pos = massexp3[neg_count:]

tens4 = p4[0]
tensexp4 = p4[1]
mass4 = p4[2]
massexp4 = p4[3]

neg_count=0
while (tens4[neg_count]<0):
	neg_count=neg_count+1

tens4_neg = tens4[:neg_count]
tensexp4_neg = tensexp4[:neg_count]
mass4_neg = mass4[:neg_count]
massexp4_neg = massexp4[:neg_count]

tens4_pos = tens4[neg_count:]
tensexp4_pos = tensexp4[neg_count:]
mass4_pos = mass4[neg_count:]
massexp4_pos = massexp4[neg_count:]

tensall_neg = np.append(np.append(np.append(tens1_neg,tens2_neg),tens3_neg),tens4_neg)
tensall_pos = np.append(np.append(np.append(tens1_pos,tens2_pos),tens3_pos),tens4_pos)
#tensall = np.append(tensall,tens3)
#tensall = np.append(tensall,tens4)
tensexpall_neg = np.append(np.append(np.append(tensexp1_neg,tensexp2_neg),tensexp3_neg),tensexp4_neg)
tensexpall_pos = np.append(np.append(np.append(tensexp1_pos,tensexp2_pos),tensexp3_pos),tensexp4_pos)
#tensexpall = np.append(tensexpall,tensexp3)
#tensexpall = np.append(tensexpall,tensexp4)
massall_neg = np.append(np.append(np.append(mass1_neg,mass2_neg),mass3_neg),mass4_neg)
massall_pos = np.append(np.append(np.append(mass1_pos,mass2_pos),mass3_pos),mass4_pos)
#massall = np.append(massall,mass3)
#massall = np.append(massall,mass4)
#massall = 1./(1.+massall)
massexpall_neg = np.append(np.append(np.append(massexp1_neg,massexp2_neg),massexp3_neg),massexp4_neg)
massexpall_pos = np.append(np.append(np.append(massexp1_pos,massexp2_pos),massexp3_pos),massexp4_pos)
#massexpall = np.append(massexpall,massexp3)
#massexpall = np.append(massexpall,massexp4)

redshift_neg = np.subtract(np.power(np.abs(np.divide(tensall_neg,0.05)),np.divide(1.,tensexpall_neg)),1.)
redshift_pos = np.subtract(np.power(np.abs(np.divide(tensall_pos,0.05)),np.divide(1.,tensexpall_pos)),1.)

fig100, ax100 = plt.subplots(figsize=(7.416,6))
ax100 = plt.subplot(111)

hist_pos, bins_pos = np.histogram(redshift_pos, bins=149, range=(0,10), density=False)
popmax_pos=hist_pos/float(max(hist_pos))
widths_pos = np.diff(bins_pos)
xvals_pos = bins_pos[:-1]+widths_pos[0]/2.
f_pos = interpolate.PchipInterpolator(xvals_pos, popmax_pos) #interp1d(xvals_pos, popmax_pos, kind='cubic')
hold=0
end=xvals_pos[0]
newxvals_pos=np.array([])
newxvals_pos=np.append(newxvals_pos,xvals_pos[0])
while (end<(xvals_pos[len(xvals_pos)-1]-0.002)):
	newxvals_pos = np.append(newxvals_pos,newxvals_pos[hold]+0.001)
	hold=hold+1
	end=newxvals_pos[hold]

hist_neg, bins_neg = np.histogram(redshift_neg, bins=160, range=(0,10), density=False)
popmax_neg=hist_neg/float(max(hist_neg))
widths_neg = np.diff(bins_neg)
xvals_neg = bins_neg[:-1]+widths_neg[0]/2.
f_neg = interpolate.PchipInterpolator(xvals_neg, popmax_neg) #interp1d(xvals_neg, popmax_neg, kind='cubic')
hold=0
end=xvals_neg[0]
newxvals_neg=np.array([])
newxvals_neg=np.append(newxvals_neg,xvals_neg[0])
while (end<(xvals_neg[len(xvals_neg)-1]-0.002)):
	newxvals_neg = np.append(newxvals_neg,newxvals_neg[hold]+0.001)
	hold=hold+1
	end=newxvals_neg[hold]

mode_pos = (float(bins_pos[argmax(hist_pos)+1])-bins_pos[argmax(hist_pos)])/2.+bins_pos[argmax(hist_pos)]
mode_neg = (float(bins_neg[argmax(hist_neg)+1])-bins_neg[argmax(hist_neg)])/2.+bins_neg[argmax(hist_neg)]

pos_val = 0
neg_val = 0
neg_low = 0
pos_low = 0

i=0
while (i < len(bins_pos)):
	pos_val += hist_pos[i]/float(sum(hist_pos))
	if (pos_val >= 0.25):
		pos_low = (bins_pos[i+1]-bins_pos[i])/2.+bins_pos[i]
		i = len(bins_pos)
	i +=1

i=0
while (i < len(bins_neg)):
	neg_val += hist_neg[i]/float(sum(hist_neg))
	if (neg_val >= 0.25):
		neg_low = (bins_neg[i+1]-bins_neg[i])/2.+bins_neg[i]
		i = len(bins_neg)
	i +=1

ax100.plot(newxvals_neg,f_neg(newxvals_neg), color='cornflowerblue', ls='-',lw=2)
ax100.plot(newxvals_pos,f_pos(newxvals_pos), color='firebrick', ls='-',lw=2)
ax100.text(0.8, 0.25,r'$\bar{z}_{\mathrm{EFT}}='+str('%.2f' % redshift_neg.mean())+'$', color='navy', ha='center', va='center', transform=ax100.transAxes)
ax100.text(0.8, 0.2,r'$\bar{z}_{\mathrm{EFT}}='+str('%.2f' % redshift_pos.mean())+'$', color='firebrick', ha='center', va='center', transform=ax100.transAxes)
ax100.text(0.8, 0.15,r'Mode: $'+str('%.2f' % mode_neg)+',\,95\%\,'+str('%.2f' % neg_low)+'$', color='navy', ha='center', va='center', transform=ax100.transAxes)
ax100.text(0.8, 0.1,r'Mode: $'+str('%.2f' % mode_pos)+',\,95\%\,'+str('%.2f' % pos_low)+'$', color='firebrick', ha='center', va='center', transform=ax100.transAxes)
ax100.set_ylabel("$P/P_{\mathrm{max}}$", fontsize=16) #G_{\mathrm{eff},0}/G
ax100.set_xlabel("$z_{\mathrm{EFT}}$", fontsize=16) #/|\\delta_{\\gamma,\\Lambda CDM,k}|
ax100.set_xlim(0,2.25)
ax100.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax100.tick_params(axis='both', labelsize=16)
plt.show()

sys.exit()

fig1, ax1 = plt.subplots(figsize=(13.424,8))
ax2 = plt.subplot(4,4,13)
ax2.plot(massall_neg,tensexpall_neg, linewidth=0, marker='o', mfc='cornflowerblue', ms=4,ls='none',alpha=0.01)
ax2.plot(massall_pos,tensexpall_pos, linewidth=0, marker='o', mfc='firebrick', ms=4,ls='none',alpha=0.01) #firebrick
ax2.set_xlabel("$\widetilde{M}_0$", fontsize=16) #G_{\mathrm{eff},0}/G
ax2.set_ylabel("$\\xi$", fontsize=16) #/|\\delta_{\\gamma,\\Lambda CDM,k}|
ax2.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax2.tick_params(axis='both', labelsize=16)
plt.show()

ax1 = plt.subplot(449, sharex=ax2)
ax1.plot(massall_neg,tensall_neg, linewidth=0, marker='o', mfc='cornflowerblue', ms=4,ls='none',alpha=0.01)
ax1.plot(massall_pos,tensall_pos, linewidth=0, marker='o', mfc='firebrick', ms=4,ls='none',alpha=0.01)
ax1.set_ylabel("$\\alpha_0^T$", fontsize=18)
ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.setp(ax1.get_xticklabels(), visible=False)
ax1.set_ylim([-1.5,3.7])
ax1.tick_params(axis='y', labelsize=16)
plt.show()

ax3 = plt.subplot(445, sharex=ax1)
ax3.plot(massall_neg,massexpall_neg, linewidth=0, marker='o', mfc='cornflowerblue', ms=4,ls='none',alpha=0.01)
ax3.plot(massall_pos,massexpall_pos, linewidth=0, marker='o', mfc='firebrick', ms=4,ls='none',alpha=0.01)
ax3.set_ylabel("$\\beta$", fontsize=18)
ax3.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.setp(ax3.get_xticklabels(), visible=False)
ax3.tick_params(axis='y', labelsize=16)
plt.show()

ax4 = plt.subplot(4,4,14, sharey=ax2)
ax4.plot(massexpall_neg,tensexpall_neg, linewidth=0, marker='o', mfc='cornflowerblue', ms=4,ls='none',alpha=0.01)
ax4.plot(massexpall_pos,tensexpall_pos, linewidth=0, marker='o', mfc='firebrick', ms=4,ls='none',alpha=0.01)
ax4.set_xlabel("$\\beta$", fontsize=18)
ax4.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax4.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.setp(ax4.get_yticklabels(), visible=False)
ax4.set_xlim([-1,20])
ax4.tick_params(axis='x', labelsize=16)
plt.show()

ax5 = plt.subplot(4,4,10, sharey=ax1, sharex=ax4)
ax5.plot(massexpall_neg,tensall_neg, linewidth=0, marker='o', mfc='cornflowerblue', ms=4,ls='none',alpha=0.01)
ax5.plot(massexpall_pos,tensall_pos, linewidth=0, marker='o', mfc='firebrick', ms=4,ls='none',alpha=0.01)
ax5.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax5.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.setp(ax5.get_xticklabels(), visible=False)
plt.setp(ax5.get_yticklabels(), visible=False)
ax5.set_ylim([-1.5,3.7])
ax5.set_xlim([-1,20])
plt.show()

ax6 = plt.subplot(4,4,15, sharey=ax4)
ax6.plot(tensall_neg,tensexpall_neg, linewidth=0, marker='o', mfc='cornflowerblue', ms=4,ls='none',alpha=0.01)
ax6.plot(tensall_pos,tensexpall_pos, linewidth=0, marker='o', mfc='firebrick', ms=4,ls='none',alpha=0.01)
ax6.set_xlabel("$\\alpha_0^T$", fontsize=18)
ax6.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax6.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.setp(ax6.get_yticklabels(), visible=False)
ax6.set_xlim([-1.5,3.7])
ax6.tick_params(axis='x', labelsize=16)
plt.show()

hist_pos, bins_pos = np.histogram(massall_pos, bins=74, range=(-1,4.96), density=False)
popmax_pos=hist_pos/float(max(hist_pos))
widths_pos = np.diff(bins_pos)
xvals_pos = bins_pos[:-1]+widths_pos[0]/2.
f_pos = interpolate.PchipInterpolator(xvals_pos, popmax_pos) #interp1d(xvals_pos, popmax_pos, kind='cubic')
hold=0
end=xvals_pos[0]
newxvals_pos=np.array([])
newxvals_pos=np.append(newxvals_pos,xvals_pos[0])
while (end<(xvals_pos[len(xvals_pos)-1]-0.002)):
	newxvals_pos = np.append(newxvals_pos,newxvals_pos[hold]+0.001)
	hold=hold+1
	end=newxvals_pos[hold]

hist_neg, bins_neg = np.histogram(massall_neg, bins=74, range=(-1,4.96), density=False)
popmax_neg=hist_neg/float(max(hist_neg))
widths_neg = np.diff(bins_neg)
xvals_neg = bins_neg[:-1]+widths_neg[0]/2.
f_neg = interpolate.PchipInterpolator(xvals_neg, popmax_neg) #interp1d(xvals_neg, popmax_neg, kind='cubic')
hold=0
end=xvals_neg[0]
newxvals_neg=np.array([])
newxvals_neg=np.append(newxvals_neg,xvals_neg[0])
while (end<(xvals_neg[len(xvals_neg)-1]-0.002)):
	newxvals_neg = np.append(newxvals_neg,newxvals_neg[hold]+0.001)
	hold=hold+1
	end=newxvals_neg[hold]

ax95 = plt.subplot(441, sharex=ax2)
ax95.plot(newxvals_neg,f_neg(newxvals_neg), color='cornflowerblue', ls='-',lw=2)
ax95.plot(newxvals_pos,f_pos(newxvals_pos), color='firebrick', ls='-',lw=2)
ax95.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
#ax95.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.setp(ax95.get_xticklabels(), visible=False)
plt.setp(ax95.get_yticklabels(), visible=False)
plt.tick_params(axis='y',which='both',left='off',right='off') 
#ax95.set_ylim([-1.5,3.7])
#ax95.set_xlim([-1,20])
#ax95.set_ylabel('$P/P_{\mathrm{max}}$', fontsize=18)
plt.show()

hist_pos, bins_pos = np.histogram(massexpall_pos, bins=149, range=(-5,20), density=False)
popmax_pos=hist_pos/float(max(hist_pos))
widths_pos = np.diff(bins_pos)
xvals_pos = bins_pos[:-1]+widths_pos[0]/2.
f_pos = interpolate.PchipInterpolator(xvals_pos, popmax_pos) #interp1d(xvals_pos, popmax_pos, kind='cubic')
hold=0
end=xvals_pos[0]
newxvals_pos=np.array([])
newxvals_pos=np.append(newxvals_pos,xvals_pos[0])
while (end<(xvals_pos[len(xvals_pos)-1]-0.002)):
	newxvals_pos = np.append(newxvals_pos,newxvals_pos[hold]+0.001)
	hold=hold+1
	end=newxvals_pos[hold]

hist_neg, bins_neg = np.histogram(massexpall_neg, bins=160, range=(-5,20), density=False)
popmax_neg=hist_neg/float(max(hist_neg))
widths_neg = np.diff(bins_neg)
xvals_neg = bins_neg[:-1]+widths_neg[0]/2.
f_neg = interpolate.PchipInterpolator(xvals_neg, popmax_neg) #interp1d(xvals_neg, popmax_neg, kind='cubic')
hold=0
end=xvals_neg[0]
newxvals_neg=np.array([])
newxvals_neg=np.append(newxvals_neg,xvals_neg[0])
while (end<(xvals_neg[len(xvals_neg)-1]-0.002)):
	newxvals_neg = np.append(newxvals_neg,newxvals_neg[hold]+0.001)
	hold=hold+1
	end=newxvals_neg[hold]

ax96 = plt.subplot(446, sharex=ax4)
ax96.plot(newxvals_neg,f_neg(newxvals_neg), color='cornflowerblue', ls='-',lw=2)
ax96.plot(newxvals_pos,f_pos(newxvals_pos), color='firebrick', ls='-',lw=2)
ax96.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
#ax95.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.setp(ax96.get_xticklabels(), visible=False)
plt.setp(ax96.get_yticklabels(), visible=False)
plt.tick_params(axis='y',which='both',left='off',right='off')
#ax95.set_ylim([-1.5,3.7])
#ax95.set_xlim([-1,20])
#ax95.set_ylabel('$P/P_{\mathrm{max}}$', fontsize=18)
plt.show()

hist_pos, bins_pos = np.histogram(tensall_pos, bins=75, range=(-1,5), density=False)
popmax_pos=hist_pos/float(max(hist_pos))
widths_pos = np.diff(bins_pos)
xvals_pos = bins_pos[:-1]+widths_pos[0]/2.
f_pos = interpolate.PchipInterpolator(xvals_pos, popmax_pos) #interp1d(xvals_pos, popmax_pos, kind='cubic')
hold=0
end=xvals_pos[0]
newxvals_pos=np.array([])
newxvals_pos=np.append(newxvals_pos,xvals_pos[0])
while (end<(xvals_pos[len(xvals_pos)-1]-0.002)):
	newxvals_pos = np.append(newxvals_pos,newxvals_pos[hold]+0.001)
	hold=hold+1
	end=newxvals_pos[hold]

hist_neg, bins_neg = np.histogram(tensall_neg, bins=80, range=(-1,5), density=False)
popmax_neg=hist_neg/float(max(hist_neg))
widths_neg = np.diff(bins_neg)
xvals_neg = bins_neg[:-1]+widths_neg[0]/2.
f_neg = interpolate.PchipInterpolator(xvals_neg, popmax_neg) #interp1d(xvals_neg, popmax_neg, kind='cubic')
hold=0
end=xvals_neg[0]
newxvals_neg=np.array([])
newxvals_neg=np.append(newxvals_neg,xvals_neg[0])
while (end<(xvals_neg[len(xvals_neg)-1]-0.002)):
	newxvals_neg = np.append(newxvals_neg,newxvals_neg[hold]+0.001)
	hold=hold+1
	#print newxvals_neg[hold]
	end=newxvals_neg[hold]

ax97 = plt.subplot(4,4,11, sharex=ax6)
ax97.plot(newxvals_neg,f_neg(newxvals_neg), color='cornflowerblue', ls='-',lw=2)
ax97.plot(newxvals_pos,f_pos(newxvals_pos), color='firebrick', ls='-',lw=2)
ax97.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
#ax95.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.setp(ax97.get_xticklabels(), visible=False)
plt.setp(ax97.get_yticklabels(), visible=False)
plt.tick_params(axis='y',which='both',left='off',right='off')
#ax95.set_ylim([-1.5,3.7])
#ax95.set_xlim([-1,20])
#ax95.set_ylabel('$P/P_{\mathrm{max}}$', fontsize=18)
plt.show()

hist_pos, bins_pos = np.histogram(tensexpall_pos, bins=149, range=(-5,20), density=False)
popmax_pos=hist_pos/float(max(hist_pos))
widths_pos = np.diff(bins_pos)
xvals_pos = bins_pos[:-1]+widths_pos[0]/2.
f_pos = interpolate.PchipInterpolator(xvals_pos, popmax_pos) #interp1d(xvals_pos, popmax_pos, kind='cubic')
hold=0
end=xvals_pos[0]
newxvals_pos=np.array([])
newxvals_pos=np.append(newxvals_pos,xvals_pos[0])
while (end<(xvals_pos[len(xvals_pos)-1]-0.002)):
	newxvals_pos = np.append(newxvals_pos,newxvals_pos[hold]+0.001)
	hold=hold+1
	end=newxvals_pos[hold]

hist_neg, bins_neg = np.histogram(tensexpall_neg, bins=149, range=(-5,20), density=False)
popmax_neg=hist_neg/float(max(hist_neg))
widths_neg = np.diff(bins_neg)
xvals_neg = bins_neg[:-1]+widths_neg[0]/2.
f_neg = interpolate.PchipInterpolator(xvals_neg, popmax_neg) #interp1d(xvals_neg, popmax_neg, kind='cubic')
hold=0
end=xvals_neg[0]
newxvals_neg=np.array([])
newxvals_neg=np.append(newxvals_neg,xvals_neg[0])
while (end<(xvals_neg[len(xvals_neg)-1]-0.002)):
	newxvals_neg = np.append(newxvals_neg,newxvals_neg[hold]+0.001)
	hold=hold+1
	#print newxvals_neg[hold]
	end=newxvals_neg[hold]

ax98 = plt.subplot(4,4,16)
ax98.plot(newxvals_neg,f_neg(newxvals_neg), color='cornflowerblue', ls='-',lw=2)
ax98.plot(newxvals_pos,f_pos(newxvals_pos), color='firebrick', ls='-',lw=2)
ax98.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
#ax95.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.setp(ax98.get_xticklabels(), visible=True)
plt.setp(ax98.get_yticklabels(), visible=False)
plt.tick_params(axis='y',which='both',left='off',right='off')
#ax95.set_ylim([-1.5,3.7])
#ax95.set_xlim([-1,20])
ax98.set_xlim([0,20])
ax98.tick_params(axis='x', labelsize=16)
ax98.set_xlabel('$\\xi$', fontsize=18)
plt.show()

fig1.tight_layout
fig1.subplots_adjust(hspace=0)
fig1.subplots_adjust(wspace=0)
plt.show()
fig1.savefig('paper/figs/Kpt1_stability_tri_new_colors_posteriors.png', bbox_inches='tight')

'''
plt.figure()
hist,xedge,yedge= np.histogram2d(tensall,tensexpall,bins=150)
plt.imshow(hist, extent=[xedge[0],xedge[-1],yedge[0],yedge[-1]])
#hist==0, origin='lower',cmap=plt.gray(),extent=[xedge[0],xedge[-1],yedge[0],yedge[-1]])
#plt.savefig('hist2d.png')
plt.title('tri test', fontsize=16)
# labels
plt.xlabel('$\\alpha_0^T$', fontsize=18)
plt.ylabel('$\\xi$', fontsize=18)
plt.show()
'''

'''
triang = tri.Triangulation(tensall, tensexpall)
plt.triplot(triang, 'bo-')
#plt.tricontourf(triang, np.ones(tensall), colors= 'r', alpha=0.3, levels=[1., 2.])
#plt.tricontour(triang, np.ones(tensall), colors='r', levels=[1., 2.])
# title of the plot
plt.title('tri test', fontsize=16)
# labels
plt.xlabel('$\\alpha_0^T$', fontsize=18)
plt.ylabel('$\\xi$', fontsize=18)
plt.show()
'''
i=len(tens1)-1
Tparam1 = np.array([])
Mparam1 = np.array([])
Tcut1 = np.array([])
Mcut1 = np.array([])
Mexp1 = np.array([])
Texp1 = np.array([])
while (tens1[i]>0.0) and (i>-1):
    Tparam1 = np.append(Tparam1,log(pow(10.0,19.0)*tens1[i]*(1./1090.72)**tensexp1[i]))
    Tcut1 = np.append(Tcut1, tens1[i])
    Texp1 = np.append(Texp1, tensexp1[i])
    Mparam1 = np.append(Mparam1,log(10.**5.*massexp1[i]*mass1[i]*(1./1090.72)**massexp1[i]/(1.+mass1[i]*(1./1090.72)**massexp1[i])))
    Mcut1 = np.append(Mcut1, mass1[i])
    Mexp1 = np.append(Mexp1, massexp1[i])
    i=i-1

i=len(tens2)-1
Tparam2 = np.array([])
Mparam2 = np.array([])
Tcut2 = np.array([])
Mcut2 = np.array([])
Mexp2 = np.array([])
Texp2 = np.array([])
while (tens2[i]>0.0) and (i>-1):
    Tparam2 = np.append(Tparam2,log(pow(10.0,19.0)*tens2[i]*(1./1090.72)**tensexp2[i]))
    Tcut2 = np.append(Tcut2, tens2[i])
    Texp2 = np.append(Texp2, tensexp2[i])
    Mparam2 = np.append(Mparam2,log(10.**5.*massexp2[i]*mass2[i]*(1./1090.72)**massexp2[i]/(1.+mass2[i]*(1./1090.72)**massexp2[i])))
    Mcut2 = np.append(Mcut2, mass2[i])
    Mexp2 = np.append(Mexp2, massexp2[i])
    i=i-1
    #print i

i=len(tens3)-1
Tparam3 = np.array([])
Mparam3 = np.array([])
Tcut3 = np.array([])
Mcut3 = np.array([])
Mexp3 = np.array([])
Texp3 = np.array([])
while (tens3[i]>0.0) and (i>-1):
    Tparam3 = np.append(Tparam3,log(pow(10.0,19.0)*tens3[i]*(1./1090.72)**tensexp3[i]))
    Tcut3 = np.append(Tcut3, tens3[i])
    Mparam3 = np.append(Mparam3,log(10.**5.*massexp3[i]*mass3[i]*(1./1090.72)**massexp3[i]/(1.+mass3[i]*(1./1090.72)**massexp3[i])))
    Mcut3 = np.append(Mcut3, mass3[i])
    Mexp3 = np.append(Mexp3, massexp3[i])
    Texp3 = np.append(Texp3, tensexp3[i])
    i=i-1

i=len(tens4)-1
Tparam4 = np.array([])
Mparam4 = np.array([])
Tcut4 = np.array([])
Mcut4 = np.array([])
Mexp4 = np.array([])
Texp4 = np.array([])
while (tens4[i]>0.0) and (i>-1):
    Tparam4 = np.append(Tparam4,log(pow(10.0,19.0)*tens4[i]*(1./1090.72)**tensexp4[i]))
    Tcut4 = np.append(Tcut4, tens4[i])
    Mparam4 = np.append(Mparam4,log(10.**5.*massexp4[i]*mass4[i]*(1./1090.72)**massexp4[i]/(1.+mass4[i]*(1./1090.72)**massexp4[i])))
    Mcut4 = np.append(Mcut4, mass4[i])
    Mexp4 = np.append(Mexp4, massexp4[i])
    Texp4 = np.append(Texp4, tensexp4[i])
    i=i-1


plt.figure()
plt.plot(Mexp1, Mparam1,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
plt.plot(Mexp2, Mparam2,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
plt.plot(Mexp3, Mparam3,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
plt.plot(Mexp4, Mparam4,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
#plt.plot(massexp1,tensor1,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
##plt.axhline(y=0.0,c='k',zorder=12)
plt.title('$\\alpha_K=a^3$, sample orig param', fontsize=18)
plt.ylabel('$\ln\\left(10^5\\alpha^M_{\mathrm{dec}}\\right)$', fontsize=18)
#plt.ylabel('$\ln\\left(10^{19}\\alpha^T_{\mathrm{dec}}\\right)$', fontsize=18)
#plt.savefig('plots/tensdec_fric_alphaK1_allexp.png')
plt.xlabel('$M_{0,exp}$', fontsize=18)
#plt.ylabel('$M_{0}$', fontsize=18)
#plt.ylabel('$\\alpha_{T,0}$', fontsize=18)
#plt.savefig('plots/Mexp_tensor_alphaK1_all.png')
plt.show()

plt.figure()
plt.plot(mass1,tens1,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
plt.plot(mass2,tens2,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
plt.plot(mass3,tens3,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
plt.plot(mass4,tens4,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
#plt.plot(massexp1,tensor1,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
##plt.axhline(y=0.0,c='k',zorder=12)
plt.title('$\\alpha_K=a^3$, sample orig param', fontsize=18)
#plt.xlabel('$\ln\\left(10^5\\alpha^M_{\mathrm{dec}}\\right)$', fontsize=18)
#plt.ylabel('$\ln\\left(10^{19}\\alpha^T_{\mathrm{dec}}\\right)$', fontsize=18)
#plt.savefig('plots/tensdec_fric_alphaK1_allexp.png')
plt.xlabel('$M_{0}$', fontsize=18)
plt.ylabel('$\\alpha_{T,0}$', fontsize=18)
#plt.savefig('plots/Mexp_tensor_alphaK1_all.png')
plt.show()

plt.figure()
plt.plot(Tparam1,Mparam1,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
plt.plot(Tparam2,Mparam2,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
plt.plot(Tparam3,Mparam3,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
plt.plot(Tparam4,Mparam4,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
#plt.plot(massexp1,tensor1,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
##plt.axhline(y=0.0,c='k',zorder=12)
plt.title('$\\alpha_K=a^3, sample orig param$', fontsize=18)
plt.ylabel('$\ln\\left(10^5\\alpha^M_{\mathrm{dec}}\\right)$', fontsize=18)
plt.xlabel('$\ln\\left(10^{19}\\alpha^T_{\mathrm{dec}}\\right)$', fontsize=18)
#plt.savefig('plots/tensdec_fric_alphaK1_allexp.png')
#plt.xlabel('$M_{0,exp}$', fontsize=18)
#plt.ylabel('$\\alpha_{T,0}$', fontsize=18)
#plt.savefig('plots/Mexp_tensor_alphaK1_all.png')
plt.show()

plt.figure()
plt.plot(Texp1,Tparam1,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
plt.plot(Texp2,Tparam2,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
plt.plot(Texp3,Tparam3,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
plt.plot(Texp4,Tparam4,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
#plt.plot(massexp1,tensor1,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
##plt.axhline(y=0.0,c='k',zorder=12)
plt.title('$\\alpha_K=a^3, sample orig param$', fontsize=18)
#plt.xlabel('$\ln\\left(10^5\\alpha^M_{\mathrm{dec}}\\right)$', fontsize=18)
plt.ylabel('$\ln\\left(10^{19}\\alpha^T_{\mathrm{dec}}\\right)$', fontsize=18)
#plt.savefig('plots/tensdec_fric_alphaK1_allexp.png')
#plt.ylabel('$M_{0}$', fontsize=18)
plt.xlabel('$\\alpha_{T,exp}$', fontsize=18)
#plt.ylabel('$\\alpha_{T,0}$', fontsize=18)
#plt.savefig('plots/Mexp_tensor_alphaK1_all.png')
plt.show()

Texptot = np.append(Texp1,Texp2)
Texptot = np.append(Texptot,Texp3)
Texptot = np.append(Texptot,Texp4)
Tparamtot = np.append(Tparam1,Tparam2)
Tparamtot = np.append(Tparamtot,Tparam3)
Tparamtot = np.append(Tparamtot,Tparam4)
Treparam = np.divide(np.subtract(Tparamtot,44.54487723),np.multiply(-7.11623565,Texptot))
Treparam2 = np.divide(np.subtract(Treparam,np.multiply(0.1294,np.exp(-Texptot))),0.9986)

new_fit = np.transpose(np.vstack((Texptot,Treparam)))
sort_fit = new_fit[new_fit[:,0].argsort()]

start_exp = min(Texptot)
upper_bound = np.array([])
upper_bound = np.append(upper_bound,0.0)
upper_exp = np.array([])
upper_exp = np.append(upper_exp,start_exp)
for i in range(0,len(Texptot)):
    if sort_fit[i][0]>upper_exp[len(upper_exp)-1]:
        upper_exp = np.append(upper_exp,sort_fit[i][0])
        upper_bound = np.append(upper_bound,sort_fit[i][1])
    else:
        if sort_fit[i][1]>upper_bound[len(upper_bound)-1]:
            upper_bound[len(upper_bound)-1]=sort_fit[i][1]
    

plt.figure()
plt.plot(Texptot,Treparam,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
plt.plot(upper_exp,upper_bound,mec='k', linewidth=0, marker='o', mfc='r', ms=4,ls='none',alpha=0.5)
plt.title('$\\alpha_K=a^3$, sample orig param, reparam', fontsize=18)
plt.xlabel('$\\alpha_{T,exp}$', fontsize=18)
plt.ylabel('New param', fontsize=18)
plt.show()


scale = 1.0
'''
massterm1 = np.multiply(mass1,np.power(scale,massexp1))
alpham1 = np.divide(np.multiply(massexp1,massterm1),np.add(1.0,massterm1))
cT_sq1 = np.add(1.0,np.multiply(tensor1,np.power(scale,tensorexp1)))

plt.figure()
plt.plot(alpham1,cT_sq1,mec='k', linewidth=2, marker='o', mfc='sienna', ms=4,ls='none')
plt.axhline(y=1.0,c='k',zorder=12)
plt.title('$\\alpha_K=a^3$', fontsize=18)
plt.xlabel('$\\alpha_m\\left(a=1.0\\right)$', fontsize=18)
plt.ylabel('$c_T^2\\left(a=1.0\\right)$', fontsize=18)
plt.show()

massterm01 = np.multiply(mass01,np.power(scale,massexp01))
alpham01 = np.divide(np.multiply(massexp01,massterm01),np.add(1.0,massterm01))
cT_sq01 = np.add(1.0,np.multiply(tensor01,np.power(scale,tensorexp01)))

plt.figure()
plt.plot(alpham01,cT_sq01,mec='k', linewidth=2, marker='o', mfc='sienna', ms=4,ls='none')
plt.axhline(y=1.0,c='k',zorder=12)
plt.title('$\\alpha_K=0.01a^3$', fontsize=18)
plt.xlabel('$\\alpha_m\\left(a=1.0\\right)$', fontsize=18)
plt.ylabel('$c_T^2\\left(a=1.0\\right)$', fontsize=18)
plt.show()
'''
'''
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for a_iter in np.arange(0,1.1,0.1):
#a_iter=0.5 
    massterm01 = np.multiply(mass01,np.power(a_iter,massexp01))
    alpham01 = np.divide(np.multiply(massexp01,massterm01),np.add(1.0,massterm01))
    cT_sq01 = np.add(1.0,np.multiply(tensor01,np.power(a_iter,tensorexp01)))
    a_size = len(cT_sq01)
    scale_list = np.empty(a_size)
    scale_list.fill(a_iter)
    ax.scatter(alpham01,cT_sq01,scale_list,zdir='z',s=1,c='k')

ax.set_title('$\\alpha_K=0.01a^3$', fontsize=18)
ax.set_xlabel('$\\alpha_m$', fontsize=18)
ax.set_ylabel('$c_T^2$', fontsize=18)
ax.set_zlabel('$\\mathrm{Scale\,Factor,\,a}$', fontsize=18)
plt.savefig('plots/fric_speed_scalefunction_10.png')
plt.show()
'''
'''
plt.figure()
plt.plot(massder,tensder,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
#plt.plot(massexp1,tensor1,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
##plt.axhline(y=0.0,c='k',zorder=12)
plt.title('$\\alpha_K=a^3$, sample ln dec', fontsize=18)
#plt.xlabel('$\ln\\left(10^5\\alpha^M_{\mathrm{dec}}\\right)$', fontsize=18)
#plt.ylabel('$\ln\\left(10^{19}\\alpha^T_{\mathrm{dec}}\\right)$', fontsize=18)
#plt.savefig('plots/tensdec_fric_alphaK1_allexp.png')
plt.xlabel('$M_{0,exp}$', fontsize=18)
plt.ylabel('$\\alpha_{T,0}$', fontsize=18)
#plt.savefig('plots/Mexp_tensor_alphaK1_all.png')
plt.show()
'''
'''
plt.figure()
plt.plot(mass01,tensor01,mec='k', linewidth=0, marker='o', mfc='b', ms=4,ls='none',alpha=0.1)
plt.axhline(y=0.0,c='k',zorder=12)
plt.title('$\\alpha_K=0.01a^3$', fontsize=18)
plt.xlabel('$M_0$', fontsize=18)
plt.ylabel('$\\alpha_{T,0}$', fontsize=18)
plt.savefig('plots/M_tens_alphaKpt01_allexp.png')
plt.show()
'''
'''
plt.figure()
for a_iter in np.arange(1.0,-0.1,-0.1):
    #massterm01 = np.multiply(mass01,np.power(a_iter,massexp01))
    #alpham01 = np.divide(np.multiply(massexp01,massterm01),np.add(1.0,massterm01))
    cT_sq01 = np.add(1.0,np.multiply(tensor01,np.power(a_iter,tensorexp01)))
    a_size = len(cT_sq01)
    scale_list = np.empty(a_size)
    scale_list.fill(a_iter)
    plt.plot(scale_list,cT_sq01,marker='o',mec='k',linewidth=0,ls='none',ms=4,alpha=0.1,mfc='r')
plt.title('$\\alpha_K=0.01a^3$', fontsize=18)
plt.xlabel('$\mathrm{Scale\,Factor,\,a}$', fontsize=18)
plt.ylabel('$c_T^2$', fontsize=18)
plt.savefig('plots/speed_a_alphaKpt01.png')
'''
'''
plt.figure()
for a_iter in np.arange(1.0,-0.1,-0.1):
    #massterm1 = np.multiply(mass1,np.power(a_iter,massexp1))
    #alpham1 = np.divide(np.multiply(massexp1,massterm1),np.add(1.0,massterm1))
    cT_sq1 = np.add(1.0,np.multiply(tensor1,np.power(a_iter,tensorexp1)))
    a_size = len(cT_sq1)
    scale_list = np.empty(a_size)
    scale_list.fill(a_iter)
    plt.plot(scale_list,cT_sq1,marker='o',mec='k',linewidth=0,ls='none',ms=4,alpha=0.1,mfc='r')
plt.title('$\\alpha_K=a^3$', fontsize=18)
plt.xlabel('$\mathrm{Scale\,Factor,\,a}$', fontsize=18)
plt.ylabel('$c_T^2$', fontsize=18)
plt.savefig('plots/speed_a_alphaK1.png')
'''

'''
p=[]
cm = plt.cm.get_cmap('nipy_spectral')
fig = plt.figure()
for a_iter in np.arange(1.0,-0.1,-0.1):
    massterm01 = np.multiply(mass01,np.power(a_iter,massexp01))
    alpham01 = np.divide(np.multiply(massexp01,massterm01),np.add(1.0,massterm01))
    cT_sq01 = np.add(1.0,np.multiply(tensor01,np.power(a_iter,tensorexp01)))
    a_size = len(cT_sq01)
    myc = np.empty(a_size)
    myc.fill(a_iter)
    plt.scatter(alpham01,cT_sq01,s=1,vmin=0.0,vmax=1.0,c=myc,cmap=cm,lw = 0,alpha=0.5)
#fig.colorbar(p)
color_bar = colorbar()
color_bar.set_alpha(1)
color_bar.draw_all()
plt.axhline(y=1.0,c='k',lw=2,zorder=12)
plt.title('$\\alpha_K=0.01$', fontsize=18)
plt.xlabel('$\\alpha_m$', fontsize=18)
plt.ylabel('$c_T^2$', fontsize=18)
plt.savefig('plots/fric_speed_scalefunction_alphaKpt01const_10_2D_trans.png')
#plt.show()


p=[]
cm = plt.cm.get_cmap('nipy_spectral')
fig = plt.figure()
#color_bar=colorbar()
#scale_list = np.arange(1.0,-0.1,-0.1)
for a_iter in np.arange(1.0,-0.1,-0.1):
    massterm1 = np.multiply(mass1,np.power(a_iter,massexp1))
    alpham1 = np.divide(np.multiply(massexp1,massterm1),np.add(1.0,massterm1))
    cT_sq1 = np.add(1.0,np.multiply(tensor1,np.power(a_iter,tensorexp1)))
    a_size = len(cT_sq1)
    myc = np.empty(a_size)
    myc.fill(a_iter)
    plt.scatter(alpham1,cT_sq1,s=1,vmin=0.0,vmax=1.0,c=myc,cmap=cm,lw = 0,alpha=0.5)
#fig.colorbar(p, alpha=1.0)
#fig.colorbar(p)
#colorbar.ColorbarBase.set_alpha(1)
#colorbar.ColorbarBase.draw_all()
color_bar = colorbar()
color_bar.set_alpha(1)
color_bar.draw_all()
#cbar.solids.set(alpha=1)
plt.axhline(y=1.0,lw=2,c='k',zorder=12)
plt.title('$\\alpha_K=1.0$', fontsize=18)
plt.xlabel('$\\alpha_m$', fontsize=18)
plt.ylabel('$c_T^2$', fontsize=18)
plt.savefig('plots/fric_speed_scalefunction_alphaK1const_10_2D_trans.png')
#plt.show()

#scale_list = np.append(scale_list,a_iter)

#massterm1 = np.multiply(mass1,np.power(scale,massexp1))
#alpham1 = np.divide(np.multiply(massexp1,massterm1),np.add(1.0,np.multiply(mass1,np.power(scale_list,massexp1))))
#cT_sq1 = np.add(1.0,np.multiply(tensor1,np.power(scale_list,tensorexp1)))

#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.scatter(np.divide(np.multiply(massexp1,massterm1),np.add(1.0,np.multiply(mass1,np.power(scale_list,massexp1)))),np.add(1.0,np.multiply(tensor1,np.power(scale_list,tensorexp1))),scale_list,zdir='z',s=1,c='k')
#ax.set_title('$\\alpha_K=a^3$', fontsize=18)
#ax.set_xlabel('$\\alpha_m$', fontsize=18)
#ax.set_ylabel('$c_T^2$', fontsize=18)
#ax.set_zlabel('Scale Factor, a', fontsize=18)
#plt.show()
#plt.savefig('mass_tensor_neg_dep.png')
'''

'''
mass_list = np.array([])
tens_max = np.array([])
mass_list = np.append(mass_list,0.0)
tens_max = np.append(tens_max,0.0)
tens_ind = 0
for i in range(0,250000): #125000
    print i
    if check2[i]>0.0:
        m_ind = 1
        ind_lim = len(mass_list)
        for ind in range(0,ind_lim):
            if (mass2[i]==mass_list[ind]):
                if (tensor2[i]>tens_max[ind]):
                    tens_max[ind]=tensor2[i]
            m_ind = m_ind + 1
        if (m_ind>len(mass_list)):
            mass_list = np.append(mass_list,mass2[i])
            tens_max = np.append(tens_max,tensor2[i])
        #ax.scatter(mass2[i],kin2[i],tensor2[i],zdir='z',s=1,c='r')
        #plt.scatter(mass2[i], tensor2[i], edgecolors='r', facecolors='r')
plt.figure()
plt.plot(mass_list,tens_max)
plt.xlabel('Mass')
plt.ylabel('Tensor, alpha')
plt.show()
'''
'''
plt.figure()
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
for i in range(0,250000): #125000
    #if check[i]>0.0:
        #ax.scatter(mass[i],kin[i],tensor[i],zdir='z',s=1,c='k')
    if check2[i]>0.0:
        #ax.scatter(mass2[i],kin2[i],tensor2[i],zdir='z',s=1,c='r')
        plt.scatter(kin2[i], tensor2[i], edgecolors='r', facecolors='r')
    #if check3[i]>0.0:
        #plt.scatter(mass3[i], tensor3[i], edgecolors='k', facecolors='none')
#ax.set_xlabel('Mass')
plt.ylabel('Tensor, alpha')
#ax.set_ylabel('Kineticity, alpha')
#ax.set_zlabel('Tensor, alpha')
plt.xlabel('Kineticit, alpha')
plt.show()
#plt.savefig('mass_tensor_neg_dep.png')
'''
