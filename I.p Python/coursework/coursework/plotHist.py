import matplotlib.pyplot as plt


class plotHistogram:
    def show_histo(dict, orient="horiz", label="counts", title="title", col=None):
        """Take a dictionary of counts and show it as a histogram."""
        if orient == "horiz":
            bar_fun = plt.barh  # NB: this assigns a function to bar_fun!
            bar_ticks = plt.yticks
            bar_label = plt.xlabel
        elif orient == "vert":
            bar_fun = plt.bar
            bar_ticks = plt.xticks
            bar_label = plt.ylabel
        else:
            raise Exception("show_histo: Unknown orientation: %s ".format % orient)

        n = len(dict)
        bar_fun(range(n), dict.values(), align='center', alpha=0.4, color=col)
        bar_ticks(range(n), dict.keys())
        bar_label(label)
        plt.title(title)
        plt.show()
