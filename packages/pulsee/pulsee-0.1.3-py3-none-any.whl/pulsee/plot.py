from fractions import Fraction

import matplotlib.pylab as plt
import numpy as np
from matplotlib import colorbar as clrbar, colors as clrs
from matplotlib.patches import Patch
from matplotlib.pyplot import xticks, yticks
from qutip import Qobj


def plot_power_absorption_spectrum(
        frequencies,
        intensities,
        show=True,
        xlim=None,
        ylim=None,
        fig_dpi=400,
        save=False,
        name="PowerAbsorptionSpectrum",
        destination="",
):
    """
    Plots the power absorption intensities as a function of the corresponding
    frequencies.

    Parameters
    ----------
    frequencies : array-like
        Frequencies of the transitions (in MHz).

    intensities : array-like
        Intensities of the transitions (in a.u.).

    show : bool
        When False, the graph constructed by the function will not be
        displayed.

        Default value is True.

    xlim : 2-element iterable or `None`
        Lower and upper x-axis limits of the plot.
        When `None` uses `matplotlib` default.

    ylim : 2-element iterable or `None`
        Lower and upper y-axis limits of the plot.
        When `None` uses `matplotlib` default.

    fig_dpi : int
        Image quality of the figure when showing and saving. Useful for
        publications. Default set to very high value.

    save : bool
        When False, the plotted graph will not be saved on disk. When True,
        it will be saved with the name passed as name and in the directory
        passed as destination.

        Default value is False.

    name : string
        Name with which the graph will be saved.
        Default value is 'PowerAbsorptionSpectrum'.

    destination : string
        Path of the directory where the graph will be saved (starting
        from the current directory). The name of the directory must
        be terminated with a slash /.

        Default value is the empty string (current directory).

    Action
    ------
    If show=True, generates a graph with the frequencies of transition on the
    x-axis and the corresponding intensities on the y-axis.

    Returns
    -------
    An object of the class matplotlib.figure.Figure representing the figure
    built up by the function.
    """
    fig = plt.figure()

    plt.vlines(frequencies, 0, intensities, colors="b")
    plt.xlabel("\N{GREEK SMALL LETTER NU} (MHz)")
    plt.ylabel("Power absorption (a.u.)")

    if xlim is not None:
        plt.xlim(left=xlim[0], right=xlim[1])
    if ylim is not None:
        plt.xlim(left=ylim[0], right=ylim[1])
    if save:
        plt.savefig(destination + name, dpi=fig_dpi)
    if show:
        plt.show()

    return fig


