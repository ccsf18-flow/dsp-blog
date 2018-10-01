from data import WINDOW_SIZE, fs
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np

def plot_waterfall(waterfall, x_slice, y_slices, outf, show_angles=True):
    nys = len(y_slices)

    # Set up the figure and all the axes we will need
    fig = plt.figure(figsize=(8,8))

    gs = GridSpec(3 + len(y_slices), 4)
    ax_joint = fig.add_subplot(gs[nys:3+nys, 0:3])
    y_slice_axes = list(map(lambda y: fig.add_subplot(gs[y, 0:3], sharex=ax_joint), range(len(y_slices))))
    ax_marg_y = fig.add_subplot(gs[nys:3+nys, 3], sharey=ax_joint)


    # Link up all the axes
    ax_joint.autoscale(False)
    ax_joint.set_ylim((0, waterfall.shape[0]))
    ax_joint.set_xlim((0, waterfall.shape[1]))

    # Plot the actual waterfall
    ax_joint.imshow(waterfall, aspect='auto')
    ax_joint.set_yticklabels(map(str, np.linspace(0, fs / 2, 7)))
    ax_joint.set_ylabel('Frequency (Hz)')
    ax_joint.set_xlabel('Time (samples / ' + str(WINDOW_SIZE) + ')' )

    # Plot the slice on the right side
    hx = waterfall[:,x_slice]
    hx_norm = np.abs(hx) / WINDOW_SIZE
    t = np.linspace(0, waterfall.shape[0], waterfall.shape[0])

    ax_marg_y.get_yaxis().set_visible(False);

    norm_plot = ax_marg_y
    angle_plot = None
    if show_angles:
        angle_plot = ax_marg_y
        norm_plot = angle_plot.twiny()

    normcolor = 'purple'
    anglecolor = 'blue'
    if not show_angles:
        normcolor = 'black'

    norm_plot.set_xlim(0, np.max(hx_norm) * 1.1)
    norm_plot.get_yaxis().set_visible(False)
    norm_plot.tick_params(axis='x', labelcolor=normcolor)

    ax_marg_y.plot(
        hx_norm,
        np.linspace(0, waterfall.shape[0], waterfall.shape[0])
    )

    if angle_plot:
        angle_plot.set_xlim(0, 180)
        angle_plot.get_yaxis().set_visible(False)
        angle_plot.tick_params(axis='x', labelcolor=anglecolor)
        angle_plot.plot(
            np.abs(np.angle(hx, deg=True)),
            t,
            color=anglecolor,
            label='angle(dft(f))'
        )
    norm_plot.plot(
        hx_norm,
        t,
        color=normcolor,
        label='mag(dft(f))'
    )

    # Plot all the slices from the top
    for y, s in enumerate(y_slices):
        hx = waterfall[s, :]
        hx_norm = np.abs(hx) / WINDOW_SIZE

        y_slice_axes[nys - y - 1].set_title(str(int (s * fs / (4 * len(hx)))) + ' Hz')

        angle_plot = None
        norm_plot = y_slice_axes[nys - y - 1]
        if show_angles:
            angle_plot = y_slice_axes[nys - y - 1]
            norm_plot = angle_plot.twinx()

        norm_plot.set_ylim(0, np.max(hx_norm) * 1.1)
        norm_plot.get_xaxis().set_visible(False);
        norm_plot.tick_params(axis='y', labelcolor=normcolor)
        norm_plot.plot(
            hx_norm,
            color=normcolor,
            label='mag(dft(f))'
        )

        if show_angles:
            angle_plot.plot(
                np.abs(np.angle(hx, deg=True)),
                color=anglecolor,
                label='angle(dft(f))'
            )
            angle_plot.set_ylim(0, 180)
            angle_plot.get_xaxis().set_visible(False);
            angle_plot.tick_params(axis='y', labelcolor=anglecolor)

        ax_joint.axhline(y=s, color='red')

    ax_joint.axvline(x=x_slice, color='red')

    fig.tight_layout()

    plt.savefig(outf, bbox_inches='tight', dpi=fig.dpi)
