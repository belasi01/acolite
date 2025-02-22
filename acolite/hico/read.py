## read HICO L1B NetCDF data
## QV 2021-08-03
## modifications: 2025-02-10 (QV) added check for Lt DN scaling

def read(file, dataset, band = None):
    import h5py
    import numpy as np

    data = None
    with h5py.File(file, mode='r') as f:
        if dataset == 'lat': df = f['/navigation/latitudes/']
        if dataset == 'lon': df = f['/navigation/longitudes/']
        if dataset == 'vaa': df = f['/navigation/sensor_azimuth/']
        if dataset == 'vza': df = f['/navigation/sensor_zenith/']
        if dataset == 'saa': df = f['/navigation/solar_azimuth/']
        if dataset == 'sza': df = f['/navigation/solar_zenith/']

        if dataset == 'lt':
            df = f['/products/Lt/']
            attributes = {k: df.attrs[k] for k in df.attrs.keys() if k != 'DIMENSION_LIST'}

            if band is None:
                data = df[:,:,:].astype(np.float32)
            else:
                for bi, b in enumerate(np.atleast_1d(band)):
                    if bi == 0:
                        data = df[:,:,b].astype(np.float32)
                    else:
                        data = np.dstack((data, df[:,:,b].astype(np.float32)))
            ## scale DN
            if ('scale_factor' in attributes) & ('add_offset' in attributes):
                data *= attributes['scale_factor'][0]
                data += attributes['add_offset'][0]
            elif ('slope' in attributes) & ('intercept' in attributes):
                data *= attributes['slope'][0]
                data += attributes['intercept'][0]
            else:
                print('Could not identify scale and offset from file {}'.format(file))
                return
        else:
            data = df[:,:].astype(np.float32)
            attributes = {k: df.attrs[k] for k in df.attrs.keys() if k != 'DIMENSION_LIST'}

    return(data, attributes)
