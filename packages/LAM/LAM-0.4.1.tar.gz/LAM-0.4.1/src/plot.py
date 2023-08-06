# -*- coding: utf-8 -*-
"""
LAM-module for plot creation.

Created on Tue Mar 10 11:45:48 2020
@author: Arto I. Viitanen
"""

# Standard libraries
import warnings
from itertools import combinations

# Packages
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

# LAM modules
from src.settings import Settings as Sett, Store
import src.logger as lg
import src.system as system
import src.plotfuncs as pfunc

LAM_logger = None


class MakePlot:
    """Create decorated plots."""

    # Base keywords utilized in plots.
    base_kws = {'hue': 'Sample Group', 'row': 'Channel', 'col': 'Sample Group', 'height': 3, 'aspect': 2.5,
                'flier_size': 2, 'title_y': 0.95, 'sharex': False, 'sharey': False, 'gridspec': {'hspace': 0.45},
                'xlabel': 'Linear Position', 'ylabel': 'Feature Count'}
    # Colors for fills
    LScolors = sns.color_palette('Reds', n_colors=4)
    GRcolors = sns.color_palette('Blues', n_colors=4)

    def __init__(self, data, handle, title, sec_data=None):
        self.data = data
        self.sec_data = sec_data
        self.plot_error = False
        self.handle = handle
        self.title = title
        self.g = None
        self.filepath = handle.savepath.joinpath(f"{self.title}.{Sett.saveformat}")

    def __call__(self, func, *args, **kws):
        plot_kws = merge_kws(MakePlot.base_kws, kws)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', category=UserWarning)
            # Make canvas if needed:
            if 'no_grid' not in args:
                self.g = self.get_facet(**plot_kws)
            # Plot data
            self.g = func(self, **plot_kws)
        if self.plot_error:
            msg = "Plot not saved"
            print("INFO: {}".format(msg))
            lg.logprint(LAM_logger, msg, 'w')
            return

        # Adjust plot sizes so that everything fits properly
        fig = plt.gcf()
        if 'adjust' in kws.keys():
            adjust = kws['adjust']
            fig.subplots_adjust(top=adjust.get('top'), bottom=adjust.get('bottom'),
                                right=adjust.get('right'), left=adjust.get('left'),
                                wspace=adjust.get('wspace'), hspace=adjust.get('hspace'))
            if 'hspace' in kws['adjust'].keys():
                fig.subplots_adjust(hspace=kws['adjust'].get('hspace'))
        else:
            fig.subplots_adjust(top=0.85, bottom=0.2, hspace=0.75)
        self.add_elements(*args, **plot_kws)
        self.save_plot()

    def add_elements(self, *args, **kws):
        """Add additional plot elements."""
        if 'centerline' in args:  # Add anchoring point line
            self.centerline()
        if 'ticks' in args:  # Adjust axis ticks
            self.xticks()
        if 'labels' in args:  # Change plot axis labels
            self.collect_labels(kws.get('xlabel'), kws.get('ylabel'))
            self.labels(kws.get('xlabel'), kws.get('ylabel'), kws.get('label_first_only'))
        if 'legend' in args:  # Add legend to plot
            self.g.add_legend()
        if 'title' in args:  # Add title
            self.set_title(**kws)
        if 'stats' in args:  # Include statistics, e.g. neg log or stars
            self.stats(**kws)
        if 'total_stats' in args:  # Add total stat significances
            self.stats_total(**kws)

        # Add detected peaks to plots:
        if isinstance(Store.border_peaks, pd.DataFrame):
            test = not Store.border_peaks.empty
        else:
            test = False
        if 'peaks' in args and Sett.add_peaks and test:
            self.plot_peaks()

        # Make labels visible even when sharing axes
        if kws.get('sharey') == 'row' or kws.get('sharex') == 'col':
            self.visible_labels()

    def centerline(self):
        """Plot centerline, i.e. the anchoring point of samples."""
        if "widths-norm" in self.title:
            line = self.handle.center * 2
        else:
            line = self.handle.center

        for ax in self.g.axes.flat:
            __, ytop = ax.get_ylim()
            ax.vlines(line, 0, ytop, 'dimgrey', zorder=0, linestyles='dashed')

    def collect_labels(self, xlabel, ylabel):
        """Collect plot labels from plot title."""
        if 'collect' not in (xlabel, ylabel):
            return
        # For each plot on canvas
        for ax in self.g.axes.flat:
            # Take apart info in seaborn generated title
            title = ax.get_title()
            var_strs = title.split(' | ')
            label_strs = [lbl.split(' = ')[1] for lbl in var_strs]
            # Collect and set needed labels
            if ylabel == 'collect':
                label = get_unit(label_strs[0])
                ax.set_ylabel(label)
            if xlabel == 'collect':
                label = get_unit(label_strs[1])
                ax.set_xlabel(label)
            ax.set_title(' | '.join(label_strs))

    def get_facet(self, **kws):
        """Create a FacetGrid for plotting."""
        g = sns.FacetGrid(self.data, row=kws.get('row'), col=kws.get('col'), hue=kws.get('hue'),
                          sharex=kws.get('sharex'), sharey=kws.get('sharey'), gridspec_kws=kws.get('gridspec'),
                          height=kws.get('height'), aspect=kws.get('aspect'), legend_out=True, dropna=False,
                          palette=self.handle.palette)
        return g

    def labels(self, xlabel=None, ylabel=None, first=None):
        """Set plot labels based on given strings."""
        for ax in self.g.axes.flat:
            if xlabel not in (None, 'collect'):
                ax.set_xlabel(xlabel)
            if ylabel not in (None, 'collect'):
                ax.set_ylabel(ylabel)
            if first:
                return

    def plot_peaks(self):
        """Add found border regions to plots."""
        peaks = None

        # Select only peaks that belong into groups being plotted
        if 'Sample Group' in self.data.columns:
            groups = self.data.loc[:, 'Sample Group'].unique()
            if isinstance(Store.border_peaks, pd.DataFrame):
                peaks = Store.border_peaks[Store.border_peaks.group.isin(groups)]
        else:
            peaks = Store.border_peaks
        # Add peaks to each plot in figure
        for ax in self.g.axes.flat:
            vmin, vtop = ax.get_ylim()
            vmax = vtop * 0.2
            for peak in peaks.iterrows():
                loc = peak[1]['peak']
                # prom = peak[1]['prominence']
                grp = peak[1]['group']
                color = self.handle.palette[grp]
                # peak location line with prominence
                ax.vlines(x=loc, ymin=vmin, ymax=vmax, color=color, alpha=0.5, linewidth=1.5, zorder=0,
                          linestyle='dashed',)

    def set_title(self, **kws):
        """Set plot title."""
        self.g.fig.suptitle(self.title, weight='bold', y=kws.get('title_y'))

    def stats(self, **kws):
        """Modify plot to include statistics."""
        stats = self.sec_data.stat_data
        __, ytop = plt.ylim()
        tytop = ytop*1.35
        ax = plt.gca()
        ax.set_ylim(top=tytop)
        yaxis = [tytop, tytop]

        # Create secondary axis for significance plotting
        ax2 = plt.twinx()
        lkws = {'alpha': 0.85}
        xmin, xtop = stats.index.min(), stats.index.max()
        ax2.plot((xmin, xtop), (0, 0), linestyle='dashed', color='grey', linewidth=0.85, **lkws)
        # Find top of original y-axis and create a buffer for twin to
        # create a prettier plot
        bottom_add = 2.75*-Sett.ylim
        ax2.set_ylim(bottom=bottom_add, top=Sett.ylim)
        ax2.set_yticks(np.arange(0, Sett.ylim, 10))
        ax2.set_yticklabels(np.arange(0, Sett.ylim, 10))
        ax2.yaxis.set_label_coords(1.04, 0.85)

        # Creation of -log2 P-value axis and line plot
        if Sett.negLog2:
            Sett.stars = False  # Force stars to be False when plotting neglog
            y_val = stats.iloc[:, 7]
            x_val = y_val.index.tolist()
            # Find locations where the log line should be drawn
            ind = y_val[y_val.notnull()].index
            logvals = pd.Series(np.zeros(y_val.shape[0]), index=y_val.index)
            with warnings.catch_warnings():
                warnings.simplefilter('ignore', category=RuntimeWarning)
                logvals.loc[ind] = np.log2(y_val[ind].astype(np.float64))
            # Create twin axis with -log2 P-values
            ax2.plot(x_val, np.negative(logvals), color='dimgrey', linewidth=1.5, **lkws)
            ax2.set_ylabel('P value\n(-log2)')
        # Create significance stars and color fills
        for index, row in stats.iterrows():
            plot_significance(index, row, ax2, yaxis, yheight=0)
        # Add info on sliding window to plot
        if 'windowed' in kws:
            comment = "Window: lead {}, trail {}".format(Sett.lead, Sett.trail)
            plt.annotate(comment, (5, 5), xycoords='figure pixels')

    def stats_total(self, **kws):
        """Create statistical objects to total statistics-plots"""
        # Loop through the plot axes
        order = kws.get('x_order')
        ctrl_x = order.index(Sett.cntrlGroup)
        for ind, ax in enumerate(self.g.axes.flat):
            # Find rejected H0 for current axis
            row = self.sec_data.iloc[ind, :]
            try:
                rejects = row.iloc[row.index.get_level_values(1).str.contains('Reject')].where(row).dropna()
            except ValueError:
                continue
            reject_num = np.count_nonzero(rejects.to_numpy())
            ax.set_ylim(bottom=0)
            if reject_num > 0:  # If any rejected H0
                # Raise y-limit of axis to fit significance plots
                __, ytop = ax.get_ylim()
                tytop = ytop*1.3
                ax.set_ylim(top=tytop)
                # Find heights for significance lines
                heights = np.linspace(ytop, ytop*1.15, reject_num)
                # Loop groups with rejected H0
                for i, grp in enumerate(rejects.index.get_level_values(0)):
                    y_height = heights[i]  # Get height for the group's line
                    grp_x = order.index(grp)  # Get x-axis location of group
                    line = sorted([grp_x, ctrl_x])
                    # Plot line
                    ax.hlines(y=y_height, xmin=line[0], xmax=line[1], color='dimgrey')
                    # Locate P-value and get significance stars
                    p_value = row.loc[(grp, 'P Two-sided')]
                    p_str, _ = significance_marker(p_value, vert=True)
                    # Define plot location for stars and plot
                    ax.annotate(p_str, (line[0]+.5, y_height), ha='center')

    def save_plot(self):
        """Save created plot."""
        fig = plt.gcf()  # Get ref to current figure
        fig.savefig(str(self.filepath), format=Sett.saveformat)
        plt.close('all')

    def visible_labels(self):
        """Make tick labels visible."""
        for ax in self.g.axes.flat:
            ax.yaxis.set_tick_params(which='both', labelleft=True)
            ax.xaxis.set_tick_params(which='both', labelbottom=True)

    def xticks(self):
        """Set plot xticks & tick labels to be shown every 5 ticks."""
        if "widths-norm" in self.title:
            tick_mp = 2
        else:
            tick_mp = 1
        xticks = np.arange(0, self.handle.total_length, 5)
        plt.setp(self.g.axes, xticks=xticks * tick_mp, xticklabels=xticks)


