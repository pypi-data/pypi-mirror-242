import argparse
import os
from sage_lib import DFTPartition, SurfaceStatesGenerator, VacuumStatesGenerator, EigenvalueFileManager, DOSManager, PeriodicSystem # Importing necessary classes

def generate_xyz_from_outcar(path, subfolders=False, verbose=False):
    """
    Generate an XYZ file from a VASP OUTCAR file.

    Parameters:
    path (str): Path to the VASP OUTCAR file.
    subfolders (bool, optional): Whether to search in subfolders. Defaults to False.
    verbose (bool, optional): If True, prints additional information. Defaults to False.
    """
    DP = DFTPartition(path)
    read_files(partition=DP, path=path, subfolders=subfolders)
    DP.export_configXYZ()

    
def generate_vacancy(path, subfolders=False, verbose=False):
    """
    Generate configurations with vacancies.

    Parameters:
    - path (str): Path to the VASP files directory.
    - verbose (bool): If True, prints additional information.
    """
    DP = DFTPartition(path)
    read_files(partition=DP, path=path, subfolders=subfolders)
    
    DP.generateDFTVariants('Vacancy', [1])
    DP.exportVaspPartition()

def generate_disassemble_surface(path, steps=5, final_distance=5.0, atoms_to_remove=None, subfolders=False, verbose=False):
    """
    Generate configurations for disassembling the surface.

    Parameters:
    - path (str): Path to the VASP files directory.
    - steps (int): Number of steps in the disassembly process.
    - final_distance (float): Final distance between layers or atoms.
    - atoms_to_remove (int or None): Specific number of atoms to remove.
    - verbose (bool): If True, prints additional information.
    """
    SSG = SurfaceStatesGenerator(path)
    read_files(partition=SSG, path=path, subfolders=subfolders)

    SSG.generate_disassemble_surface(steps=steps, final_distance=final_distance, atoms_to_remove=atoms_to_remove)
    SSG.exportVaspPartition()

def generate_dimers(path=None, labels:list=None, steps:int=10, vacuum:float=18.0, subfolders=False, verbose=False):
    """
    Generate configurations for dimer search.

    Parameters:
    - path (str): Path to the VASP files directory (optional if labels are provided).
    - labels (list of str): List of atom labels (optional if path is provided).
    - steps (int): Number of steps in the dimer search.
    - vacuum (int): Specific vacuum distance.
    - verbose (bool): If True, prints additional information.
    """
    VSG = VacuumStatesGenerator(path)
    read_files(partition=VSG, path=path, subfolders=subfolders)

    if labels is not None: 
        VSG.generate_dimers(AtomLabels=labels, steps=steps )
    else: 
        VSG.generate_dimers(steps=steps )

    VSG.exportVaspPartition()

def generate_config(path:str=None, source:str=None, subfolders:bool=None, config_path:str=None, output_path:str=None, output_source:str=None, verbose=False):
    """
    Generate VASP partition and execution script for each container.

    Parameters:
    - path (str): Path to the VASP files directory.
    - config_path (str): Path to the configuration file.
    - output_path (str): Path for exporting VASP partition and scripts.
    - verbose (bool): If True, prints additional information.
    """
    DP = DFTPartition(path)
    read_files(partition=DP, path=path, source=source, subfolders=subfolders, verbose=verbose)

    DP.readConfigSetup(config_path)
    if output_source.upper() == 'VASP':
        DP.exportVaspPartition(output_path, label='enumerate')
    
    DP.generate_execution_script_for_each_container([f'{n:03d}' for n, c in enumerate(DP.containers)], output_path)

    if verbose:
        print("Script and VASP partition generated successfully.")

def generate_band_calculation(path:str, points:int, special_points:str, source:str=None, subfolders:bool=False, output_path:str=None, verbose:bool=False):
    """
    Generate and export band structure calculation files.

    This function creates the necessary files for performing band structure calculations using Density Functional Theory (DFT) data. It sets up the calculation parameters and exports them in a format suitable for VASP.

    Parameters:
    path (str): Path to the directory containing VASP files.
    points (int): Number of k-points in each segment of the band path.
    special_points (str): String representing high-symmetry points in the Brillouin zone.
    source (str, optional): Source of the files (default is None, typically set to 'VASP').
    subfolders (bool, optional): Whether to include subfolders in the search (default False).
    output_path (str, optional): Directory path where the output files will be saved.
    verbose (bool, optional): If True, provides detailed output during execution.

    Returns:
    None
    """
    DP = DFTPartition(path)
    read_files(partition=DP, path=path, source=source, subfolders=subfolders, verbose=verbose)

    DP.generateDFTVariants('band_structure', values=[{'points':points, 'special_points':special_points}])
    DP.exportVaspPartition(output_path+'/band_structure')


