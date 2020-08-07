
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from .utils import LUT_reader, LUT_processor

class componentModel:
    """
    This is a base component model class that can be used to create new components.

    :param f_: Frequency datapoints.
    :type f_: class:`numpy.ndarray`

    :param data_folder: The location of the data folder containing s-parameter data files and a look up table.
    :type data_folder: class:`pathlib.Path`
    

    TO DO
    """
    def __init__(self, f_, data_folder, filename, nports=0, sparam_attr="", **kwargs):
        self.f_ = f_
        self.c = 299792458
        self.lambda_= self.c*1e6/self.f_
        self.componentParameters = []
        self.componentID = ""
        self.nports = nports
        self.sparam_attr = sparam_attr
        self.sparam_file = ""
        for key,value in kwargs.items():
            self.componentParameters.append([key, str(value)])
            
        
        #add component to the loaded components' list
        #components_loaded.append(self)

    def load_sparameters(self, data_folder, filename):
        """
        decides whether to load sparameters from npz file or raw sparam file
        """

        if('.npz' in filename):
                componentData = np.load(data_folder/filename)
                return self.interpolate_sparameters(self.f_, componentData['f'], componentData['f'])
        else:
            componentData, self.sparam_file = LUT_processor(data_folder, filename, self.componentParameters, self.nports, self.sparam_attr)
            return self.interpolate_sparameters(self.f_, componentData[0], componentData[1])

    def interpolate_sparameters(self, target_f, source_f, source_s):
        """
        cubic interpolation of the component sparameter data to match frequency
        """

        func = interp1d(source_f, source_s, kind='cubic', axis=0)
        return func(target_f)

    def get_data(self,ports=None, xscale="freq", yscale = "log"):
        """
        get data for specific [input,output] port combinations
        """
        
        temp_data = {} # reformat data in an array
        
        ports_ = [] #ports the plot

        if (xscale == "freq"):
            x_data = self.f_ 
            xlabel = "Frequency (Hz)" 
        else:
            x_data = self.c*1e6/self.f_
            xlabel = "Wavelength (um)"

        temp_data["xdata"] = x_data
        temp_data["xunit"] = xlabel

        if(ports==None):
            nports = self.s_.shape[-1]
            for i in range(nports):
                for j in range(nports):
                    ports_.append('S_%d_%d'%(i,j))
        else:
            ports_ = ['S_%d_%d'%(each[0],each[1]) for each in ports]

        for each_port in ports_:
            _, i, j = each_port.split('_')
            if(yscale == "log"):
                temp_data[each_port] = 10*np.log10(np.square(np.abs(self.s_[:,int(i),int(j)])))
                temp_data['yunit']='dB'
            elif(yscale=="abs"):
                temp_data[each_port] = np.abs(self.s_[:,int(i),int(j)])
                temp_data['yunit']='abs'
            elif(yscale=="abs_sq"):
                temp_data[each_port] = np.square(np.abs(self.s_[:,int(i),int(j)]))
                temp_data['yunit']='abs_sq'

        return temp_data


    def plot_sparameters(self, ports=None, show_freq=True, scale = "log"):
        ports_ = [] #ports the plot

        if (show_freq):
            x_data = self.f_ 
            xlabel = "Frequency (Hz)" 
        else:
            x_data = self.c*1e6/self.f_
            xlabel = "Wavelength (um)"

        if(ports==None):
            nports = self.s_.shape[-1]
            for i in range(nports):
                for j in range(nports):
                    ports_.append('S_%d_%d'%(i,j))
        else:
            ports_ = ['S_%d_%d'%(each[0],each[1]) for each in ports]

        for each_port in ports_:
            _, i, j = each_port.split('_')
            if(scale == "log"):
                plt.plot(x_data,10*np.log10(np.square(np.abs(self.s_[:,int(i),int(j)]))))
                plt.ylabel('Transmission (dB)')
            elif(scale=="abs"):
                plt.plot(x_data, np.abs(self.s_[:,int(i),int(j)]))
                plt.ylabel('Transmission (normalized)')
            elif(scale=="abs_sq"):
                plt.plot(x_data, np.square(np.abs(self.s_[:,int(i),int(j)])))
                plt.ylabel('Transmission (normalized^2)')
        plt.xlabel(xlabel)
        plt.xlim(left=np.min(x_data), right=np.max(x_data))
        plt.tight_layout()
        plt.legend(ports_)
        plt.show()

class compoundElement(componentModel):
    def __init__(self, f_, s_, nets = None):
        self.f_ = f_
        self.c = 299792458
        self.lambda_= self.c*1e6/self.f_ 
        self.s_ = s_
        self.nets = [i for i in s_.shape[-1]] if nets == None else nets
        #components_loaded.append(self)

class Waveguide(componentModel):
    def __init__(self, f_, length, data_folder, filename, TE_loss, **kwargs):
        self.ng_ = None
        self.alpha_ = None
        self.ne_ = None
        self.nd_ = None
        self.f_ = f_
        self.componentID = ""
        self.c = 299792458
        self.sparam_file = ""
        self.lambda_= self.c*1e6/self.f_
        self.componentParameters = []
        for key,value in kwargs.items():
            self.componentParameters.append([key, str(value)])
        
        #components_loaded.append(self)

    def load_sparameters(self, length, data_folder, filename, TE_loss):

        sfilename,_,_ = LUT_reader(data_folder, filename, self.componentParameters)
        self.sparam_file = sfilename[-1]
        filepath = data_folder / sfilename[-1]

        # Read info from waveguide s-param file
        with open(filepath, 'r') as f:
            coeffs = f.readline().split()

        nports = 2

        # Initialize array to hold s-params
        temp_s_ = np.zeros((len(self.f_), nports, nports), dtype=complex) 

        alpha = TE_loss/(20*np.log10(np.exp(1)))

        # calculate angular frequency from frequency 
        w = np.asarray(self.f_) * 2 * np.pi

        # calculate center wavelength, effective index, group index, group dispersion
        lam0, ne, ng, nd = float(coeffs[0]),  float(coeffs[1]), float(coeffs[3]), float(coeffs[5])

        # calculate angular center frequency
        w0 = (2*np.pi*self.c) / lam0

        # calculation of K
        K = 2*np.pi*ne/lam0 + (ng/self.c)*(w - w0) - (nd*lam0**2/(4*np.pi*self.c))*((w - w0)**2)

        # compute s-matrix from K and waveguide length
        for x in range(0, len(self.f_)):
            temp_s_[x,0,1] = temp_s_[x,1,0] = np.exp(-alpha*length + (K[x]*length*1j))

        s = temp_s_
        self.ng_ = ng
        self.alpha_ = alpha
        self.ne_ = ne
        self.nd_ = nd
    
        return s