class Plotting:
    """Make operations for different plots."""
    handle_kws = {'IDs': ['Channel', 'Sample Group'],
                  'melt': {'id_vars': ['Sample Group', 'Channel'],
                           'var_name': 'Linear Position',
                           'value_name': 'Value'},
                  'array_index': 'Sample Group',
                  'drop_grouper': 'Sample Group'}

    def __init__(self, samplegroups, **kws):
        self.kws = Plotting.handle_kws.copy()
        self.kws.update(kws)
        self.sgroups = samplegroups

    def add_bivariate(self):
        """Create additional data bivariate plots."""
        data_vars = ['Channel', 'Sample Group', 'Sample', 'Type']
        m_kws = {'IDs': data_vars, 'ylabel': 'collect', 'xlabel': 'collect', 'title_y': 1,
                 'melt': {'id_vars': data_vars, 'value_name': 'Value', 'var_name': 'Linear Position'},
                 'plot_kws': {'col': 'Type_X', 'row': 'Type_Y'}, 'drop_grouper': ['Sample Group', 'Channel', 'Type'],
                 'adjust': {'hspace': 0.3, 'top': 0.95}}
        new_kws = merge_kws(self.kws, m_kws)
        # If required data hasn't been yet collected
        savepath = self.sgroups.paths.plotdir.joinpath('Versus')
        savepath.mkdir(exist_ok=True)
        add_paths = select(self.sgroups._addData)
        # Get Add data
        all_add_data = pd.DataFrame()
        for channel in Sett.vs_channels:
            paths = [p for p in add_paths if channel == str(p.name).split('_')[1]]
            if not paths:
                print(f"-> No data found for {channel}")
                continue
            handle = system.DataHandler(self.sgroups, paths, savepath)
            add_data = handle.get_data('drop_outlier', **new_kws)
            all_add_data = pd.concat([all_add_data, add_data])
        grouped = all_add_data.groupby('Channel')

        # Make plot:
        combined_grps = set(combinations(grouped.groups, 2))
        for grps in combined_grps:
            grp, grp2 = grps
            data = grouped.get_group(grp)
            data2 = grouped.get_group(grp2)
            print(f"    {grp} vs. {grp2}  ...")
            f_title = f'Versus_Add {grp} Data - Add {grp2} Data Matrix'
            # Take only data types present in both channels:
            diff = set(data.Type.unique()).symmetric_difference(set(data2.Type.unique()))
            data_ind = data[~data.Type.isin(diff)].index
            data2_ind = data2[~data2.Type.isin(diff)].index
            # Define identifier columns that are in plottable format
            data = data.assign(Type_Y=data['Channel'] + '_' + data['Type'])
            data2 = data2.assign(Type_X=data2['Channel'] + '_' + data2['Type'])
            # Make plot
            plotter = MakePlot(data.loc[data_ind, :], handle, f_title, sec_data=data2.loc[data2_ind, :])
            plotter(pfunc.bivariate_kde, 'title', 'legend', 'no_grid', 'labels', **new_kws)

    def add_data(self):
        """Plot additional data line plots."""
        # Collect data:
        data_vars = ['Channel', 'Sample Group', 'Type']
        m_kws = {'IDs': data_vars, 'row': 'Type', 'col': None, 'ylabel': 'collect', 'sharey': 'row',
                 'melt': {'id_vars': data_vars, 'value_name': 'Value', 'var_name': 'Linear Position'}}
        new_kws = merge_kws(self.kws, m_kws)
        handle = system.DataHandler(self.sgroups, self.sgroups._addData)
        all_data = handle.get_data('drop_outlier', 'peaks', **new_kws)
        grouped_data = all_data.groupby('Channel')

        # Make plot:
        for grp, data in grouped_data:
            plotter = MakePlot(data, handle, f'Additional Data - {grp}')
            plotter(pfunc.lines, 'centerline', 'ticks', 'title', 'legend', 'labels', 'peaks', **new_kws)

    def chan_bivariate(self):
        """Create channel versus additional data bivariate plots."""
        savepath = self.sgroups.paths.plotdir.joinpath('Versus')
        savepath.mkdir(exist_ok=True)
        paths1 = select(self.sgroups._addData)
        paths2 = select(self.sgroups._chanPaths, adds=False)

        # Get Add data
        all_add_data = pd.DataFrame()
        for channel in Sett.vs_channels:  # Only channels named in settings
            paths = [p for p in paths1 if channel == str(p.name).split('_')[1]]
            if not paths:
                print("-> No data found for {}".format(channel))
                continue
            handle = system.DataHandler(self.sgroups, paths, savepath)
            data_vars = ['Channel', 'Sample Group', 'Sample', 'Type']
            m_kws = {'IDs': data_vars, 'ylabel': 'collect', 'xlabel': 'collect', 'title_y': 1,
                     'melt': {'id_vars': data_vars, 'var_name': 'Linear Position', 'value_name': 'Value'},
                     'plot_kws': {'col': 'Channel', 'row': 'Type'}, 'drop_grouper': ['Channel', 'Sample Group', 'Type']}
            new_kws = merge_kws(self.kws, m_kws)
            add_data = handle.get_data('drop_outlier', **new_kws)
            all_add_data = pd.concat([all_add_data, add_data])

        # Get Channel data
        data_vars = ['Channel', 'Sample Group', 'Sample']
        new_kws.update({'IDs': data_vars, 'drop_grouper': ['Channel', 'Sample Group']})
        new_kws['melt'].update({'id_vars': data_vars})
        ch_handle = system.DataHandler(self.sgroups, paths2)
        all_chan_data = ch_handle.get_data('drop_outlier', **new_kws)

        # Make plot:
        grouped = all_add_data.groupby('Channel')
        for grp, data in grouped:
            print("    {}  ...".format(grp))
            f_title = f'Versus_Channels - Add {grp} Data Matrix'
            plotter = MakePlot(data, handle, f_title, sec_data=all_chan_data)
            plotter(pfunc.bivariate_kde, 'title', 'legend', 'no_grid', 'labels', **new_kws)

    def channels(self):
        """Plot channel line plots."""
        new_kws = merge_kws(self.kws, {'sharey': 'row', 'col': None, 'adjust': {'hspace': 3}})

        # Collect data:
        handle = system.DataHandler(self.sgroups, self.sgroups._chanPaths)
        all_data = handle.get_data('drop_outlier', **new_kws)

        # Make plot:
        plotter = MakePlot(all_data, handle, 'Channels - All')
        plotter(pfunc.lines, 'centerline', 'ticks', 'title', 'legend', 'labels', 'peaks', **new_kws)

    def channel_matrix(self):
        """Create matrix plot containing channels on both axes."""
        # Collect data:
        paths = self.sgroups.paths.datadir.glob('ChanAvg_*')
        handle = system.DataHandler(self.sgroups, paths)
        m_kws = {'id_sep': 1, 'IDs': ['Sample Group'], 'kind': 'reg', 'diag_kind': 'kde', 'title_y': 1,
                 'xlabel': 'Feature Count', 'merge_on': ['Sample Group', 'Linear Position'],
                 'melt': {'id_vars': ['Sample Group'], 'var_name': 'Linear Position', 'value_name': 'Value'}}
        new_kws = merge_kws(self.kws, m_kws)
        all_data = handle.get_data('path_id', 'merge', **new_kws)

        # Make plot:
        plotter = MakePlot(all_data, handle, 'Channels - Matrix')
        plotter(pfunc.channel_matrix, 'title', 'legend', 'no_grid', **new_kws)

    def clusters(self):
        """Create all plots pertaining clusters."""
        # Find cluster channels from existing data
        cl_chans = [str(p.stem).split('-')[1] for p in
                    self.sgroups.paths.datadir.glob('Clusters-*.csv')]
        if not cl_chans:  # If no cluster data is found
            msg = 'No cluster count files found (Clusters_*)'
            print('WARNING: {}'.format(msg))
            lg.logprint(LAM_logger, msg, 'w')
            return

        # Create directory for cluster plots
        savepath = self.sgroups.paths.plotdir.joinpath('Clusters')
        savepath.mkdir(exist_ok=True)

        # SAMPLE-SPECIFIC POSITION PLOTS:
        # Find all cluster data files for each sample
        chan_paths = [c for p in self.sgroups.sample_paths for c in
                      p.glob('*.csv') if c.stem in cl_chans]
        cols = ['Position X', 'Position Y', 'ClusterID']
        kws = {'ylabel': 'Y', 'xlabel': 'X', 'height': 5, 'adjust': {'top': 0.65, 'bottom': 0.2}}
        new_kws = merge_kws(self.kws, kws)
        # Find all channel paths relevant to cluster channels
        for sample in Store.samples:
            smpl_paths = [p for p in chan_paths if p.parent.name == sample]
            handle = system.DataHandler(self.sgroups, smpl_paths, savepath)
            all_data = handle.get_sample_data(cols, 'no_var')
            test = all_data.loc[:, 'ClusterID'].isna().all()
            if 'ClusterID' not in all_data.columns or test:
                print(f"  -> No clusters on {sample}")
                continue  # If sample does not contain clusters, continue
            all_data.index = pd.RangeIndex(stop=all_data.shape[0])
            sub_ind = all_data.loc[all_data.ClusterID.notnull()].index
            f_title = "Positions - {}".format(sample)
            plotter = MakePlot(all_data.loc[sub_ind, :], handle, f_title)
            b_data = all_data.loc[all_data.index.difference(sub_ind), :]
            new_kws.update({'b_data': b_data})
            plotter(pfunc.cluster_positions, 'title', 'labels', **new_kws)

        # CLUSTER HEATMAPS
        paths = list(self.sgroups.paths.datadir.glob('ClNorm_*.csv'))
        if not paths:  # Only if cluster data is found
            msg = 'No normalized cluster count files found (ClNorm_*)'
            print('WARNING: {}'.format(msg))
            lg.logprint(LAM_logger, msg, 'w')
            return

        new_kws = remove_from_kws(self.kws, 'melt')
        new_kws.update({'IDs': ['Channel', 'Sample Group', 'Sample'], 'col': None, 'hue': None,
                        'xlabel': 'Linear Position', 'ylabel': 'Clustered Cells',
                        'adjust': {'top': 0.8, 'bottom': 0.2}})

        # Get and plot heatmap with samples
        handle = system.DataHandler(self.sgroups, paths, savepath)
        all_data = handle.get_data(array=False, **new_kws)

        all_data.index = all_data.loc[:, 'Sample']
        # Drop unneeded identifiers for 'samples' heatmap
        smpl_data = all_data.drop(['Sample Group', 'Sample'], axis=1)
        plotter = MakePlot(smpl_data, handle, 'Cluster Heatmaps - Samples')
        p_kws = merge_kws(new_kws, {'Sample_plot': True})
        plotter(pfunc.heatmap, 'centerline', 'ticks', 'title', 'labels', **p_kws)

        # Plot sample group averages
        grouped = all_data.groupby(['Channel', 'Sample Group'])
        # Construct a dataframe with averages:
        avg_data = pd.DataFrame()
        for grp, data in grouped:
            temp = pd.Series(data.mean(), name=grp[1])
            temp['Channel'] = grp[0]
            avg_data = avg_data.append(temp)
        # Create plot
        plotter = MakePlot(avg_data, handle, 'Cluster Heatmaps - Groups')
        plotter(pfunc.heatmap, 'centerline', 'ticks', 'title', 'labels', 'peaks', **new_kws)

        # CLUSTER LINEPLOT
        m_kws = {'ylabel': 'Clustered cells', 'titley': 1.01, 'row': 'Channel', 'col': None,
                 'melt': {'id_vars': ['Channel', 'Sample Group'], 'var_name': 'Linear Position', 'value_name': 'Value'}}
        m_data = all_data.drop('Sample', axis=1)
        m_data = m_data.melt(id_vars=['Channel', 'Sample Group'], var_name='Linear Position', value_name='Value')
        plotter = MakePlot(m_data, handle, 'Cluster Lineplots')
        plotter(pfunc.lines, 'centerline', 'ticks', 'title', 'legend', 'peaks', 'labels', **m_kws)

    def distributions(self):
        """Create distributions of all variables."""
        # Channels:
        m_kws = {'IDs': ['Sample Group', 'Channel'], 'title_y': 0.97,
                 'ylabel': 'Density', 'xlabel': None, 'row': 'Channel', 'col': None, 'aspect': 1.5,
                 'melt': {'id_vars': ['Sample Group', 'Channel'], 'var_name': 'Linear Position', 'value_name': 'Value'},
                 'drop_grouper': ['Sample Group', 'Channel'],
                 'gridspec': {'top': 0.92, 'left': 0.15, 'right': 0.8, 'hspace': 0.6}}
        print('   Channels  ...')
        new_kws = merge_kws(self.kws, m_kws)
        # Collect data:
        handle = system.DataHandler(self.sgroups, self.sgroups._chanPaths)
        all_data = handle.get_data('drop_outlier', **new_kws)
        # Make plot:
        plotter = MakePlot(all_data, handle, 'Distributions - Channels')
        plotter(pfunc.distribution, 'title', 'legend', 'labels', 'no_grid', **new_kws)

        # Additional data
        print("   Additional Data  ...")
        # id_vars = ['Sample Group', 'Channel', 'Type']
        new_kws.update({'drop_grouper': ['Sample Group', 'Type'], 'row': 'Type', 'col': None,
                        'melt': {'id_vars': ['Sample Group', 'Channel', 'DistBin'], 'var_name': 'Type',
                                 'value_name': 'Value'}})
        paths = [p for s in self.sgroups.sample_paths for p in s.glob('*.csv')
                 if p.stem not in ['Vector', 'MPs', 'MP', Sett.MPname]]
        # Collect and plot each channel separately:
        for channel in Store.channels:
            print("     {}  ...".format(channel))
            ch_paths = [p for p in paths if p.stem == channel]
            handle = system.DataHandler(self.sgroups, ch_paths)
            all_data = handle.get_sample_data(Sett.AddData.keys(), 'drop_outlier', **new_kws)
            if all_data.empty:
                continue
            # Make plot:
            p_title = 'Distributions - Additional {} Data'.format(channel)
            plotter = MakePlot(all_data, handle, p_title)
            plotter(pfunc.distribution, 'title', 'legend', 'labels', 'no_grid', **new_kws)

    def heatmaps(self):
        """Create heatmaps of channel data."""
        # Get and plot _sample group averages_
        hm_paths = self.sgroups.paths.datadir.glob("ChanAvg_*")
        handle = system.DataHandler(self.sgroups, hm_paths)
        new_kws = remove_from_kws(self.kws, 'melt')
        new_kws.update({'IDs': ['Channel', 'Sample Group']})
        all_data = handle.get_data(array='Sample Group', **new_kws)
        all_data.index = all_data['Sample Group'].tolist()
        all_data.drop('Sample Group', axis=1, inplace=True)
        plotter = MakePlot(all_data, handle, 'Heatmaps - Groups')
        p_kws = {'col': None, 'hue': None}
        plotter(pfunc.heatmap, 'centerline', 'ticks', 'title', 'peaks', **p_kws)

        # Get and plot heatmap with _samples_
        hm_paths = self.sgroups.paths.datadir.glob("Norm_*")
        handle = system.DataHandler(self.sgroups, hm_paths)
        new_kws.update({'IDs': ['Channel', 'Sample']})
        all_data = handle.get_data(array=False, **new_kws)
        all_data.index = all_data['Sample'].tolist()
        all_data.drop('Sample', axis=1, inplace=True)
        plotter = MakePlot(all_data, handle, 'Heatmaps - Samples')
        p_kws.update({'Sample_plot': True})
        plotter(pfunc.heatmap, 'centerline', 'ticks', 'title', **p_kws)

    def stat_totals(self, total_stats, path):
        """Plot variable totals with statistics."""
        plot_data = total_stats.data
        ctrl_n = int(len(total_stats.groups) / 2)
        order = total_stats.test_grps
        order.insert(ctrl_n, Sett.cntrlGroup)

        # Melt data to long form and drop missing observation points
        plot_data = pd.melt(plot_data, id_vars=['Sample Group', 'Variable'], var_name='Linear Position',
                            value_name='Value')
        plot_data = plot_data.dropna(subset=['Value'])
        # Make sure that data is in float format
        plot_data['Value'] = plot_data['Value'].astype('float64')
        # Assign variable indication the order of plotting
        plot_data['Ord'] = plot_data.loc[:, 'Sample Group'].apply(order.index)
        plot_data.sort_values(by=['Ord', 'Variable'], axis=0, inplace=True)
        # Find group order number for control group for plotting significances
        total_stats.stat_data.sort_index(inplace=True)
        # Create plot:
        savepath = total_stats.plot_dir
        handle = system.DataHandler(self.sgroups, path, savepath)
        plotter = MakePlot(plot_data, handle, total_stats.filename, sec_data=total_stats.stat_data)
        p_kws = {'row': None, 'col': 'Variable', 'x_order': order, 'height': 3, 'aspect': 1, 'title_y': 1,
                 'ylabel': 'collect', 'xlabel': 'Sample Group', #'gridspec': {'wspace': 0.25},
                 'adjust': {'left': 0.2, 'right': 0.9, 'bottom': 0.17, 'wspace': 0.6, 'top': 0.85}}
        plotter(pfunc.violin, 'title', 'total_stats', 'labels', 'legend', **p_kws)

    def stat_versus(self, stats, path):
        """Plot statistics of group versus1
         group for all variables."""
        # Restructure data to be plottable:
        ctrl_data = stats.ctrl_data.T
        test_data = stats.test_data.T
        if Sett.Drop_Outliers:  # Drop outliers
            ctrl_data = system.drop_outliers(ctrl_data, raw=True)
            test_data = system.drop_outliers(test_data, raw=True)
        # Add identifier
        ctrl_data.loc[:, 'Sample Group'] = stats.ctrl_grp
        test_data.loc[:, 'Sample Group'] = stats.test_grp
        # Combine data in to one frame and melt it to long format
        plot_data = pd.concat([ctrl_data, test_data], ignore_index=True)
        plot_data = plot_data.melt(id_vars=['Sample Group'], var_name='Linear Position', value_name='Value')
        # Initialize plotting:
        savepath = stats.plot_dir
        handle = system.DataHandler(self.sgroups, path, savepath)
        # Give title
        data_name = str(path.stem).split('_')[1:]
        titlep = '-'.join(data_name)
        f_title = "{} = {}".format(stats.title, titlep)
        # Plot variable
        plotter = MakePlot(plot_data, handle, f_title, sec_data=stats)
        ylabel = get_unit(data_name[-1])
        p_kws = {'col': None, 'row': None, 'ylabel': ylabel, 'label_first_only': True, 'gridspec': {'bottom': 0.2},
                 'melt': {'id_vars': ['Sample Group'], 'var_name': 'Linear Position', 'value_name': 'Value'}}
        if Sett.windowed:
            p_kws.update({'windowed': True})

        plotter(pfunc.lines, 'centerline', 'ticks', 'title', 'stats', 'labels', 'legend', 'peaks', **p_kws)

    def width(self):
        """Create line plots of sample group widths."""
        name = 'Sample_widths_norm.csv'
        filepath = list(self.sgroups.paths.datadir.glob(name))
        if not filepath:
            print("   No width file found. Perform 'Count' with measure_width")
            lg.logprint(LAM_logger, 'No width file found', 'w')
            return
        # Collect data:
        handle = system.DataHandler(self.sgroups, filepath)
        all_data = handle.get_data('drop_outlier', **self.kws)
        var = 'Linear Position'
        all_data.loc[:, var] = all_data.loc[:, var].divide(2, fill_value=0)

        # Make plot:
        plotter = MakePlot(all_data, handle, 'Widths - All')
        p_kws = merge_kws(self.kws, {'row': None, 'col': None, 'ylabel': 'Units (coord system)',
                                     'gridspec': {'bottom': 0.2}})
        plotter(pfunc.lines, 'centerline', 'ticks', 'title', 'legend', 'labels', 'peaks', **p_kws)


