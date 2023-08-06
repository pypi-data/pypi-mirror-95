# pyPcazip: PCA-based trajectory file compression. #


pyPcazip uses Principal Component Analysis (PCA) to compress molecular dynamics (MD) trajectory files.

The approach is (controllably) lossy, but in the right situations is very effective:

* When the system behaviour is not diffusive (avoid ions and solvent).
* When the trajectory is free of periodic boundary condition artifacts.
* When loss of information about global translation and rotation is not an issue.

The current code (V3) is a complete re-write of the previous version (V2) and incompatible with it. For information about V2,
please see the [Wiki]((https://bitbucket.org/ramonbsc/pypcazip/wiki/Home).

## Background:

Taking a trajectory as a \[n_frames, n_coordinates] 2D array (n_coordinates=3\*n_atoms), PCA allows this to be
deconstructed into an \[n_scores, n_coordinates] 2D array of *eigenvectors* plus an \[n_frames, n_scores] 2D 
array of *scores* (where typically, n_scores << n_coordinates), plus an \[n_coordnates] vector for the *mean* structure (global translation and rotation of the system
being, conventionally, removed prior to analysis).

The total number of values in the trajectory is (n_frames * n_coordinates), in the PCA deconstruction this becomes
(n_scores * n_coordinates + n_frames * n_scores + n_coordinates). So if we have a trajectory of 10000 frames, 
each of 600 coordinates, that by PCA can be represented to satisfactory accuracy by, say, 200 scores, then:

    Original size = 600 * 10000 = 6,000,000
    Compressed size = 600 * 200 + 10000 * 200 + 600 = 2,120,600

I.e, PCA has the potential to achieve a about 3-fold compression.

PyPcazip implements this strategy, in addition using data compression techniques (similar to those used in the GROMACS xtc
format) to achive even smaller file sizes.


## Installation

From pip:

    pip install pypcazip
	
## Usage:

To compress a trajectory file:

    pyPcazip traj.xtc traj.pcz
	
To uncompress a trajectory file:

    pyPcaunzip traj.pcz traj.dcd
	
Pypcazip can read and write any of the trajectory file formats supported by [MDTraj](http://mdtraj.org). 
Some file formats may require a compatible parameter/topology file to be available:

    pyPcazip traj.mdcrd traj.pcz -p system.prmtop
	
The tradeoff between compression and loss of accuracy is controlled by telling pyPcazip the fraction of the
total variance you wish to capture (i.e., a number between 0 - 1, the default is 0.95):

    pyPcazip traj.nc traj.pcz -q 0.98


## Who do I talk to? ##

* charles.laughton@nottingham.ac.uk (This version)
* ardita.shkurti@nottingham.ac.uk (Previous versions, Repo admin)
* rgoni@mmb.pcb.ub.es (Previous versions, Repo owner/admin)

## Other contributors: ##

* e.breitmoser@epcc.ed.ac.uk
* ibethune@epcc.ed.ac.uk
* kwabenantim@yahoo.com

![logos.jpg](https://bitbucket.org/repo/XRMEjz/images/965878357-logos.jpg)