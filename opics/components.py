import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from .utils import LUT_reader, LUT_processor
from numpy import ndarray
from pathlib import PosixPath
from typing import Dict, List, Optional, Union


class componentModel:
    """Defines the base component model class used to create new components for a library."""

    def __init__(
        self,
        f: ndarray,
        data_folder: PosixPath,
        filename: str,
        nports: int = 0,
        sparam_attr: str = "",
        **kwargs
    ) -> None:
        """Defines the base component model class used to create new components for a library.

        Args:
            f (numpy.ndarray): Frequency datapoints.
            data_folder (pathlib.Path): The location of the data folder containing s-parameter data files and a look up table.
            filename (str): File name of the component.
            nports (int, optional): Number of ports in the component. Defaults to 0.
            sparam_attr (str, optional): XML LUT attribute for the s-parameter data file name. Defaults to "".
        """

        self.f = f
        self.c = 299792458
        self.s = np.array((2, 2))
        self.lambda_ = self.c * 1e6 / self.f
        self.componentParameters = []
        self.componentID = ""
        self.nports = nports
        self.port_references = [i for i in range(self.nports)]
        self.sparam_attr = sparam_attr
        self.sparam_file = ""
        for key, value in kwargs.items():
            self.componentParameters.append([key, str(value)])

        # add component to the loaded components' list
        # components_loaded.append(self)

    def load_sparameters(self, data_folder: PosixPath, filename: str) -> ndarray:
        """Decides whether to load sparameters from npz file or from a raw sparam file or from a look-up table (for tunable components with attributes).

        Args:
            data_folder (pathlib.Path): The location of the data folder containing s-parameter data files and a look up table.
            filename (str): File name of the component.

        Returns:
            sparameters (numpy.ndarray): Array of the component's s-parameters.
        """

        if ".npz" in filename:
            componentData = np.load(data_folder / filename)
            return self.interpolate_sparameters(
                self.f, componentData["f"], componentData["f"]
            )
        else:
            componentData, self.sparam_file = LUT_processor(
                data_folder,
                filename,
                self.componentParameters,
                self.nports,
                self.sparam_attr,
            )
            return self.interpolate_sparameters(
                self.f, componentData[0], componentData[1]
            )

    def interpolate_sparameters(
        self, target_f: ndarray, source_f: ndarray, source_s: ndarray
    ) -> ndarray:
        """Cubic interpolation of the component sparameter data to match the desired simulation frequency range.

        Args:
            target_f (numpy.ndarray): The target frequency range onto which the s-parameters will be interpereted on.
            source_f (numpy.ndarray): The source frequency range that the component data has stored.
            source_s (numpy.ndarray): The source s-parameters that the component data has stored.

        Returns:
            sparameters (numpy.ndarray): Interpolated s-parameters value over the target frequency range.
        """

        func = interp1d(source_f, source_s, kind="cubic", axis=0)
        return func(target_f)

    def write_sparameters(self, dirpath, filename, f_data, s_data):
        """Export the simulated s-parameters to a file.

        Args:
            dirpath (pathlib.Path): Directory of the filed to be saved.
            filename (str): Name of the file to be saved.
            f_data (numpy.ndarray): Frequency range data to be exported.
            s_data (numpy.ndarray): S-parameter data to be exported.
        """
        with open(dirpath / filename, "w") as datafile_id:
            datalen = s_data.shape[0]

            for i in range(s_data.shape[1]):
                for j in range(s_data.shape[2]):
                    datafile_id.write(
                        "('port %d','TE',1,'port %d',1,'transmission')\n" % (i, j)
                    )
                    datafile_id.write("(%d,3)\n" % (datalen))

                    temp_data = s_data[:, i, j]
                    data = np.array([f_data, np.abs(temp_data), np.angle(temp_data)])
                    data = data.T
                    np.savetxt(datafile_id, data, fmt=["%d", "%f", "%f"])

    def get_data(
        self, ports: None = None, xscale: str = "freq", yscale: str = "log"
    ) -> Dict[str, Union[ndarray, str]]:
        """Get the S-parameters data for specific [input,output] port combinations, to be used for plotting functionalities.
        (WARNING: unused, to be used in plot_sparameters)

        Args:
            ports (list, optional): List of lists that contains the desired S-parameters, e.g., [[1,1],[1,2],[2,1],[2,2]]. Defaults to None.
            xscale (str, optional): Plotting x axis label. Defaults to "freq".
            yscale (str, optional): Plotting Y axis label. Defaults to "log".

        Returns:
            temp_data (dict): Dictionary containing the plotting information to be used, including S-parameters data and plotting labels.
        """
        temp_data = {}  # reformat data in an array

        ports_ = []  # ports the plot

        if xscale == "freq":
            x_data = self.f
            xlabel = "Frequency (Hz)"
        else:
            x_data = self.c * 1e6 / self.f
            xlabel = "Wavelength (um)"

        temp_data["xdata"] = x_data
        temp_data["xunit"] = xlabel

        if ports is None:
            nports = self.s.shape[-1]
            for i in range(nports):
                for j in range(nports):
                    ports_.append("S_%d_%d" % (i, j))
        else:
            ports_ = ["S_%d_%d" % (each[0], each[1]) for each in ports]

        for each_port in ports_:
            _, i, j = each_port.split("_")
            if yscale == "log":
                temp_data[each_port] = 10 * np.log10(
                    np.square(np.abs(self.s[:, int(i), int(j)]))
                )
                temp_data["yunit"] = "dB"
            elif yscale == "abs":
                temp_data[each_port] = np.abs(self.s[:, int(i), int(j)])
                temp_data["yunit"] = "abs"
            elif yscale == "abs_sq":
                temp_data[each_port] = np.square(np.abs(self.s[:, int(i), int(j)]))
                temp_data["yunit"] = "abs_sq"

        return temp_data

    def plot_sparameters(self, ports=None, show_freq=True, scale="log"):
        """Plot the component's S-parameters.

        Args:
            ports (list, optional): List of lists that contains the desired S-parameters, e.g., [[1,1],[1,2],[2,1],[2,2]]. Defaults to None.
            show_freq (bool, optional): Flag to determine whether to plot with respect to frequency or wavelength. Defaults to True.
            scale (str, optional): Plotting y axis scale, options available: ["log", "abs", "abs_sq"]. Defaults to "log".
        """

        ports_ = []  # ports the plot

        if show_freq:
            x_data = self.f
            xlabel = "Frequency (Hz)"
        else:
            x_data = self.c * 1e6 / self.f
            xlabel = "Wavelength (um)"

        if ports is None:
            nports = self.s.shape[-1]
            for i in range(nports):
                for j in range(nports):
                    ports_.append("S_%d_%d" % (i, j))
        else:
            ports_ = ["S_%d_%d" % (each[0], each[1]) for each in ports]

        for each_port in ports_:
            _, i, j = each_port.split("_")
            if scale == "log":
                plt.plot(
                    x_data, 10 * np.log10(np.square(np.abs(self.s[:, int(i), int(j)])))
                )
                plt.ylabel("Transmission (dB)")
            elif scale == "abs":
                plt.plot(x_data, np.abs(self.s[:, int(i), int(j)]))
                plt.ylabel("Transmission (normalized)")
            elif scale == "abs_sq":
                plt.plot(x_data, np.square(np.abs(self.s[:, int(i), int(j)])))
                plt.ylabel("Transmission (normalized^2)")
        plt.xlabel(xlabel)
        plt.xlim(left=np.min(x_data), right=np.max(x_data))
        plt.tight_layout()
        plt.legend(ports_)
        plt.show()


