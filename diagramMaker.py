import matplotlib.pyplot as plt


def box_plotter(title, list_of_lists, labels):
    colors = ["ivory", "antiquewhite", "wheat", "peachpuff"]

    fig, ax = plt.subplots()
    ax.set_ylabel("number")

    bplot = ax.boxplot(list_of_lists, patch_artist=True, tick_labels=labels)

    # Colours!
    for patch, color in zip(bplot["boxes"], colors):
        patch.set_facecolor(color)

    plt.savefig(f"Diagrams/{title}_box_plot.png")


def histogramer(title, list_of_lists, labels):
    colors = ["ivory", "antiquewhite", "wheat", "peachpuff"]

    num_dists = len(list_of_lists)
    fig, axs = plt.subplots(1, num_dists, figsize=(5 * num_dists, 4), tight_layout=True)

    if num_dists == 1:
        axs = [axs]

    # Plot histograms
    for i in range(num_dists):
        axs[i].hist(list_of_lists[i], bins=20, color=colors[i], edgecolor="black")
        if labels:
            axs[i].set_title(f"{title} {labels[i]}")
        axs[i].set_xlabel("Value")
        axs[i].set_ylabel("Frequency")

    plt.savefig(f"Diagrams/{title}_histogram.png")