def plot_real_part_density_matrix(
        dm,
        many_spin_indexing=None,
        show=True,
        fig_dpi=400,
        save=False,
        xmin=None,
        xmax=None,
        ymin=None,
        ymax=None,
        show_legend=True,
        name="RealPartDensityMatrix",
        destination="",
):
    """
    Generates a 3D histogram displaying the real part of the elements of the
    passed density matrix.

    Parameters
    ----------
    dm : Qobj / numpy array as a square matrix
        Density matrix to be plotted.

    many_spin_indexing : None or list
        If not None, the density matrix dm is interpreted as the state of
        a many spins' system, and this parameter provides the list of the
        dimensions of the subspaces of the full Hilbert space related to the
        individual nuclei of the system.
        The ordering of the elements of many_spin_indexing should match that of
        the single spins' density matrices in their tensor product
        resulting in dm. Default value is None.

    show : bool
        When False, the graph constructed by the function will not be
        displayed.
        Default value is True.

    fig_dpi : int
        Image quality of the figure when showing and saving. Useful for
        publications. Default set to very high value.

    save : bool
        When False, the plotted graph will not be saved on disk. When True,
        it will be saved with the name passed as name and in the directory
        passed as destination.
        Default value is False.

    xmin, xmax, ymin, ymax : float
        Set axis limits of the graph.

    name : string
        Name with which the graph will be saved.
        Default value is 'RealPartDensityMatrix'.

    destination : string
        Path of the directory where the graph will be saved (starting
        from the current directory). The name of the directory must
        be terminated with a slash /.
        Default value is the empty string (current directory).

    Action
    ------
    If show=True, draws a histogram on a 2-dimensional grid representing the
    density matrix, with the real part of each element indicated along the z
    axis. Blue bars indicate the positive matrix elements, red bars indicate the
    negative elements in absolute value.

    Returns
    -------
    An object of the class matplotlib.figure.Figure and an object of the class
    matplotlib.axis.Axis representing the figure built up by the function.

    """
    real_part = np.vectorize(np.real)
    if isinstance(dm, Qobj):
        data_array = real_part(dm)
    else:
        data_array = real_part(dm)

    # Create a figure for plotting the data as a 3D histogram.
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # Create an X-Y mesh of the same dimension as the 2D data
    # You can think of this as the floor of the plot
    x_data, y_data = np.meshgrid(np.arange(data_array.shape[1]) + 0.25, np.arange(data_array.shape[0]) + 0.25)

    # Set width of the vertical bars
    dx = dy = 0.5

    # Flatten out the arrays so that they may be passed to "ax.bar3d".
    # Basically, ax.bar3d expects three one-dimensional arrays: x_data, y_data, z_data. The following
    # call boils down to picking one entry from each array and plotting a bar from (x_data[i],
    # y_data[i], 0) to (x_data[i], y_data[i], z_data[i]).
    x_data = x_data.flatten()
    y_data = y_data.flatten()
    z_data = data_array.flatten()

    bar_color = np.zeros(len(z_data), dtype=object)

    for i in range(len(z_data)):
        if z_data[i] < -1e-10:
            bar_color[i] = "tab:red"
        else:
            bar_color[i] = "tab:blue"

    ax.bar3d(x_data, y_data, np.zeros(len(z_data)), dx, dy, np.absolute(z_data), color=bar_color)

    d = data_array.shape[0]
    tick_label = []

    if not many_spin_indexing:
        many_spin_indexing = dm.dims[0]

    d_sub = many_spin_indexing
    n_sub = len(d_sub)
    m_dict = []

    for i in range(n_sub):
        m_dict.append({})
        for j in range(d_sub[i]):
            m_dict[i][j] = str(Fraction((d_sub[i] - 1) / 2 - j))

    for i in range(d):
        tick_label.append(">")

    for i in range(n_sub)[::-1]:
        d_downhill = int(np.prod(d_sub[i + 1: n_sub]))
        d_uphill = int(np.prod(d_sub[0:i]))

        for j in range(d_uphill):
            for k in range(d_sub[i]):
                for l in range(d_downhill):
                    comma = ", "
                    if j == n_sub - 1:
                        comma = ""
                    tick_label[j * d_sub[i] * d_downhill + k * d_downhill + l] = (
                            m_dict[i][k] + comma + tick_label[j * d_sub[i] * d_downhill + k * d_downhill + l]
                    )

    for i in range(d):
        tick_label[i] = "|" + tick_label[i]

    ax.tick_params(axis="both", which="major", labelsize=6)
    xticks(np.arange(start=0.5, stop=data_array.shape[0] + 0.5), tick_label)
    yticks(np.arange(start=0.5, stop=data_array.shape[0] + 0.5), tick_label)

    ax.set_zlabel("Re(\N{GREEK SMALL LETTER RHO})")
    legend_elements = [
        Patch(facecolor="tab:blue", label="<m|\N{GREEK SMALL LETTER RHO}|m> > 0"),
        Patch(facecolor="tab:red", label="<m|\N{GREEK SMALL LETTER RHO}|m> < 0"),
    ]
    if show_legend:
        ax.legend(handles=legend_elements, loc="upper left")

    if (xmin is not None) and (xmax is not None):
        plt.xlim(xmin, xmax)
    if (ymin is not None) and (ymax is not None):
        plt.ylim(ymin, ymax)

    if save:
        plt.savefig(destination + name, dpi=fig_dpi)

    if show:
        plt.show()

    return fig, ax


def complex_phase_cmap():
    """
    Create a cyclic colormap for representing the phase of complex variables

    From QuTiP 4.0:
    https://qutip.org

    Returns
    -------
    cmap : A matplotlib linear segmented colormap.
    """
    cdict = {
        "blue": ((0.00, 0.0, 0.0), (0.25, 0.0, 0.0), (0.50, 1.0, 1.0), (0.75, 1.0, 1.0), (1.00, 0.0, 0.0)),
        "green": ((0.00, 0.0, 0.0), (0.25, 1.0, 1.0), (0.50, 0.0, 0.0), (0.75, 1.0, 1.0), (1.00, 0.0, 0.0)),
        "red": ((0.00, 1.0, 1.0), (0.25, 0.5, 0.5), (0.50, 0.0, 0.0), (0.75, 0.0, 0.0), (1.00, 1.0, 1.0)),
    }

    cmap = clrs.LinearSegmentedColormap("phase_colormap", cdict, 256)
    return cmap


