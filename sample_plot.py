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

#load your files first


#triangle plot for contours and posteriors if have 4 parameters, as an example
#this whole thing can be put in a loop and have functions defined to get rid of lines of code
fig1, ax1 = plt.subplots(figsize=(13.424,8))
ax2 = plt.subplot(4,4,13) #this part could be automated instead of hard coded
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

#The following lines interpolate the histogram to obtain the posterior distribution for my particular problem. We will approach this differently.
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

#The following lines interpolate the histogram to obtain the posterior distribution for my particular problem. We will approach this differently.
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

#The following lines interpolate the histogram to obtain the posterior distribution for my particular problem. We will approach this differently.
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

#The following lines interpolate the histogram to obtain the posterior distribution for my particular problem. We will approach this differently.
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

#The following lines interpolate the histogram to obtain the posterior distribution for my particular problem. We will approach this differently.
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

#The following lines interpolate the histogram to obtain the posterior distribution for my particular problem. We will approach this differently.
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

#The following lines interpolate the histogram to obtain the posterior distribution for my particular problem. We will approach this differently.
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
#save the figure to a file
fig1.savefig('paper/figs/Kpt1_stability_tri_new_colors_posteriors.png', bbox_inches='tight')