def select(paths, adds=True):
    """Select paths of defined types of data for versus plot."""
    # Find target names from settings
    add_targets = Sett.vs_adds
    ch_targets = Sett.vs_channels
    # If selecting additional data:
    if adds:
        ret_paths = [p for p in paths if str(p.stem).split('_')[1] in ch_targets
                     and str(p.stem).split('_')[2].split('-')[0] in add_targets]
        return ret_paths
    # If selecting channel counts:
    ret_paths = [p for p in paths if str(p.stem).split('_')[1] in ch_targets]
    return ret_paths


def identifiers(data: pd.DataFrame, path, ids: list) -> pd.DataFrame:
    """Add identifier variables to dataframes."""
    if 'Channel' in ids:
        data.loc['Channel', :] = path.stem.split('_')[1]
    if 'Sample Group' in ids:
        data.loc['Sample Group', :] = [str(c).split('_')[0] for c in data.columns]
    if 'Sample' in ids:
        data.loc['Sample', :] = data.columns
    if 'Type' in ids:
        name = str(path.stem).split('_')[2:]
        data.loc['Type', :] = '_'.join(name)
    return data


def get_unit(string):
    """Get unit of variable."""
    # If string is a LAM created value name:
    if string == "Distance Means":
        return "Units (coord system)"
    if '_' in string:
        var_strings = string.split('_')
        chan = var_strings[0]
        string = var_strings[1]
    sub_str = string.split('-')
    if len(sub_str) == 2:
        key, key_c = sub_str
    else:
        key = sub_str[0]
    # If not user defined value:
    if key not in Sett.AddData.keys():
        if key in Store.channels:
            return '{} Count'.format(string)
        return 'Value'
    # Otherwise, build label from the sub-units
    label = Sett.AddData.get(key)[1]
    if 'chan' in locals():
        label = f'{chan}, {label}'
    if 'key_c' in locals():
        if Sett.replaceID and key_c in Sett.channelID.keys():
            key_c = Sett.channelID.get(key_c)
        label = label + f' {key_c}'
    return label