def plot_complex_density_matrix(
        dm,
        many_spin_indexing=None,
        show=True,
        phase_limits=None,
        phi_label=r"$\phi$",
        show_legend=True,
        fig_dpi=400,
        save_to="",
        figsize=None,
        labelsize=6,
        elev=45,
        azim=-15,
):
    """
    Generates a 3D histogram displaying the amplitude and phase (with colors)
    of the elements of the passed density matrix.

    Inspired by QuTiP 4.0's matrix_histogram_complex function.
    https://qutip.org

    Parameters
    ----------
    dm : Qobj
        Density matrix to be plotted.

    many_spin_indexing : None or list
        If not None, the density matrix dm is interpreted as the state of
        a many spins' system, and this parameter provides the list of the
        dimensions of the subspaces of the full Hilbert space related to the
        individual nuclei of the system.
        The ordering of the elements of many_spin_indexing should match that of
        the single spins' density matrices in their tensor product resulting in dm.

        For example, a system of [spin-1/2 x spin-1 x spin-3/2] will correspond to:
        many_spin_indexing = [2, 3, 4]

        Default value is None.

    show : bool
        When False, the graph constructed by the function will not be
        displayed.
        Default value is True.

    phase_limits : list/array of two floats
        The phase-axis (colorbar) limits [min, max]

    phi_label : str
        Label for the legend for the angle of the complex number.

    show_legend : bool
        Show the legend for the complex angle.

    fig_dpi : int
        Image quality of the figure when showing and saving. Useful for
        publications. Default set to very high value.

    save_to : str
        If this is not the empty string, the plotted graph will be saved to the
        path ('directory/filename') described by this string.

        Default value is the empty string.

    figsize :  (float, float)
         Width, height in inches.
         Default value is the empty string.

    labelsize : int
         Default is 6

    (azim, elev) : (float, float)
         Angle of viewing for the 3D plot.
         Default is (45 deg, -15 deg)

    Action
    ------
    If show=True, draws a histogram on a 2-dimensional grid representing the
    density matrix, with phase sentivit data.

    Returns
    -------
    An object of the class matplotlib.figure.Figure and an object of the class
    matplotlib.axis.Axis representing the figure built up by the function.

    """
    if not isinstance(dm, Qobj):
        raise TypeError("First argument must be an instance of Qobj!")

    if not many_spin_indexing:
        many_spin_indexing = dm.dims[0]

    dm = np.array(dm)

    # Create a figure for plotting the data as a 3D histogram.
    fig = plt.figure()
    if figsize:
        fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection="3d")

    # Create an X-Y mesh of the same dimension as the 2D data
    # You can think of this as the floor of the plot
    x_data, y_data = np.meshgrid(np.arange(dm.shape[1]) + 0.25, np.arange(dm.shape[0]) + 0.25)

    # Set width of the vertical bars
    dx = dy = 0.5

    # Flatten out the arrays so that they may be passed to "ax.bar3d".
    # Basically, ax.bar3d expects three one-dimensional arrays: x_data, y_data, z_data.
    # The following call boils down to picking one entry from each array and plotting a bar from
    # (x_data[i], y_data[i], 0) to (x_data[i], y_data[i], z_data[i]).
    x_data = x_data.flatten()
    y_data = y_data.flatten()
    z_data = dm.flatten()

    if phase_limits:  # check that limits is a list type
        phase_min = phase_limits[0]
        phase_max = phase_limits[1]
    else:
        phase_min = -np.pi
        phase_max = np.pi

    norm = clrs.Normalize(phase_min, phase_max)
    cmap = complex_phase_cmap()
    colors = cmap(norm(np.angle(z_data)))

    ax.bar3d(x_data, y_data, np.zeros(len(z_data)), dx, dy, np.absolute(z_data), color=colors, shade=True)
    ax.view_init(elev=elev, azim=azim)  # rotating the plot so the "diagonal" direction is more clear

    d = dm.shape[0]
    tick_label = []

    d_sub = many_spin_indexing
    n_sub = len(d_sub)
    m_dict = []  # dictionary of labels for the spin orientation "m"

    # For example, for a two spin-1/2 system:
    # m_dict = [{0: '1/2', 1:'-1/2'}, {0: '1/2', 1:'-1/2'}]
    for i in range(n_sub):
        m_dict.append({})
        for j in range(d_sub[i]):
            m_dict[i][j] = str(Fraction((d_sub[i] - 1) / 2 - j))

    for i in range(d):
        tick_label.append(">")

    for i in range(n_sub)[::-1]:
        d_downhill = int(np.prod(d_sub[i + 1:]))
        d_uphill = int(np.prod(d_sub[0:i]))

        for j in range(d_uphill):
            for k in range(d_sub[i]):
                for l in range(d_downhill):
                    comma = ", "
                    if j == n_sub - 1:
                        comma = ""
                    tick_label[(j * d_sub[i] + k) * d_downhill + l] = (
                            m_dict[i][k] + comma + tick_label[(j * d_sub[i] + k) * d_downhill + l]
                    )

    for i in range(d):
        tick_label[i] = "|" + tick_label[i]

    ax.tick_params(axis="both", which="major", labelsize=labelsize)

    xticks(np.arange(start=0.5, stop=dm.shape[0] + 0.5), tick_label)
    yticks(np.arange(start=1.0, stop=dm.shape[0] + 1.0), tick_label)
    if show_legend:
        cax, kw = clrbar.make_axes(ax, location="right", shrink=0.75, pad=0.06)
        cb = clrbar.ColorbarBase(cax, cmap=cmap, norm=norm)
        cb.set_ticks([-np.pi, -np.pi / 2, 0, np.pi / 2, np.pi])
        cb.set_ticklabels((r"$-\pi$", r"$-\pi/2$", r"$0$", r"$\pi/2$", r"$\pi$"))
        cb.set_label(phi_label)

    if save_to != "":
        plt.savefig(save_to, dpi=fig_dpi)

    if show:
        plt.show()

    return fig, ax


