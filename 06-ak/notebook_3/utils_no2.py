#!/usr/bin/python3

"""
author: felipe cifuentes (Adapted from John Douros)

Helper functions for comparing CAMS with TROPOMI
"""

import numpy as np
import xarray as xr


def CAMS_levels(no2_cams, sp, a_inter, b_inter):
    
    #Dimensions will be use later
    nlev, nlat, nlon = no2_cams.shape
    
    pres_fl = np.zeros((nlev,nlat,nlon))
    z_fl = np.zeros((nlev,nlat,nlon))
    pres_hl = np.zeros((nlev+1,nlat,nlon))
    z_hl = np.zeros((nlev+1,nlat,nlon))

    # Calculate pressures at half and full levels
    for ilev in np.arange(nlev+1):

        # half-level pressures
        pres_hl[ilev,:,:] = a_inter[ilev] + b_inter[ilev] * sp

    for ilev in np.arange(nlev):
        # use half-level as & bs to produce full-level values
        a = (a_inter[ilev+1] + a_inter[ilev])/2.0
        b = (b_inter[ilev+1] + b_inter[ilev])/2.0
        pres_fl[ilev,:,:] = a + b * sp


    # Calculate estimates of CAMS-global level altitudes (above ground) assuming
    # Use constant lapse rate and surface temperature (see config)
    import scipy.constants as sc

    MWair = 28.97  # g/mol Molecular weight of dry air
    MWno2 = 46.0055  # g/mol NO2
    Rs = sc.R * 1000.0 / MWair  # J/(kg K) Specific gas constant for air
    T0 = 300  # K : Assumption for the surface temperature
    L = -0.0065  # K/m Tropospheric temperature lapse rate

    z_hl = (T0 / L) * ((pres_hl / sp ) ** (-1*L*Rs/sc.g) -1)

    # this won't work for the model top however, where p=0 => z=inf,
    # and gives a runtime warning, thus:
    z_hl[nlev,:,:] = 2*z_hl[nlev-1,:,:] - z_hl[nlev-2,:,:]

    # Altitudes of TM5 full levels
    # with constant lapse rate
    z_fl = (T0 / L) * ((pres_fl / sp) ** (-1*L*Rs/sc.g) -1)

    return pres_fl, z_fl, pres_hl, z_hl


def CAMS_reg_levels(no2_cams, alt, sp):
    
    #Dimensions will be use later
    nlev, nlat, nlon = no2_cams.shape
    
    pres_fl = np.zeros((nlev-1,nlat,nlon))
    z_fl = np.zeros((nlev-1,nlat,nlon))
    no2_fl = np.zeros((nlev-1,nlat,nlon))
    
    pres_hl = np.zeros((nlev,nlat,nlon))
    z_hl = np.zeros((nlev,nlat,nlon))
    
    for i in np.arange(nlev):
        z_hl[i,:,:] = alt[i]
    
    #Calculate full level altitudes
    for i in np.arange(nlev-1):
        
        z_fl[i] = (z_hl[i] + z_hl[i+1])/2
        no2_fl[i] = (no2_cams[i] + no2_cams[i+1])/2


    import scipy.constants as sc
    MWair = 28.97  # g/mol Molecular weight of dry air
    MWno2 = 46.0055  # g/mol NO2
    Rs = sc.R * 1000.0 / MWair  # J/(kg K) Specific gas constant for air
    T0 = 300  # K : Assumption for the surface temperature
    L = -0.0065  # K/m Tropospheric temperature lapse rate

    pres_hl = sp*(1+(L / T0)*(z_hl))**(-1*sc.g/(L*Rs))
    pres_fl = sp*(1+(L / T0)*(z_fl))**(-1*sc.g/(L*Rs))

    return pres_fl, z_fl, pres_hl, z_hl, no2_fl



def convert_units(input1, pres, z):
    """ 
    Convert between kg/kg to molecule/m3

        * Pressures: Pa
        * Heights: m
        * Temperatures: K

        * Concentrations: μg/m3
        * Densities: molecules/m3

    Ideal gas constant (sc.R) is in m3 Pa K−1 mol−1

    """ 
    import sys
    import scipy.constants as sc

    MWair = 28.97  # g/mol Molecular weight of dry air
    MWno2 = 46.0055  # g/mol NO2
    Rs = sc.R * 1000.0 / MWair  # J/(kg K) Specific gas constant for air
    T0 = 300  # K : Assumption for the surface temperature
    L = -0.0065  # K/m Tropospheric temperature lapse rate
    
    temp = T0 + L * z
    
    output1 = input1 * pres /(Rs * temp) * 1e9 * sc.Avogadro /(1e6 * MWno2)
    
    return output1


