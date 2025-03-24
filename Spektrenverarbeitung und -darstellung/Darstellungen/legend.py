import matplotlib.pyplot as plt
from Variables.constants import CATEG_PALETTE, DIAG_KATEG_NAMEN, REF_COLORS

def create_legend():
    colors = CATEG_PALETTE
    labels = DIAG_KATEG_NAMEN

    # Create a blank figure
    fig, ax = plt.subplots(figsize=(6, 2))  # Adjust size for better fit

    # Create proxy artists for the legend
    handles = [plt.Line2D([0], [0], color=color, lw=4) for color in colors]

    # Add legend to the figure
    legend = ax.legend(handles, labels, loc='center', frameon=False)

    # Remove axes for a cleaner legend-only look
    ax.axis('off')

    return fig, ax

def create_legend_ref(ax):
    colors = REF_COLORS
    labels = [f"Altersgruppe {i}" for i in range(2,6)]

    # Create proxy artists for the legend
    handles = [plt.Line2D([0], [0], color=color, lw=4) for color in colors]

    # Add legend to the figure
    legend = ax.legend(handles, labels, loc='center',
                       prop={'size': 20}, frameon=True)

    # Remove axes for a cleaner legend-only look
    ax.axis('off')

    return ax