def merge_kws(kws1, kws2):
    """Merge keyword arguments with another dictionary."""
    new_kws = kws1.copy()
    if kws2 is not None:
        new_kws.update(kws2)
    return new_kws


def remove_from_kws(kws, *args):
    """Remove keys from dictionary"""
    new_kws = kws.copy()
    for key in args:
        if isinstance(key, str):
            del new_kws[key]
    return new_kws


def significance_marker(value, colors=MakePlot.GRcolors, vert=False):
    """Find strings for significance stars."""
    if value <= 0.001:
        p_str = ["*", "*", "*"]
        color = colors[3]
    elif value <= 0.01:
        p_str = ["*", "*"]
        color = colors[2]
    elif value <= Sett.alpha:
        if value <= 0.05:
            p_str = ["*"]
        else:
            p_str = [""]
        color = colors[1]
    else:
        p_str = [" "]
        color = colors[0]
    if vert:
        ret_str = ' '.join(p_str)
    else:
        ret_str = '\n'.join(p_str)
    return ret_str, color


def plot_significance(index, row, ax, yaxis, yheight, fill=Sett.fill, stars=Sett.stars):
    """Add significance stars or color fills to plots."""
    color, p_str = None, None

    # If both hypothesis rejections have same value, continue
    if row[3] == row[6]:
        return
    xaxis = [index-0.43, index+0.43]
    if row[3] is True:  # ctrl is greater
        p_str, color = significance_marker(row[1], MakePlot.LScolors)
    elif row[6] is True:  # ctrl is lesser
        p_str, color = significance_marker(row[4], MakePlot.GRcolors)
    if fill:
        ax.fill_between(xaxis, yaxis, color=color, alpha=0.35, zorder=0)
    if stars:
        ax.annotate(p_str, (index, yheight), fontsize=8, ha='center')