def no2_column_cams_simple(no2_cams, z_hl):
    
    nlev, nlat, nlon = no2_cams.shape
    no2_layer = np.zeros((nlev, nlat, nlon))

    for n in range(nlev):
        no2_layer[n,:,:] = ((z_hl[n+1,:,:] - z_hl[n,:,:]) *  no2_cams[n,:,:]) / 1e19  #Conversion de molec/m2 a Pmolec/cm2 

    no2_colum = np.sum(no2_layer,axis=0)
    
    return no2_colum, no2_layer


def no2_column_cams_interp(no2_cams, z_hl_cams, pres_CAMS_fl, AK_trop, fl_fields, valindex):
    
    from scipy.interpolate import interp2d
    
    # Vertically interpolate kernells
    a, b, c = pres_CAMS_fl.shape
    AK_final = np.zeros((a, b, c))
    
    tm5_press_levels = fl_fields.pres_tm5_fl.values
    tropopause_index = fl_fields.TM5_tropopause.values
    
    # For linear interpolation
    for x in range(a):
        for y,z in valindex:
            
            if np.isnan(tropopause_index[y,z]) == True :
                
                AK_final[x,y,z] = 0
                
            else:
                
                p_cams = pres_CAMS_fl[x,y,z]
            
                if p_cams > tm5_press_levels[int(tropopause_index[y,z]),y,z]:
            
                    dif_p = np.absolute(tm5_press_levels[:,y,z]-p_cams)
                    index_p1 = dif_p.argmin()
            
                    dif_p[index_p1] = dif_p[index_p1]*1e9
                    index_p2 = dif_p.argmin()
            
                    # For linear interpolation            
                    m = (AK_trop.values[index_p1,y,z] - AK_trop.values[index_p2,y,z]) / (tm5_press_levels[index_p1,y,z] - tm5_press_levels[index_p2,y,z])
                    intercept = AK_trop.values[index_p1,y,z] - m * tm5_press_levels[index_p1,y,z]
            
                    AK_final[x,y,z] = m * p_cams + intercept
                
                else:
                
                    AK_final[x,y,z] = 0
                    
    # Estimate column
    NO2_layer = np.zeros((a, b, c))
    

    for n in range(a):
        NO2_layer[n,:,:] = ((z_hl_cams[n+1,:,:] - z_hl_cams[n,:,:]) *  no2_cams[n,:,:]  * AK_final[n,:,:]) / 1e19  #Conversion de molec/m2 a Pmolec/cm2 

    NO2_colum = np.sum(NO2_layer,axis=0)
    
    return NO2_colum, NO2_layer


def grid_bounds(scanlines, ground_pixels, ds_GL):

    """
    Calculate TROPOMI grid boundaries in the form that can be used for regridding
    xith xESMF/ESMF

    Background:
    The TROPOMI product follows the CF conventions and provides
    coordinate_bounds(scanline,ground_pixel,4). This however is not directly
    compatible with standard Python practice (e.g. in pcolormesh or ESMF/ESMPy/xesmf)
    which use and require some lon_b/lat_b(n+1,m+1) variables to account for the
    boundaries. Thus, two extra dimensions with +1 length and two new coordinates
    need to be calculated.

    *HOWEVER*, this conversion as realised in the code below is not for arbitrary grids
    as it will depend on the order of the corner points in combination with the
    orientation of the grid. Here we assume oriantation with slope < 1
    (as e.g. for Europe in TROPOMI?).

    TODO: A generic way to convert between the two methods aplicable for
    arbitrary curvilinear grids.

    Or perhaps not, check below, it's not a trivial problem:
    https://cf-xarray.readthedocs.io/en/latest/generated/xarray.Dataset.cf.bounds_to_vertices.html

    """

    lat_b = np.empty([scanlines+1, ground_pixels+1])
    lon_b = np.empty([scanlines+1, ground_pixels+1])

    lat_b[0:scanlines,0:ground_pixels] = ds_GL['latitude_bounds'].sel(time=0).values[:,:,0]
    lat_b[scanlines,0:ground_pixels] = ds_GL['latitude_bounds'].sel(time=0).values[-1,:,3]
    lat_b[0:scanlines,ground_pixels] = ds_GL['latitude_bounds'].sel(time=0).values[:,-1,1]
    lat_b[scanlines,ground_pixels] = ds_GL['latitude_bounds'].sel(time=0).values[-1,-1,2]

    lon_b[0:scanlines,0:ground_pixels] = ds_GL['longitude_bounds'].sel(time=0).values[:,:,0]
    lon_b[scanlines,0:ground_pixels] = ds_GL['longitude_bounds'].sel(time=0).values[-1,:,3]
    lon_b[0:scanlines,ground_pixels] = ds_GL['longitude_bounds'].sel(time=0).values[:,-1,1]
    lon_b[scanlines,ground_pixels] = ds_GL['longitude_bounds'].sel(time=0).values[-1,-1,2]

    return lon_b, lat_b