class compoundElement(componentModel):
    """Defines the properties of a compound element or simulated component. A compound element is a collection of connected components, inherits componentModel OPICS class."""

    def __init__(
        self, f: ndarray, s: ndarray, nets: Optional[List[List[int]]] = None
    ) -> None:
        """Defines the properties of a compound element or simulated component. A compound element is a collection of connected components, inherits componentModel OPICS class.

        Args:
            f (numpy.ndarray): Frequency range data of the compound element.
            s (numpy.ndarray): S-parameters data of the compound element.
            nets (list, optional): List of nets available in the compound element. Defaults to None.
        """
        self.f = f
        self.c = 299792458
        self.lambda_ = self.c * 1e6 / self.f
        self.s = s
        self.nets = [i for i in s.shape] if nets is None else nets
        # components_loaded.append(self)


class Waveguide(componentModel):
    """Defines the properties of a waveguide component, can be used in the interconnected between components."""

    def __init__(
        self,
        f: ndarray,
        length: float,
        data_folder: PosixPath,
        filename: str,
        TE_loss: int,
        **kwargs
    ) -> None:
        """Defines the properties of a waveguide component, can be used in the interconnected between components.

        Args:
            f (numpy.ndarray): Frequency range data of the waveguide element.
            length (float): Length of the waveguide, in meters.
            data_folder (pathlib.Path): The location of the data folder containing waveguide data files and a look up table.
            filename (str): File name of the waveguide data file.
            TE_loss (float): Value that defines the loss of the waveguide in dB/m.
        """
        self.ng_ = None
        self.alpha_ = None
        self.ne_ = None
        self.nd_ = None
        self.f = f
        self.length = length
        self.componentID = ""
        self.c = 299792458
        self.sparam_file = ""
        self.nports = 2
        self.port_references = [i for i in range(self.nports)]
        self.lambda_ = self.c * 1e6 / self.f
        self.componentParameters = []
        for key, value in kwargs.items():
            self.componentParameters.append([key, str(value)])

        # components_loaded.append(self)

    def load_sparameters(
        self, length: float, data_folder: PosixPath, filename: str, TE_loss: int
    ) -> ndarray:
        """read s_parameters"""

        sfilename, _, _ = LUT_reader(data_folder, filename, self.componentParameters)
        self.sparam_file = sfilename[-1]
        filepath = data_folder / sfilename[-1]

        # Read info from waveguide s-param file
        with open(filepath, "r") as f:
            coeffs = f.readline().split()

        # Initialize array to hold s-params
        temp_s_ = np.zeros((len(self.f), self.nports, self.nports), dtype=complex)

        alpha = TE_loss / (20 * np.log10(np.exp(1)))

        # calculate angular frequency from frequency
        w = np.asarray(self.f) * 2 * np.pi

        # calculate center wavelength, effective index, group index, group dispersion
        lam0, ne, ng, nd = (
            float(coeffs[0]),
            float(coeffs[1]),
            float(coeffs[3]),
            float(coeffs[5]),
        )

        # calculate angular center frequency
        w0 = (2 * np.pi * self.c) / lam0

        # calculation of K
        K = (
            2 * np.pi * ne / lam0
            + (ng / self.c) * (w - w0)
            - (nd * lam0**2 / (4 * np.pi * self.c)) * ((w - w0) ** 2)
        )

        # compute s-matrix from K and waveguide length
        temp_s_[:, 0, 1] = temp_s_[:, 1, 0] = np.exp(
            -alpha * length + (K * length * 1j)
        )

        s = temp_s_
        self.ng_ = ng
        self.alpha_ = alpha
        self.ne_ = ne
        self.nd_ = nd

        return s