def plot_real_part_FID_signal(
        times,
        FID,
        show=True,
        fig_dpi=400,
        save=False,
        name="FIDSignal",
        destination="",
        xlim=None,
        ylim=None,
        figure=None
):
    """
    Plots the real part of the FID signal as a function of time.

    Parameters
    ----------
    times : array-like
        Sampled instants of time (in microseconds).

    FID : array-like
        Sampled FID values (in arbitrary units).

    show : bool
        When False, the graph constructed by the function will not be
        displayed.
        Default value is True.

    fig_dpi : int
        Image quality of the figure when showing and saving. Useful for
        publications. Default set to very high value.

    save : bool
        When False, the plotted graph will not be saved on disk. When True,
        it will be saved with the name passed as name and in the directory
        passed as destination.
        Default value is False.

    name : string
        Name with which the graph will be saved.
        Default value is 'FIDSignal'.

    destination : string
        Path of the directory where the graph will be saved (starting
        from the current directory). The name of the directory must
        be terminated with a slash /.
        Default value is the empty string (current directory).

    xlim: tuple
        x limits of plot

    ylim: tuple
        y limits of plot

    figure: plt.figure
        figure to plot FID signal on


    Action
    ------
    If show=True, generates a plot of the FID signal as a function of time.

    Returns
    -------
    An object of the class matplotlib.figure.Figure representing the figure
    built up by the function.
    """
    if figure is None:
        fig, ax = plt.subplots()
    else:
        fig, ax = figure

    ax.plot(times, np.real(FID), label="Real part")
    ax.set_title("FID signal")
    ax.set_xlabel("time (\N{GREEK SMALL LETTER MU}s)")
    ax.set_ylabel("Real(FID) (a.u.)")

    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)
    if save:
        plt.savefig(destination + name, dpi=fig_dpi)
    if show:
        plt.show()

    return fig, ax