def xesmf_conservative_cams_s5p(scanlines, ground_pixels, var, ds_GL, lonmin, lonmax, latmin, latmax, dlon_out, dlat_out, lon_b, lat_b, lon_in, lat_in):
    """
    Conservative regridding using xesmf
    Requires as input and returns xr.dataarray
    """
    import xesmf as xe
    
    # Define imput EMEP grid for xesmf (arguments are boundaries, not cell centres)
    ds_inp = xe.util.grid_2d(lonmin, lonmax-0.0000000001, dlon_out, latmin, latmax-0.0000000001, dlat_out)


    # Define output tropomi grid for xesmf

    # Create extra dimensions to account for cell boundaries
    scanline_b = np.linspace(0, scanlines, scanlines+1)
    ground_pixel_b = np.linspace(0, ground_pixels, ground_pixels+1)
    
    
    # create a dummy array to be merged with original data aiming to add
    # the above dimensions
    ds_out = xr.DataArray(lon_b, coords=[scanline_b, ground_pixel_b], dims=['scanline_b', 'ground_pixel_b'])
    ds_out = ds_out.to_dataset(name='example_field')
    # add cell boundary coordinates
    ds_out.coords['lon_b'] = (('scanline_b', 'ground_pixel_b'), lon_b)
    ds_out.coords['lat_b'] = (('scanline_b', 'ground_pixel_b'), lat_b)
    ds_out.coords['lon'] = (('scanline', 'ground_pixel'), lon_in)
    ds_out.coords['lat'] = (('scanline', 'ground_pixel'), lat_in)
    
    regridder = xe.Regridder(ds_inp, ds_out, 'conservative', unmapped_to_nan=True)
    
    data_out = regridder(var)
    

    return data_out


def bilin_regrid_cams_s5p(no2_cams, lat_cams, lon_cams, lat_s5p, lon_s5p):

    from scipy.interpolate import interp2d
    
    nlat, nlon = lat_s5p.shape
    regrid_no2 = np.zeros((8,nlat,nlon))*np.nan
    
    for i in range(8):
        
        regridder = interp2d(lon_cams, lat_cams, no2_cams[i,:,:], kind='linear', fill_value=np.nan)
    
        for x in range(nlat):
            for y in range (nlon):
                
                regrid_no2[i,x,y] = regridder(lon_s5p[x,y],lat_s5p[x,y]) 
    
    return regrid_no2



