import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import h5py
from IPython.display import display
import os


class array_error(Exception):
    pass

def load_and_plot_weighted_histogram(hdf_file, observable_name, weight_name='weights_nominal', bins=20,
                                     title='weighted distribution', xlabel='observable', ylabel='weighted count'):
    """
    Parameters:
    hdf_file: (file_path) the exact file path of the hdf5 file
    observable_name: (str) the physical quantity which needs to be plotted on ewighted histogram
    weight_name: (str) the per event weights array
    bins: default = 20
    title: the title of the histogram
    xlabel: the label for x axis
    ylabel: the label for y axis

    Here's how my function works:
    step0: wrapping the core logic of weighted histogram plotting into a helper function
    step1: Accessing the relevant observable and weigths column
        step1.1: looping through the blocks searching for name of the observable and weights columns among column names
        step1.2: if found, save the observable and weights columns as numpy arrays. Else, throw a user friendly error..
    step2: perform sanity checks and cleaning to ensure no problems would arise when we start plotting the histogram
        step2.1: removing all (observable, weight) with NaN values
        
    step3: plot the weighted histogram
        step3.1: if bins = "auto" chosen. Calculate number of bins using friedman diaconis rule. Else just use the specified number of bins
    step4: keeping an alternate test suite function to ensure the function works and doesnt break even when it faces edge cases
    """


    def compute_histogram(obs, wts, bins):
        obs = np.asarray(obs)
        wts = np.asarray(wts)
        
        if len(obs) != len(wts):
            raise array_error("Observables and weights must have the same length")
        
        # this is a subroutine to filter out all (observable, weight) pairs where even one is an NaN value 
        # x: cleaned observable array
        # w: cleaned weights array 
        mask = np.isfinite(obs) & np.isfinite(wts)
        x = obs[mask]
        w = wts[mask]
        N = len(x)
        
        if N == 0:
            raise ValueError("No valid data points after cleaning")
        
        
        w_sum = np.sum(w)
        mean = np.sum(w * x) / w_sum
        var = np.sum(w * (x - mean)**2) / w_sum
        std = np.sqrt(var)
        skew = np.sum(w * (x - mean)**3) / (w_sum * std**3 + 1e-12)
        
        
        # Below binning method uses the freedman diaconis rule
        # The rule chooses an appropriate number of bins without getting affected by outliers 
        # this method is very ideal for non normal distributions...
        if bins == "auto":
            q75, q25 = np.percentile(x, [75,25])
            iqr = q75 - q25
            if iqr == 0:
                bins = int(np.sqrt(N))
            else:
                bin_width = 2 * iqr / (N ** (1/3))
                bins = int((x.max() - x.min()) / bin_width)
            if abs(skew) > 1:
                bins = int(bins * 1.5)
            bins = max(20, min(500, bins))
        
        counts, bin_edges = np.histogram(x, bins=bins, weights=w)
        
        df = pd.DataFrame({
            "bin_left": bin_edges[:-1],
            "bin_right": bin_edges[1:],
            "weighted_counts": counts
        })
        
        return counts, bin_edges, bins, skew, df, x, w  # return x,w for plotting
    
    # HDF5 file reading routine
    # important assumption about the dataframe components:
    # the dataframe conpnents are nested inside df which is itself nested inside the .h5 file
    # This assumption is very important as other users of this funciton will need to structure their .h5 file in a similar
    # way almost like a convention. This could be inconvenient and that is why i wrapped the plottign routine inside the helper function
    #  as it is reusable.
    with h5py.File(hdf_file, 'r') as f:
        obs, wts = None, None
        block_num = 0
        while f'/df/block{block_num}_items' in f:
            block_cols = f[f'/df/block{block_num}_items'][()]
            if block_cols.dtype.kind in {'S','O'}:
                block_cols = block_cols.astype(str)
            if observable_name in block_cols:
                col_idx = np.where(block_cols == observable_name)[0][0]
                obs = f[f'/df/block{block_num}_values'][:, col_idx]
            if weight_name in block_cols:
                col_idx = np.where(block_cols == weight_name)[0][0]
                wts = f[f'/df/block{block_num}_values'][:, col_idx]
            block_num += 1

    if obs is None:
        raise ValueError(f"Observable '{observable_name}' not found in any block.")
    if wts is None:
        raise ValueError(f"Weight '{weight_name}' not found in any block.") 
    
    
    counts, bin_edges, bins_used, skew, df, x, w = compute_histogram(obs, wts, bins)
    
    # plotting routine using matplotlib
    plt.figure(figsize=(8,6))
    plt.hist(x, bins=bin_edges, weights=w, histtype='stepfilled',
             alpha=0.6, color='skyblue', edgecolor='navy',
             label=f'Weighted Data (bins={bins_used})')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(axis='y', alpha=0.3)
    plt.legend()
    plt.show()

    print(f"Auto binning selected {bins_used} bins | skewness = {skew:.2f} | N = {len(x)}")
    display(df)
    
    return