# If another set of data is passed as fourier_neg, the function plots a couple of graphs, with the
# one at the top interpreted as the NMR signal produced by a magnetization rotating counter-clockwise,
# the one at the bottom corresponding to the opposite sense of rotation
def plot_fourier_transform(
        frequencies,
        fourier,
        fourier_neg=None,
        square_modulus=False,
        xlim=None,
        ylim=None,
        scaling_factor=None,
        norm=True,
        fig_dpi=400,
        show=True,
        save=False,
        name="FTSignal",
        destination="",
        figure=None,
        my_label="",
):
    """
    Plots the Fourier transform of a signal as a function of the frequency.

    Parameters
    ----------
    frequencies : array-like
        Sampled values of frequency (in MHz).

    fourier : array-like
        Sampled values of the Fourier transform (in a.u.).

    fourier_neg : array-like
        Sampled values of the Fourier transform (in a.u.) evaluated
        at the frequencies in frequencies changed by sign.
        Default value is `None`.

    square_modulus : bool
        When True, makes the function plot the square modulus of
        the Fourier spectrum rather than the separate real and
        imaginary parts, which is the default option (by default,
        `square_modulus=False`).

    xlim (ylim) : 2-element iterable or `None`
        Lower and upper x-axis (y-axis) limits of the plot.
        When `None` uses `matplotlib` default.

    scaling_factor : float
        When it is not None, it specifies the scaling factor which
        multiplies the data to be plotted.
        It applies simultaneously to all the plots in the resulting figure.

    norm : Boolean
        Whether to normalize the fourier transform; i.e.,
        scale it such that its maximum value is 1.

    fig_dpi : int
        Image quality of the figure when showing and saving. Useful for
        publications. Default set to very high value.

    show : bool
        When False, the graph constructed by the function will not be
        displayed.
        Default value is `True`.

    save : bool
        When `False`, the plotted graph will not be saved on disk. When `True`,
        it will be saved with the name passed as name and in the directory
        passed as destination.
        Default value is False.

    name : string
        Name with which the graph will be saved.
        Default value is `'FTSignal'`.

    destination : string
        Path of the directory where the graph will be saved (starting from
        the current directory). The name of the directory must be terminated
        with a slash /.
        Default value is the empty string (current directory).

    figure : plt.subplot
        Plot to plot on the fourier transformed frequency

    Action
    ------
    Builds up a plot of the Fourier transform of the passed complex signal as a function of the frequency.
    If fourier_neg is different from None, two graphs are built up which
    represent respectively the Fourier spectra for counter-clockwise and
    clockwise rotation frequencies.

    If show=True, the figure is printed on screen.

    Returns
    -------
    An object of the class matplotlib.figure.Figure and an object of the class
    matplotlib.axis.Axis representing the figure
    built up by the function.
    """
    fourier = np.array(fourier)
    frequencies = np.array(frequencies)

    if fourier_neg is None:
        n_plots = 1
        fourier_data = [fourier]
    else:
        n_plots = 2
        fourier_data = [fourier, fourier_neg]
        plot_title = ["Counter-clockwise precession", "Clockwise precession"]

    if norm:
        for i in range(n_plots):
            fourier_data[i] = fourier_data[i] / np.amax(np.abs(fourier_data[i]))

    if scaling_factor is not None:
        for i in range(n_plots):
            fourier_data[i] = scaling_factor * fourier_data[i]
    if figure is None:
        fig, ax = plt.subplots(n_plots, 1, sharey=True, gridspec_kw={"hspace": 0.5})
    else:
        fig = figure[0]
        ax = figure[1]
    if fourier_neg is None:
        ax = [ax]

    for i in range(n_plots):
        if not square_modulus:
            ax[i].plot(frequencies, np.real(fourier_data[i]), label="Real part " + my_label)
            ax[i].plot(frequencies, np.imag(fourier_data[i]), label="Imaginary part " + my_label)
        else:
            ax[i].plot(frequencies, np.abs(fourier_data[i]) ** 2, label="Square modulus " + my_label)

        if n_plots > 1:
            ax[i].title.set_text(plot_title[i])
        else:
            ax[i].set_title("Frequency Spectrum")

        ax[i].legend(loc="upper left")
        ax[i].set_xlabel("Frequency (MHz)")
        ax[i].set_ylabel("FT signal (a.u.)")

        if xlim is not None:
            ax[i].set_xlim(*xlim)

        if ylim is not None:
            ax[i].set_ylim(*ylim)

    if save:
        plt.savefig(destination + name, dpi=fig_dpi)

    if show:
        plt.show()

    return fig, ax
