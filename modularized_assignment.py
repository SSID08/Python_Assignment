import argparse
import os


def main(): 

    try: 
        import matplotlib #Check to see if Matplotlib exists in the virtual environment. 
    except ImportError:
        print('Matplotlib is a required module and it is missing from this virtual environment. Please install Matplotlib and then run the scipt again.')
        return #Exit the script if Matplotlib was not found in the virtual environment.

    try: 
        import seaborn #Check to see if Seaborn exists in the virtual environment. 
    except ImportError:
        print('Seaborn is a required module and it is missing from this virtual environment. Please install Seaborn and then run the scipt again.')
        return #Exit the script if Seaborn was not found in the virtual environment.

    try:
        import pandas # Check to see if Pandas exists in the virtual environment.
    except ImportError:
        print('Pandas is a required module and it is missing from this virtual environment. Please install Pandas and then run the scipt again.')
        return #Exit the script if Pandas was not found in the virtual environment.

    try: 
        import numpy #Check to see if Numpy exists in the virtual environment.
    except ImportError: 
        print('Numpy is a required module and it is missing from this virtual environment. Please install Numpy and then run the scipt again.')
        return #Exit the script if Numpy was not found in the virtual environment.
    
    
    try:#Check if the required modules for the script can be imported. 
        from bcf_parse_module import parse_bcf
        from plot_module import plot_bcf
    except ModuleNotFoundError:
        print( '\n'+'Module required to run this script was not found in the same directory/folder as this script. Either move the module to the same directory as the script\
or append the path to the module to the system path using sys.path.append() .',end='')
        return #Exit the function if the required modules were not found/were not able to be imported.


    #Create the argparser object
    parser=argparse.ArgumentParser(description='This script takes a Bcftools-stats file(with file name and file path),\
    parses the .vchk file and returns the different sections of the file to the specified folder depending on user input.\
    Further, it provides descriptive/exploratory plots for the numeric data',prog='BCF parser and analyser',exit_on_error=False)
    
    # Add required arguments and optional flags to the parser object.
    parser.add_argument('file_name',metavar='File name (with path)',type= str,help='This argument needs the file name (with path). This is a \
    required argument for the program to run')
    parser.add_argument('output_folder',metavar='Output Folder',type=str,help='This argument needs the ouptput folder name (with path). This is where ALL the requested output will be \
    saved in the required subfolders.')
    parser.add_argument('-sn','-SN',action='store_true',help='Return the section on Summary numbers from the Bcf-stats file. Saves the ouput file as a .txt file in the \'SN\' subfolder within the provided path.')
    parser.add_argument('-tstv','-TSTV',action='store_true',help='Returns the section on transitions\\transversions from the Bcf-stats file. Saves the output in a .txt file in the \'TSTV\' subfolder within the provided path.')
    parser.add_argument('-sis','-Singleton stats',action='store_true',help='Returns the section on Singleton stats from the Bcf-stats file. Saves the output in a .txt file in the \'SiS\' subfolder within the provided path')
    parser.add_argument('-af','-Stats on Allele frequency',action='store_true',help='Returns the section on ALLele Frequency stats from the Bcf-stats file. Saves the output in a .txt file in the \'AF\' subfolder within the path.')
    parser.add_argument('-q','-Stats on quality',action='store_true',help='Returns the section on quality from the Bcf-stats file. Saves the output as a .txt file in the \'Qual\' subfolder in the path.')
    parser.add_argument('-idd','-Stats on the InDel distribution',action='store_true',help='Returns the section on the distribution of InDels in the samples from the Bcf-stats file. Saves the output in a .txt file in the \'InDel\' subfolder within the path.')
    parser.add_argument('-st','-Stats on the Substitution type',action='store_true',help='Returns the section on the base pair substitutions statistics in the samples from the Bcf-stats file. Saves the output in the \'Subs_type\' subfolder as a .txt file within the path.')
    parser.add_argument('-dp','-Stats on the Depth distribution',action='store_true',help='Returns the section on the Depth Distribution statistics in the samples from the Bcf-stats file. Saves the output in the \'Depth_dist\' subfolder within the path as a .txt file.')
    parser.add_argument('-psc','-Per sample statistics',action='store_true',help='Returns the section on per sample count statistics from the bcf-stats file. Saves the output in the \'PSC\' subfolder within the path as a .txt file.')
    parser.add_argument('-psi','-Per sample Indels',action='store_true',help='Returns the section on Indel statistics from the bcf-stats file. Saves the output in the \'PSI\' subfolder within the path as a .txt file.')
    parser.add_argument('-hwe','-Hardy-Weinberg Equilibrium statistics',action='store_true',help='Returns the section on HWE statistics from the bcf-stats file. Saves the output in the \'HWE\' subfolder within the path as a .txt file.')
    parser.add_argument('-ALL','-all',action='store_true',help='Use this flag if you want to extract ALL the above mentioned sections from the bcf-stats file. This saves the output in their respective subfolder within the path as a .txt file.')
    
    args=parser.parse_args()

    try: #Check if the file passed as the argument exists in the given path.
        if not os.path.isfile(args.file_name):
            raise FileNotFoundError
        elif not (os.path.splitext(args.file_name)[-1].lower() == '.vchk'):
            raise TypeError
    except FileNotFoundError:
        print('Input file path is not valid. Please check and run this script again after.')
        return #Exit the script if the input file was not found at the input location.
    except TypeError:
        print('The input file does not have a .vhck extension. This script is only made to work with a vchk files. Please try again with a valid file.')
        return

    try: #Check if path to the output folder argument exists.
        if not os.path.exists(args.output_folder):
            raise FileNotFoundError
    except FileNotFoundError:
        print('Output folder path is not valid. Please check and run this script again after.')
        return #Exit if path to the output folder argument does not exist.

    parse_bcf(args.file_name,args.output_folder,args) # Parse the input bcf_stats file and exrtact the required information into the subfolders.
    plot_bcf(args.output_folder,args) # Plot the requested information and export the plots to their respective sub-folders.


if(__name__=="__main__"):
    main()