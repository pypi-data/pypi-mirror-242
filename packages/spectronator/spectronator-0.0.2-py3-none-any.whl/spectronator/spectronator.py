
import os
import numpy as np
import scipy.signal
try:
    import biosystfiles
except:
    biosystfiles = None


class Spectronator:
    '''Generate spectral responsivness data timeserie responses.
    
    Attributes
    ----------
    data : dict
        Keys are datafile file basenames. Items are (trace, sampling_frequency)
        pairs where trace is a 1D numpy array and sampling_frequency is a float.
    lowpass, highpass : float
        Critical frequencies for lowpass and highpass filters, in Herz (Hz).
    filter_order : int
        Filter order.
    filter : string
    filters : dict
    chop_interval : flaot or None
    method : string
    methods : list

    '''

    def __init__(self):

        self.data = {}

        self.lowpass = 0.01
        self.highpass = 100
        self.filter_order = 2
        self.filters = {
                'Butterworth': scipy.signal.butter,
                #'Chebyshev type 1': scipy.signal.cheby1,
                #'Chebyshev type 2': scipy.signal.cheby2,
                #'Elliptic (Cauer)': scipy.signal.ellip,
                'Bessel/Thomson': scipy.signal.bessel,
                }
        self.filter = 'Butterworth'

        self.chop_interval = None

        self.method = 'minmax'
        self.methods = ['minmax', 'start-vs-max', 'start-vs-min']

        self._cached_filtered = {}

    @property
    def max_fs(self):
        fs = 0
        for fn in self.data:
            fs = max(fs, self.data[fn][1])
        return fs
    

    def clear(self):
        self.data = {}
        self._cached_filtered = {}

    def add_datafile(self, fn, wavelengths):
        '''Loads a datafile.

        wavelengths : list
            List of stimulus wavelengths that are within this file, in order.
        '''

        if not os.path.isfile(fn):
            raise ValueError(f'Is not a file {fn}')
        
        if fn.lower().endswith('.csv'):
            data = np.loadtxt(fn, delimiter=',').T
            print(data.shape)
            fs = 1/(data[0][1] - data[0][0])
            data = data[1]
        
        elif fn.endswith('.mat') and biosystfiles is not None:
            # Attempt to open as a Biosyst file
            data, fs = biosystfiles.extract(fn, 0)
            data = data.flatten()
        else:
            raise ValueError(f'File type unkown: {fn}')
        
        self.data[os.path.basename(fn)] = (data, fs, wavelengths)



    def get_raw(self):
        '''Return raw, unfiltered responses.
        
        Returns
        X, Y : list
        '''
        X = []
        Y = []

        for fn in self.data:
            y = self.data[fn][0]
            fs = self.data[fn][1]
            x = np.linspace(0, len(y)/fs, len(y))
            
            X.append(x)
            Y.append(y)
        
        return X, Y


    def get_filtered(self):
        '''Return filtered responses

        Returns
        X, Y : list
        '''
        key = f'{self.lowpass}-{self.highpass}-{self.filter_order}-{self.filter}'
        if key in self._cached_filtered:
            return self._cached_filtered[key]

        X = []
        Y = []


        filt = self.filters.get(self.filter)

        for fn in self.data:
            y = self.data[fn][0]
            fs = self.data[fn][1]
            
            #if self.filter == ''
            f0 = filt(self.filter_order, self.lowpass,
                                     btype='highpass', output='sos', fs=fs)
            f1 = filt(self.filter_order, self.highpass,
                                     btype='lowpass', output='sos', fs=fs)

            y = scipy.signal.sosfiltfilt(f1, y)
            y = scipy.signal.sosfiltfilt(f0, y)

            x = np.linspace(0, len(y)/fs, len(y))
            
            X.append(x)
            Y.append(y)
        
        self._cached_filtered = {key : (X, Y)}

        return self._cached_filtered[key]
    
    def get_wavelengths(self):
        '''Reuturns used wavelengths in order.
        '''
        wavelengths = []
        for fn in self.data:
            wavelengths.extend( self.data[fn][2] )
        return wavelengths

    def get_choppoints(self, in_seconds=True):
        '''Returns chop points.

        in_seconds
        '''
        
        X, Y = self.get_filtered()
        
        for fn, (x,y) in zip(self.data, zip(X,Y)):
            fs = self.data[fn][1]
            if self.chop_interval is None:
                if in_seconds:
                    return [i*len(x)/fs/19 for i in range(19+1)] 
                else:
                    return [int(i*len(x)/19) for i in range(19+1)] 
            else:
                if in_seconds:
                    return [i*self.chop_interval for i in range(19+1)]
                else:
                    return [int(i*self.chop_interval*fs) for i in range(19+1)]

    
  
    def get_spectral_response(self, method=None):
        '''

        method : string
        '''
        
        if method is None:
            method = self.method

        X, Y = self.get_filtered()
        x = X[0]
        y = Y[0]

        chop_points = self.get_choppoints(in_seconds=False)
        
        responses = []

        for i in range(len(chop_points)-1):
            a = chop_points[i]
            b = chop_points[i+1]
            
            segment = Y[0][a:b]

            if method == 'minmax':
                response = abs(np.max(segment) - np.min(segment))
            elif method == 'start-vs-max':
                start = np.mean(segment[:10])
                maxi = np.max(segment)
                response = abs(maxi-start)
            elif method == 'start-vs-min':
                start = np.mean(segment[:10])
                mini = np.min(segment)
                response = abs(mini-start)
            else:
                raise ValueError(f'Unkown method minmax')
            responses.append(response)

        return [self.get_wavelengths()], [responses]




