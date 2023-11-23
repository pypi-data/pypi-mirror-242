try:
    from sage_lib.FileManager import FileManager
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing FileManager: {str(e)}\n")
    del sys

try:
    import numpy as np
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing numpy: {str(e)}\n")
    del sys

try:
    import json
except ImportError as e:
    import sys
    sys.stderr.write(f"An error occurred while importing json: {str(e)}\n")
    del sys

class EigenvalueFileManager(FileManager):
    def __init__(self, file_location:str=None, name:str=None, cell:np.array=None, fermi:float=None, **kwargs):
        """
        Initialize OutFileManager class.
        :param file_location: Location of the file to be read.
        :param name: Name identifier for the file.
        :param kwargs: Additional keyword arguments.
        """
        super().__init__(name=name, file_location=file_location)
        self._comment = None

        self._bands = None
        self._kpoints = None
        self._k_distance = None

        self._fermi = fermi
        self._cell = cell

    def read_EIGENVAL(self, file_location:str=None):
        file_location = file_location if type(file_location) == str else self._file_location
        lines = [n for n in self.read_file(file_location) ]
        
        self.bands, self.kpoints=[], []
        var = -1
        for i, n in enumerate(lines):

            vec = [float(m) for m in n.split(' ') if self.is_number(m) ] 
            if i == 5: self.bands = np.zeros((int(vec[1]), int(vec[2]), 4))
            if len(vec) == 4 and i>5: self.kpoints.append(vec); var+=1
            if len(vec) == 5 and i>5: self.bands[var,int(vec[0]-1), :] = vec[1:]

        self.k_distance = np.zeros((len(self.kpoints)))
        var = 0
        for n in range(len(self.k_distance)-1): 
            var += ((self.kpoints[n][0]-self.kpoints[n+1][0])**2+(self.kpoints[n][1]-self.kpoints[n+1][1])**2+(self.kpoints[n][2]-self.kpoints[n+1][2])**2)**0.5
            self.k_distance[n+1] = var

        self.kpoints = np.array(self.kpoints)
        self.bands = np.array(self.bands)
        self.k_distance = np.array(self.k_distance)

        return True

    def _ndarray_2_list(self, array):
        return [list(array.shape), str(array.dtype), list(array.flatten(order='C'))]

    def _ndarray_2_dict(self, array):
        return {'__ndarray__':self._ndarray_2_list(array)}

    def _get_specialpoints(self, kpoints:np.array) -> list:
        """Check if points in a kpoints matrix exist in a lattice points dictionary."""
        found_points = []

        for point in kpoints:
            for label, special_lattice_point in self.special_lattice_points.items():
                # Compare only the first three elements (x, y, z coordinates)
                if self.is_close(point[:3], special_lattice_point[:3]):
                    found_points.append( label )
                    break

        return found_points
    
    def subtract_fermi(self, fermi:float=None):
        fermi = fermi if fermi is not None else self.fermi 

        self.bands[:,:,:2] -= fermi 
        self.fermi = 0
        
        return True

    def export_as_json(self, file_location:str=None, subtract_fermi:bool=True) -> True:
        file_location = file_location if type(file_location) == str else self._file_location+'data.json'

        if subtract_fermi: self.subtract_fermi()

        SP = self._get_specialpoints(self.kpoints)
        
        # Crear el formato JSON
        json_data = {
            "path": {
                "kpts": self._ndarray_2_dict(self.kpoints[:,:3]),
                "special_points": {sp:self._ndarray_2_dict(self.special_lattice_points[sp]) for sp in SP},
                "labelseq": ''.join(SP),
                "cell": {"array": self._ndarray_2_dict(self.cell), "__ase_objtype__": "cell"},
                "__ase_objtype__": "bandpath"

                    },
            "energies": self._ndarray_2_dict(self.bands[:,:,0]),
            "reference": self.fermi,
            "__ase_objtype__": "bandstructure"
        }

        self.save_to_json(json_data, file_location)
        
        return True

'''
ei = EigenvalueFileManager('/home/akaris/Documents/code/Physics/VASP/v6.1/files/EIGENVAL/EIGENVAL', fermi=0)
ei.read_VASP_EIGENVALUE()
print(ei.bands.shape)
ei.export_as_json()

path = '/home/akaris/Documents/code/Physics/VASP/v6.1/files/EIGENVAL/bs_wz_ZnO.json'
with open(path, 'r') as file:
    data = json.load(file)
print( data['path'].keys() )

path = '/home/akaris/Documents/code/Physics/VASP/v6.1/files/EIGENVAL/EIGENVALdata.json'
with open(path, 'r') as file:
    data = json.load(file)
print( data['path'].keys() )

import matplotlib.pyplot as plt
plt.plot( ei.bands[:,:,1] )
plt.show()

#


        self.n_electrons = None
        self.n_kpoints = None
        self.n_bands = None
        self.bands = None
        self.kpoints = None
        self.k_distance = None
'''