def generate_json_from_bands(path:str, fermi:float, source:str=None, subfolders:bool=False, output_path:str=None, verbose:bool=False):
    """
    Generate a JSON file from band structure data.

    This function reads the band structure data from VASP output files, processes it, and exports it to a JSON file. This is useful for further analysis or visualization of the band structure.

    Parameters:
    path (str): Path to the directory containing VASP files.
    fermi (float): Fermi level energy. If not provided, it will be read from the DOSCAR file.
    source (str, optional): Source of the files ('VASP' is a common option).
    subfolders (bool, optional): Whether to include subfolders in the search (default False).
    output_path (str, optional): Directory path where the JSON file will be saved.
    verbose (bool, optional): If True, provides detailed output during execution.

    Returns:
    None
    """
    if source.upper() == 'VASP':
        # read fermi level from DOSCAR
        if fermi is None:
            # === read DOCAR === #
            DM = DOSManager(path + "/DOSCAR")
            DM.read_DOSCAR()
            fermi = DM.fermi

        # === read POSCAR === #
        PC = PeriodicSystem(path + "/POSCAR")
        PC.readPOSCAR()
        cell = PC.latticeVectors

        # === read EIGENVAL === #
        EFM = EigenvalueFileManager(file_location=path + "/EIGENVAL", fermi=fermi, cell=cell)
        EFM.read_EIGENVAL()

    EFM.export_as_json(output_path+'/band_structure.json')

def generate_export_files(path:str, source:str=None, subfolders:bool=False, output_path:str=None, output_source:str=None, verbose:bool=False):
    """
    Export atomic position files from a specified source format to another format.

    This function is used to convert the format of atomic position files, which is often necessary for compatibility with different simulation tools or visualization software.

    Parameters:
    path (str): Path to the directory containing source format files.
    source (str, optional): Source format of the files (e.g., 'VASP').
    subfolders (bool, optional): Whether to include subfolders in the search (default False).
    output_path (str, optional): Directory path where the converted files will be saved.
    output_source (str, optional): Target format for exporting (e.g., 'PDB').
    verbose (bool, optional): If True, provides detailed output during execution.

    Returns:
    None
    """
    DP = DFTPartition(path)
    read_files(partition=DP, path=path, source=source, subfolders=subfolders, verbose=verbose)

    if output_source.upper() == 'PDB':
        for container in DP.containers:
            container.AtomPositionManager.export_as_PDB()

def generate_plot(path:str, source:str=None, subfolders:bool=False, output_path:str=None, plot:str=None, verbose:bool=False,
                    fermi:float=None):
    """
    Generate plots from simulation data.

    This function processes simulation data and generates plots, such as band structure or molecular structures, based on the data and specified plot type.

    Parameters:
    path (str): Path to the directory containing the simulation data files.
    source (str, optional): Source of the files (e.g., 'VASP').
    subfolders (bool, optional): Whether to include subfolders in the search (default False).
    output_path (str, optional): Directory path where the plots will be saved.
    plot (str, optional): Type of plot to generate (e.g., 'band').
    verbose (bool, optional): If True, provides detailed output during execution.
    fermi (float, optional): Fermi level energy, important for certain types of plots.

    Returns:
    None
    """
    DP = DFTPartition(path)
    read_files(partition=DP, path=path, source=source, subfolders=subfolders, verbose=verbose)


    if plot.upper() == 'BANDS':
        if fermi is None:
            # === read DOCAR === #
            DM = DOSManager(path + "/DOSCAR")
            DM.read_DOSCAR()
            fermi = DM.fermi

        # === read EIGENVAL === #
        EFM = EigenvalueFileManager(file_location=path+"/EIGENVAL", fermi=fermi )
        EFM.read_EIGENVAL()

        EFM.plot()