def test_weighted_histogram():
    """
    Test function(automated) for load_and_plot_weighted_histogram's core logic.
    """
    
    # Helper: mimic the internal compute_histogram
    # (it is the clone of the compute_histogram function in load_and_plot_weighted_histogram function)
    def compute_histogram(obs, wts, bins="auto"):
        mask = np.isfinite(obs) & np.isfinite(wts)
        x = np.array(obs)[mask]
        w = np.array(wts)[mask]
        N = len(x)
        if N == 0:
            raise ValueError("No valid data points")
        
        w_sum = np.sum(w)
        mean = np.sum(w*x)/w_sum
        var = np.sum(w*(x-mean)**2)/w_sum
        std = np.sqrt(var)
        skew = np.sum(w*(x-mean)**3)/(w_sum*std**3 + 1e-12)
        
        if bins == "auto":
            q75,q25 = np.percentile(x,[75,25])
            iqr = q75-q25
            if iqr == 0:
                bins = int(np.sqrt(N))
            else:
                bin_width = 2*iqr/(N**(1/3))
                bins = int((x.max()-x.min())/bin_width)
            if abs(skew)>1:
                bins = int(bins*1.5)
            bins = max(20,min(500,bins))
        
        counts, edges = np.histogram(x,bins=bins,weights=w)
        return counts, edges, bins, skew, x, w

    #  TEST CASES
    # I will use assert because even if one of the test fails the code cell will get interrupted from running and will throw an assertion error

    # 1.Basic weighted counts
    obs = [0,1,2,3]
    wts = [1,2,1,1]
    counts, edges, bins_used, skew, x, w = compute_histogram(obs, wts)
    assert counts.sum() == sum(wts)
    assert len(edges) == bins_used + 1

    # 2. NaN handling
    obs = [0,np.nan,1]
    wts = [1,1,1]
    counts, edges, bins_used, skew, x, w = compute_histogram(obs,wts)
    assert np.isfinite(x).all()
    assert len(x) == 2



    # 4. Delta-function peak (all values same)
    obs = [0]*10
    wts = [1]*10
    counts, edges, bins_used, skew, x, w = compute_histogram(obs,wts,"auto")
    assert counts.sum() == 10
    assert bins_used >= 20 and bins_used <= 500

    # 5. Right-skewed distribution
    obs = [1,2,3,10,20]
    wts = [1]*5
    counts, edges, bins_used, skew, x, w = compute_histogram(obs,wts,"auto")
    assert counts.sum() == 5
    assert skew > 0  # should be right-skewed

    # 6. Symmetric distribution around 0
    obs = [-2,-1,0,1,2]
    wts = [1]*5
    counts, edges, bins_used, skew, x, w = compute_histogram(obs,wts,"auto")
    assert abs(skew) < 1  # roughly symmetric

    # 7. Very small dataset (it should autobin lower limit)
    obs = [0,1]
    wts = [1,1]
    counts, edges, bins_used, skew, x, w = compute_histogram(obs,wts,"auto")
    assert bins_used >= 20

    # 8. Very large dataset (it should autobin upper limit)
    obs = np.arange(10000)
    wts = np.ones_like(obs)
    counts, edges, bins_used, skew, x, w = compute_histogram(obs,wts,"auto")
    assert bins_used <= 500

    print("All automated tests passed!")

"""
I used assert because even if one of the test fails, 
the code cell will get interrupted from running and will throw an assertion error

As can be seen, i included tests to checkwhether the function would behave as
expected under different kinds of edge cases like:
0. Basic check whether weights actually sum up to the expected number
1. When there are NaN values (removed such events)
2. The dataset is too large or too small (autobinned to appropriate limit)
3. Does the function recognise symmetry or skewness of the dataset (yes it does!)

"""

# Run the tests


# Just the run the file and see the results :)
load_and_plot_weighted_histogram(hdf_file="multifold.h5", observable_name='y_trackj2')
test_weighted_histogram()