def pressure_alts_tm5(scanlines, ground_pixels, tm5_a, tm5_b, sp, AK):
    """        
    Calculate TM5 pressures and layer altitudes/heights

    S5P TM5 comment on pressures:
      p(t, k, j, i, l) = ap(k, l) + b(k, l)*ps(t, j, i);
      k from surface to top of atmosphere;
      l=0 for base of layer, l=1 for top of layer.

    Counting is from surface to top.
    AK in not used, it's only to get the grid coordinates.
    """ 
    
    import sys
    import scipy.constants as sc
    
    MWair = 28.97  # g/mol Molecular weight of dry air
    MWno2 = 46.0055  # g/mol NO2
    Rs = sc.R * 1000.0 / MWair  # J/(kg K) Specific gas constant for air
    T0 = 300  # K : Assumption for the surface temperature
    L = -0.0065  # K/m Tropospheric temperature lapse rate
    
    # Create an empty dataset with the correct dims/coords
    fl_fields = AK.to_dataset(name='AK')
    fl_fields = fl_fields.drop('AK')

    # Create an empty dataset with the correct dims/coords
    # for the full level fields
    hl_fields = xr.Dataset()
    # horizontal dimensions and time are the same
    hl_fields.coords['scanline'] = fl_fields.scanline.data
    hl_fields.coords['ground_pixel'] = fl_fields.ground_pixel.data
    hl_fields.coords['longitude'] = (('scanline','ground_pixel'),fl_fields.longitude.data)
    hl_fields.coords['latitude'] = (('scanline','ground_pixel'),fl_fields.latitude.data)
    hl_fields.coords['time'] = fl_fields.time.data
    # levels are +1
    hl_fields.coords['layer'] = np.arange(fl_fields.layer.data[0],\
                                    fl_fields.layer.data[-1]+2,1.0)


    # Get number of levels/layers (34)
    tm5_levels = tm5_a.layer.values.size

    # No need to use all of them when considering only CAMS-regional.
    # There are usually up to 11 levels up to 5000 meters,
    # let's select 15 just to be sure.
    #tm5_levels = 15

    # Initialize
    # pressure at half-levels
    pres_tm5_hl = np.empty((tm5_levels+1, scanlines, ground_pixels))
    # pressure at full-levels
    pres_tm5_fl = np.empty((tm5_levels, scanlines, ground_pixels))
    # Layer thickneses 
    D = np.empty((tm5_levels, scanlines, ground_pixels))

    # get as and bs at interfaces
    a_inter = tm5_a.values
    b_inter = tm5_b.values

    # Calculate TM5 pressures at half and full levels
    for ilev in np.arange(tm5_levels):
        
        # half-level pressures
        pres_tm5_hl[ilev,:,:] = a_inter[ilev][0] + b_inter[ilev][0] * sp

        # use half-level as & bs to produce full-level values
        a = (a_inter[ilev][0] + a_inter[ilev][1])/2.0
        b = (b_inter[ilev][0] + b_inter[ilev][1])/2.0
        pres_tm5_fl[ilev,:,:] = a + b * sp


    # at the top (half-level)
    pres_tm5_hl[tm5_levels,:,:] = a_inter[tm5_levels-1][1] + b_inter[tm5_levels-1][1] * sp

    # Calculate estimates of TM5 level altitudes (above ground) assuming
    # Use constant lapse rate and surface temperature (see config)

    # Altitudes of TM5 half levels with constant lapse rate
    try:
        z_hl = (T0 / L) * ((pres_tm5_hl / sp.values) ** (-1*L*Rs/sc.g) -1)
    except:
        z_hl = (T0 / L) * ((pres_tm5_hl / sp) ** (-1*L*Rs/sc.g) -1)
    # this won't work for the model top however where p=0 => z=inf,
    # and gives a runtime warning, thus just repeat a same thicknes layer on 
    # top of the last one:
    z_hl[tm5_levels,:,:] = 2*z_hl[tm5_levels-1,:,:] - z_hl[tm5_levels-2,:,:]

    # Altitudes of TM5 full levels with constant lapse rate
    try:
        z_fl = (T0 / L) * ((pres_tm5_fl / sp.values) ** (-1*L*Rs/sc.g) -1)
    except:
        z_fl = (T0 / L) * ((pres_tm5_fl / sp) ** (-1*L*Rs/sc.g) -1)
        
    # Calculate layer thickness
    for ilev in np.arange(tm5_levels): D[ilev,:,:] = z_hl[ilev+1,:,:] - z_hl[ilev,:,:]

    # Add fields to dataset
    fl_fields['pres_tm5_fl'] = (('layer', 'scanline', 'ground_pixel'), pres_tm5_fl)
    hl_fields['pres_tm5_hl'] = (('layer', 'scanline', 'ground_pixel'), pres_tm5_hl)
    fl_fields['z_fl'] = (('layer', 'scanline', 'ground_pixel'), z_fl)
    hl_fields['z_hl'] = (('layer', 'scanline', 'ground_pixel'), z_hl)
    fl_fields['D'] = (('layer', 'scanline', 'ground_pixel'), D)

    fl_fields['pres_tm5_fl'].attrs['units'] = 'Pa'
    fl_fields['z_fl'].attrs['units'] = 'm'
    hl_fields['pres_tm5_hl'].attrs['units'] = 'Pa'
    hl_fields['z_hl'].attrs['units'] = 'm'
    fl_fields['D'].attrs['units'] = 'm'

    del pres_tm5_fl, z_fl, D

    return fl_fields, hl_fields, tm5_levels