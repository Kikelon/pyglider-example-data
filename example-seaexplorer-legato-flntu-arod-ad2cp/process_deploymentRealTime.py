import logging
import os
import pyglider.seaexplorer as seaexplorer
import pyglider.ncprocess as ncprocess
import pyglider.plotting as pgplot

logging.basicConfig(level='INFO')

rawdir = './realtime_raw/'
rawncdir = './realtime_rawnc/'
deploymentyaml = './deploymentRealtime.yml'
l0tsdir = './L0-timeseries/'
profiledir = './L0-profiles/'
griddir = './L0-gridfiles/'
plottingyaml = './plottingconfig.yml'

if __name__ == '__main__':
    # clean last processing...
    os.system('rm ' + rawncdir + '* ' + l0tsdir + '* ' + profiledir + '* ' +
              griddir + '* ')

    # turn seaexplorer zipped csvs into nc files.
    seaexplorer.raw_to_rawnc(rawdir, rawncdir, deploymentyaml)
    # merge individual netcdf files into single netcdf files *.gli*.nc and *.pld1*.nc
    seaexplorer.merge_rawnc(rawncdir, rawncdir, deploymentyaml, kind='sub')
    # Make level-0 timeseries netcdf file from the raw files...
    outname = seaexplorer.raw_to_timeseries(rawncdir, l0tsdir, deploymentyaml, kind='sub')
    ncprocess.extract_timeseries_profiles(outname, profiledir, deploymentyaml)
    outname2 = ncprocess.make_gridfiles(outname, griddir, deploymentyaml)
    # make profile netcdf files for ioos gdac...
    # make grid of dataset....
    pgplot.timeseries_plots(outname, plottingyaml)
    pgplot.grid_plots(outname2, plottingyaml)