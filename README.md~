# RegionGrowingAlgorithm

1. This algorithm is used in object segmentation based on user-choosen seed pixels.
2. This [paper](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.59.8092&rep=rep1&type=pdf) describes the method presented in the code.

## Requirements

1. This module needs Python 2.x, [Numpy](http://www.scipy.org/scipylib/download.html), [SciPy](http://www.scipy.org/scipylib/download.html), [datetime](https://docs.python.org/2/library/datetime.html)

## Citations

*Vezhnevets, Vladimir, and Vadim Konouchine. "GrowCut: Interactive multi-label ND image segmentation by cellular automata." proc. of Graphicon. Vol. 1. 2005.* 

## Usage

### General usage

	$ python regiongrowingca.py sample/star-white-clipart.jpg sample/seeds

runs with threshold (`-t`) of $0.5$ and number of iterations (`-i`) of $50$ as default

From terminal

	$ python regiongrowingca.py sample/star-white-clipart.jpg sample/seeds -t 0.7 -i 75

reads ``sample/star-white-clipart.jpg`` from sample folder with seeds given in an utf-8 encoded file as like ``sample/seeds`` with threshold of $0.7$ and number of iterations as $75$

Seeds are be of assumed format
	
	n1,n2
	n3,n4
	...
Run
	
	$ python regiongrowingca.py -h

for help regarding arguments
