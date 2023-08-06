**Author:** Matthias Bieg

# hmap: Python Heatmap Package

This package implements a convenient heatmap plotting package in python. It offers low level functions for

1. Plotting
	- Heatmaps
	- Dendrograms
	- Annotations
	- Legends
2. Figure layouting

## Clustered heatmap

![Clustered Heatmap](jupyter_notebooks/pics/clustered_heatmap.jpeg)

## Grouped clustered heatmap

![Grouped Clustered Heatmap](jupyter_notebooks/pics/grouped_clustered_heatmap.jpeg)

## Figure layout
The hmap package comes with a module for defining the layout of a figure using absolute length measurements. Currently the only unit supported is milimeters. The layout of a figure is defined as a grid. You have to specify 
- the number of rows, 
- the number of columns, 
- the widths of the columns,
- the heights of the rows,
- the vertical distance between adjacent rows, 
- the horizontal distance between adjacent columns,
- the size of the bottom border margin,
- the size of the top border margin,
- the size of the left border margin, and
- the size of theright border margin
As said before, the sizes are given in milimeters.

### Example

```python
import sys
import hmap
import matplotlib.pyplot as plt

fig, gs = hmap.layout.layout.layoutGrid(4, 5, [10., 2., 40., 40., 40], [10., 2., 40., 40.], 1., 1., 20., 15., 15., 20.)
col_widths = ["10 mm", "2 mm", "40 mm", "40 mm", "40 mm"]
row_heights = ["10 mm", "2 mm", "40 mm", "40 mm"]

for row_idx in range(4):
    for col_idx in range(5):
        ax = plt.subplot(gs[row_idx, col_idx])
        plt.xticks([], [])
        plt.yticks([], [])
        if(row_idx == 0):
            ax.xaxis.set_label_position("top")
            plt.xlabel(col_widths[col_idx], 
                       fontsize=7, 
                       rotation=90)
        if(col_idx == 0):
            plt.ylabel(row_heights[row_idx], 
                       fontsize=7, 
                       rotation=0, 
                       horizontalalignment="right",
                       verticalalignment="center")
```

![Figure layout](jupyter_notebooks/pics/figure_layout.jpeg)

# Installation
```bash
pip install hmap
```

# Usage Example
Please check the [jupyter notebook](jupyter_notebooks/hmap_example.ipynb) for an example of how to use hmap.

# Acknowledgements
This package was implemented during my time at the *German Cancer Research Center* in the group of *Theoretical Bioinformatics* headed by Prof. Dr. Roland Eils, where i was part of the core bioinformatics team of the *Heidelberg Institute of Personalized Oncology (HIPO)*. Further refinment and final upload to PyPI was done during my time at *Charite, Universitaetsmedizin Berlin, Berlin Institute of Health (BIH) in the Department of Digital Health* headed by Prof. Roland Eils.

# License
Copyright (c) 2021, Matthias Bieg

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