def generate_atom_move(path:str, source:str=None, subfolders:bool=False, output_path:str=None, output_source:str=None, verbose:bool=False, move:str=None, N:int=None, std:float=None):
    """

    """
    DP = DFTPartition(path)
    read_files(partition=DP, path=path, source=source, subfolders=subfolders, verbose=verbose)

    if output_source.upper() == 'rattle':
        DP.generateDFTVariants('rattle', [ {'N':N, 'std':[0]} ] )

def read_files(partition, path=None, source='VASP', subfolders=False, verbose=False):
    """
    Read files from a specified path and store in a given partition object.

    Parameters:
    partition (DFTPartition): The DFTPartition object to which files are read into.
    path (str, optional): Path to read files from. If None, uses partition's file location.
    source (str, optional): Source of the files (VASP or XYZ). Defaults to 'VASP'.
    subfolders (bool, optional): Whether to include subfolders in the search. Defaults to False.
    verbose (bool, optional): Enables verbose output. Defaults to False.
    """
    path = path if path is not None else partition.file_location
    absolute_path = os.path.abspath(path)
    partition._file_location = absolute_path

    # Reading files based on the specified source
    if source.upper() == 'VASP':
        if subfolders:
            partition.readVASPSubFolder(absolute_path)
        else:
            partition.readVASPFolder(absolute_path)
    elif source.upper() == 'XYZ':
        partition.read_configXYZ(absolute_path)

def add_arguments(parser):
    parser.add_argument('--path', type=str, default='.', help='Path to the files directory')
    parser.add_argument('--verbose', action='store_true', help='Display additional information')
    parser.add_argument('--subfolders', default=False, action='store_true', help='Read from all subfolders under the specified path')
    parser.add_argument('--source', type=str, choices=['VASP', 'GAP', 'xyz'], default='VASP', help='Source of calculation from which the files originate: VASP, molecular_dynamics, or force_field (default: VASP)')
    parser.add_argument('--output_path', type=str, default='.', help='Path for exporting VASP partition and scripts')

