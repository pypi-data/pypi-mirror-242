# %%
import matplotlib.pyplot as plt

def plot(*args,**kwargs):
    """Wrapper for pyplot with better defaults.
    """
    fig, ax = plt.subplots(dpi=150)
    ax.plot(*args,**kwargs)
    ax.grid()
    if 'label' in kwargs:
        ax.legend()
    return fig, ax

def multiplot(xx,ydict,**kwargs):
    """Plot multiple y values on the same axis.

    Args:
        xx (array): x-axis values.
        ydict (dict[array]): Dictionary of y-values with the keys being the legend labels.
    """
    fig, ax = None, None
    for k,v in ydict.items():
        if ax is None:
            fig, ax = plot(xx,v,label=k,**kwargs)
            continue
        ax.plot(xx,v,label=k)
    ax.legend()
    return fig, ax
