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
    def __init__(self, file_location:str=None, name:str=None, **kwargs):
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

    def read_VASP_EIGENVALUE(self, file_location:str=None):
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

    def export_as_json(self, file_location:str=None):
        file_location = file_location if type(file_location) == str else self._file_location+'data.json'

        SP = self._get_specialpoints(self.kpoints)
        
        # Crear el formato JSON
        json_data = {
            "path": {
                "kpts": self._ndarray_2_dict(self.kpoints[:,:3]),
                "special_points": {sp:self._ndarray_2_dict(self.special_lattice_points[sp]) for sp in SP},
                "labelseq": ''.join(SP) 
                    },
            "energies": self._ndarray_2_dict(self.bands)
        }
        print(json_data)

    file_location = "your_file.json"
    try:
        with open(file_location, 'w') as outfile:
            json.dump(json_data, outfile, indent=4)
    except MemoryError:
        print("Memory Error occurred")
    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    def read_eigenvalues(self, file_location:str=None, subtractFermi:bool=True):
        file_location = file_location if type(file_location) == str else self._file_location

        inputFile_EIGENVAL = open(f'{file_location}/EIGENVAL', 'r')
        #inputFile_IBZKPT = open('IBZKPT', 'r')
        inputFile_DOSCAR = open(f'{file_location}/DOSCAR', 'r')

        for i in range(5):
            inputFile_EIGENVAL.readline()
            inputFile_DOSCAR.readline()
        #for i in range(3):
        #    inputFile_IBZKPT.readline()

        efermi = float(inputFile_DOSCAR.readline().split()[3])


        line = inputFile_EIGENVAL.readline()

        nelectrons     = int(line.split()[0])
        nkpt           = int(line.split()[1])
        neigen_per_kpt = int(line.split()[2])

        print( nelectrons, ' electrons')
        print( nkpt, ' kpoints')
        print( neigen_per_kpt, ' eigenvalues per kpoint')

        print( 'Fermi level at: ', efermi)

        #wkpt_array = numpy.zeros(nkpt, dtype=int)
        eigenvalue_array = []

        for i in range(nkpt):

            eigenvalue_array.append([])

            inputFile_EIGENVAL.readline()   # skips line before data
            inputFile_EIGENVAL.readline()   # this has kpoint and float weight

            # wkpt = float(inputFile_IBZKPT.readline().split()[3])
            #wkpt_array[i] = wkpt

            for j in range(neigen_per_kpt):
                eigenvalue = float(inputFile_EIGENVAL.readline().split()[1])
                eigenvalue_array[-1].append(eigenvalue)


        eigenvalue_list = []

        for i in range(nkpt):

            for eigenvalue in eigenvalue_array[i]:

                if (subtractFermi == True): 
                    eigenvalue_list.append(eigenvalue - efermi)
                else:
                    eigenvalue_list.append(eigenvalue)

        self._eigenvalue_list, self._nkpt, self._neigen_per_kpt = np.array(eigenvalue_list), np.array(nkpt), np.array(neigen_per_kpt)
        print(self._eigenvalue_list.shape, self._nkpt.shape)
        return eigenvalue_list, nkpt, neigen_per_kpt # wkpt_array

path = ''
ei = EigenvalueFileManager('/home/akaris/Documents/code/Physics/VASP/v6.1/files/EIGENVAL/EIGENVAL')
ei.read_VASP_EIGENVALUE()

ei.export_as_json()

'''

        self.n_electrons = None
        self.n_kpoints = None
        self.n_bands = None
        self.bands = None
        self.kpoints = None
        self.k_distance = None
'''