def main():
    """
    Main function to handle command line arguments and execute respective functions.
    """
    parser = argparse.ArgumentParser(description='Tool for theoretical calculations in quantum mechanics and molecular dynamics.')
    subparsers = parser.add_subparsers(dest='command', help='Available sub-commands')

    # =========== Sub-command to generate vacancy directory ===========
    parser_vacancy = subparsers.add_parser('vacancy', help='Generate vacancy.')
    add_arguments(parser_vacancy)

    # =========== Sub-command to generate XYZ file from an OUTCAR directory ===========
    parser_xyz = subparsers.add_parser('xyz', help='Generate an XYZ file from an OUTCAR directory.')
    add_arguments(parser_xyz)

    # =========== Sub-command to generate configurations for disassembling the surface ===========
    parser_disassemble = subparsers.add_parser('disassemble', help='Generate configurations for disassembling the surface.')
    add_arguments(parser_disassemble)
    parser_disassemble.add_argument('--steps', type=int, default=5, help='Number of steps in disassembly (default: 5)')
    parser_disassemble.add_argument('--final_distance', type=float, default=5.0, help='Final distance between layers or atoms (default: 5.0)')
    parser_disassemble.add_argument('--atoms_to_remove', type=int, help='Specific number of atoms to remove')

    # =========== Sub-command: dimer ===========
    parser_dimer = subparsers.add_parser('dimer', help='Generate configurations for dimer search.')
    add_arguments(parser_dimer)
    parser_dimer.add_argument('--labels', nargs='+', help='List of atom labels for dimer search')
    parser_dimer.add_argument('--steps', type=int, default=10, help='Number of steps in the dimer search (default: 10)')
    parser_dimer.add_argument('--vacuum', type=int, default=18, help='Specific vacuum distance (default: 18)')

    # =========== Sub-comando para generar script ===========
    parser_config = subparsers.add_parser('config', help='Read Position data from "path", read Configurtion data from "config_path" and export to "output_path".')
    add_arguments(parser_config)
    parser_config.add_argument('--config_path', type=str, required=True, help='Path to the configuration file')
    parser_config.add_argument('--output_source', type=str, default='VASP', help='Source for exporting partition and scripts')

    # =========== Sub-comando para generar BAND files ===========
    parser_bands = subparsers.add_parser('bands', help='Configure parameters for generating band calculation files from VASP data.')
    add_arguments(parser_bands)
    parser_bands.add_argument('--points', type=int, help='Specifies the number of k-points in each segment of the band path. It should be an integer value representing the total number of k-points along the path.')
    parser_bands.add_argument('--special_points', type=str, required=True, default='GMMLLXXG', help='Defines special points in the Brillouin zone for band calculations. Should be a character string representing points, for example, "GMXLG", indicating the high-symmetry points along the band path.')

    # =========== Sub-command for ganerate .JSON files from EIGENVAL ===========
    parser_bands2json = subparsers.add_parser('bands2json', help='Configure parameters for generating band calculation files from VASP data.')
    add_arguments(parser_bands2json)
    parser_bands2json.add_argument('--fermi', type=float, help='Specifies the energy of the fermi level.')

    # =========== Sub-command for export files from SOURCE format to OUTPUT format ===========
    parser_export_position = subparsers.add_parser('export_position', help='Export atomic positions from a specified source format to a desired output format. This is useful for converting file formats for compatibility with various simulation and visualization tools.')
    add_arguments(parser_export_position)
    parser_export_position.add_argument('--output_source', type=str, default='VASP', help='Specifies the target format for exporting. For example, "VASP" or "PDB".')

    # =========== Sub-command for PLOT files from SOURCE format to OUTPUT format ===========
    parser_plot = subparsers.add_parser('plot', help='Generates plots based on data from a specified source. This can include plotting energy bands, density of states, or molecular structures, depending on the input data and specified plot type.')
    add_arguments(parser_plot)
    parser_plot.add_argument('--plot', type=str, default='bands', help='Specifies the type of plot to generate, such as "band" for band structure plots.')
    parser_plot.add_argument('--fermi', type=float, help='Specifies the energy of the Fermi level, which is essential for accurate band structure plots.')

    # =========== Sub-command for PLOT files from SOURCE format to OUTPUT format ===========
    parser_plot = subparsers.add_parser('move_position', help='')
    add_arguments(parser_plot)
    parser_plot.add_argument('--move', type=str, default='rattle', help='')
    parser_plot.add_argument('--std', type=float, required=False, help='')
    parser_plot.add_argument('--N', type=float, required=False, help='')

    args = parser.parse_args()

    # Handle execution based on the specified sub-command
    if   args.command == 'xyz':
        generate_xyz_from_outcar(args.path, subfolders=args.subfolders, verbose=args.verbose)
    
    elif args.command == 'vacancy':
        generate_vacancy(args.path, subfolders=args.subfolders, verbose=args.verbose)
    
    elif args.command == 'disassemble':
        generate_disassemble_surface(args.path, steps=args.steps, final_distance=args.final_distance, atoms_to_remove=args.atoms_to_remove, subfolders=args.subfolders, verbose=args.verbose)
    
    elif args.command == 'dimer':
        generate_dimers(path=args.path, labels=args.labels, steps=args.steps, vacuum=args.vacuum, subfolders=args.subfolders, verbose=args.verbose)
    
    elif args.command == 'config':
        generate_config(path=args.path, source=args.source, subfolders=args.subfolders, config_path=args.config_path, 
                        output_path=args.output_path, output_source=args.output_source, verbose=args.verbose)
    
    elif args.command == 'bands':
        generate_band_calculation(path=args.path, source=args.source, fermi=fermi,
                        subfolders=args.subfolders, verbose=args.verbose, output_path=args.output_path)
    
    elif args.command == 'bands2json':
        generate_json_from_bands(path=args.path, source=args.source, fermi=args.fermi,
                        subfolders=args.subfolders, verbose=args.verbose, output_path=args.output_path)

    elif args.command == 'export_position':
        generate_export_files(path=args.path, source=args.source, subfolders=args.subfolders, 
            verbose=args.verbose, output_path=args.output_path, output_source=args.output_source)

    elif args.command == 'plot':
        generate_plot(path=args.path, source=args.source, subfolders=args.subfolders, 
            verbose=args.verbose, output_path=args.output_path, plot=args.plot, fermi=args.fermi)

    elif args.command == 'move_position':
        generate_atom_move(path=args.path, source=args.source, subfolders=args.subfolders, 
            verbose=args.verbose, output_path=args.output_path, move=args.move, std=args.std)

if __name__ == '__main__':
    main()