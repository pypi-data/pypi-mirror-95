Resting state HRF estimation and deconvolution.
========
[![PyPI version](https://badge.fury.io/py/rsHRF.png)](https://badge.fury.io/py/rsHRF)

Please refer to https://github.com/compneuro-da/rsHRF for MATLAB version

![BOLD HRF](https://github.com/guorongwu/rsHRF/raw/master/docs/BOLD_HRF.png)


The basic idea 
-------------

This toolbox is aimed to retrieve the onsets of pseudo-events triggering an hemodynamic response from resting state fMRI BOLD voxel-wise signal.
It is based on point process theory, and fits a model to retrieve the optimal lag between the events and the HRF onset, as well as the HRF shape, using either the canonical shape with two derivatives, or a (smoothed) Finite Impulse Response.

![BOLD HRF](http://users.ugent.be/~dmarinaz/example_hrf.png)

Once that the HRF has been retrieved for each voxel, it can be deconvolved from the time series (for example to improve lag-based connectivity estimates), or one can map the shape parameters everywhere in the brain (including white matter), and use the shape as a pathophysiological indicator.

![HRF map](http://users.ugent.be/~dmarinaz/FIR_Height_full_layout.png)

How to use the toolbox 
-------------

The input is voxelwise BOLD signal, already preprocessed according to your favorite recipe. Important thing are:

* bandpass filter in the 0.01-0.08 Hz interval (or something like that)
* z-score the voxel BOLD time series

To be on the safe side, these steps are performed again in the code.

The input can be images (3D or 4D), or directly matrices of [observation x voxels].

It is possible to use a temporal mask to exclude some time points (for example after scrubbing).

The demos allow you to run the analyses on several formats of input data.

Python Package and BIDS-app 
-------------
A BIDS-App has been made for easy and reproducible analysis. Its documentation can be accessed at:

http://bids-apps.neuroimaging.io/rsHRF/

Collaborators 
-------------
* Guorong Wu
* Nigel Colenbier
* Sofie Van Den Bossche
* Daniele Marinazzo

* Madhur Tandon (Python - BIDS)
* Asier Erramuzpe (Python - BIDS)
* Amogh Johri   (Python - BIDS)


**References**
--------

1. Guo-Rong Wu, Wei Liao, Sebastiano Stramaglia, Ju-Rong Ding, Huafu Chen, Daniele Marinazzo*. "A blind deconvolution approach to recover effective connectivity brain networks from resting state fMRI data." Medical Image Analysis, 2013, 17:365-374. [PDF](https://github.com/guorongwu/rsHRF/raw/master/docs/2013_MIA.pdf)

2. Guo-Rong Wu, Daniele Marinazzo. "Sensitivity of the resting state hemodynamic response function estimation to autonomic nervous system fluctuations." Philosophical Transactions of the Royal Society A, 2016, 374: 20150190. [PDF](https://github.com/guorongwu/rsHRF/raw/master/docs/2016_PTA.pdf)

3. Guo-Rong Wu, Daniele Marinazzo. "Retrieving the Hemodynamic Response Function in resting state fMRI: methodology and applications." PeerJ PrePrints, 2015. [PDF](https://github.com/guorongwu/rsHRF/raw/master/docs/poster_OHBM2016_HRF.pdf)
