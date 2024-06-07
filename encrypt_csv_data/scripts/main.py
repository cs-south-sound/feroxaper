'''
Encrypt or smudge CSV files, leave the smudged headers unencrypted
'''

import argparse  # command line input
from cryptography.fernet import Fernet
import logging   # standardized messaging to console or logfile
import os           # access the directory filenames
from pathlib import Path
import pandas as pd # manipulate dataframes input from csv files
from rich.console import Console    # pretty print the readme as help
from rich.markdown import Markdown

version = "rc_0.0.3"

# use command line argument `--verbose` to select logging.DEBUG
# defaulting here to info
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info(version)

# encryption
def generate_key(secret_key):
    return Fernet.generate_key() + secret_key.encode()


def encrypt_data(key, variable):
    f = Fernet(key)
    encrypted_data = f.encrypt(str(variable).encode())
    # sanity check the encryption
    decrypted_data = decrypt_data(key, encrypted_data)
    if str(variable) == str(decrypted_data):
        #the encryption succeeded
        pass
    else:
        msg = "The input value causing the error is: " + str(variable)
        msg += "  The decrypted_data is: " + str(decrypted_data)
        logger.warning(msg)


        msg = "In function encrypt_data the decrypted data does not match the input variable \n"
        msg += "For example type(variable): " + str(type(variable))
        msg += "   ne type(decrypted_data): "+ str(type(decrypted_data))
        raise ValueError(msg)
    return encrypted_data


def decrypt_data(key, encrypted_data):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data).decode()
    return decrypted_data


# smudging
def smudge(cleartxt):
    # Use the adjacent ASCII character as a replacement
    cleartxt_string = str(cleartxt)
    smudged = "".join([ chr(ord(c)+1) for c in cleartxt_string])
    return smudged

# help
def help(relative_path_to_readme):
    with open(relative_path_to_readme, "r") as f:
        readme_markdown = f.read()
        console = Console(force_terminal=bool(os.environ.get("rich_force_terminal", True)))
        md = Markdown(readme_markdown)
        console.print(md)

#

def construct_absolute(path_to):
    parent_directory = str(Path(__file__).parent)
    absolute_path_object  = Path(os.path.join(parent_directory, path_to))
    absolute_path_to  = str(absolute_path_object.resolve())
    return str(absolute_path_to)

#


def main():
    path_to_input = "../data/"
    path_to_output = "../output_data/"
    path_to_readme = "../README.md"


    path_to = {
            "data_in" : "../data/",
            "output": "../output_data/",
            "output_e": "",
            "output_s": "",
            "readme": "../README.md"
            }

    def get_absolute_paths(path_to, filename):

        path_to['data_in'] += path_to['data_in'] + filename
        path_to['output_e'] = path_to['output'] + "encrypted-" + filename
        path_to['output_s'] = path_to['output'] + "smudged-" + filename

        absolute_path_to = {}
        absolute_path_to['input'] = construct_absolute(path_to['data_in'])
        absolute_path_to['output_e'] = construct_absolute(path_to['output_e'])
        absolute_path_to['output_s'] = construct_absolute(path_to['output_s'])
        absolute_path_to['readme'] = construct_absolute(path_to['readme'])
        return absolute_path_to


    parser = argparse.ArgumentParser(description='Encrypt or smudge CSV data')
    parser.add_argument("--augmented_help",  action='store_true', default="", help="Verbose help")
    parser.add_argument('-v', '--version', action='store_true', default='',
                        help="Print the version of this script")
    e_help = "Encrypt headers and data  with Fernet. Your super-secret key required as an argument"
    parser.add_argument('-e', '--encrypt', nargs=1, default='', help=e_help)
    s_help = "Smudge the input data to make it less readable"
    parser.add_argument('-s', '--smudge', action='store_true', default='', help=s_help)
    f_help = "Where FILENAMES is a python style list of filenames in data/, like [example-100.csv]."
    f_help += "  Current version only retrieves the first item."
    parser.add_argument('-f', '--filenames', nargs='?',
                         default='[example-100.csv]', const='[example-100.csv]',  help=f_help)

    parser.add_argument('--verbose', action='store_true', default='', help='Print debugging messages')
    args = parser.parse_args()

#

    if args.verbose:
        global logger
        logger.setLevel(logging.DEBUG)
        logger = logging.getLogger(__name__)

#
    filenames_string = args.filenames
    # Converting string to list
    filenames_list = filenames_string.strip('][').split(',')
    filename = filenames_list[0] # only gets the first name in the list
    # TODO
    # At this point the list needs to be iterated
    # to get each file name, then each file will
    # be encrypted in turn
    # TODO

    paths = get_absolute_paths(path_to, filename)
    if args.verbose:
        logger.debug("Paths:")
        for i in paths:
            msg = i + ": " + paths[i]
            logger.debug(msg)

#

    if args.augmented_help:
        help(paths['readme'])
        exit()

    if args.version:
        msg = "version: " + version
        logger.info(msg)
        logger.info(Path(__file__))
        exit()

    # Choose between strong encryption to require a key for
    # encryption or choose smudging the data to make it not
    # human readable.  Smudging is just ASCII char + 1, very
    # easy to guess and not secure.  Default to strong encryption.

    default_to_encryption = "yes"

    if args.smudge and args.encrypt:
        print("Select encrypt or smudge option, but not both!")
        exit()

    if args.smudge:
        default_to_encryption = "no"

    if args.encrypt:
        default_to_encryption = "yes"

    if args.verbose:
        msg = "args.filenames: " + args.filenames
        logger.debug(msg)

    if args.filenames == '[example-100.csv]':
        msg = "The default file 'data/example-100.csv' will be used."
        logger.info(msg)
        msg = "To process your own files try option -f '[myfile1.csv, myfile2.csv]'"
        logger.info(msg)

    # Read data from a csv file
    try:
        data = pd.read_csv(paths['input'])
    except FileNotFoundError as fnf_error:
        error_type = str(type(fnf_error)).strip("<>'").replace("'",'')
        error_type = error_type.replace("class","").replace(" ","")
        logger.error(error_type)
        msg = "Files to be encrypted must be placed in the data/ directory "
        msg += "and spelled correctly as an argument to the -f option. "
        msg += "For more help try the --augmented_help option."
        logger.error(msg)
        exit()

    # Replace variables that are missing with a ''
    data.fillna('', inplace=True)

    if args.verbose:
        msg = "First five lines of csv file in pandas dataframe"
        logger.debug(msg)
        print(data.head().to_string())

    # Capture the column headers unencrypted
    unencrypted_headers_list = data.columns.tolist()
    unencrypted_header_row_df = pd.DataFrame(columns=unencrypted_headers_list)

    if default_to_encryption == "yes":
        try:
            key = generate_key(args.encrypt[0])
        except IndexError: #string index out of range, ie no argparse values
            logger.warning("Please use options `--encrypt with_my_super_secret_key` OR `--smudge`")
            help(paths['readme'])
            exit()

        # encrypt each element of the header and the data
        encrypted_head  = unencrypted_header_row_df.map(lambda x: encrypt_data(key, x), na_action=None)
        encrypted_dataz = data.map(lambda x: encrypt_data(key, x), na_action=None)
        # write to output file (overwrites an existing file name)
        encrypted_head.to_csv( paths['output_e'], index=False, mode='w', header=False)
        encrypted_dataz.to_csv(paths['output_e'], index=False, mode='a', header=False)
        logger.info("Encryption complete.")
        msg = "Find output in " + paths['output_e']
        logger.info(msg)

    elif default_to_encryption == "no":
        # smudge
        # Write the unencrypted first row to a new file
        unencrypted_header_row_df.to_csv(paths['output_s'], index=False, mode='w')
        encrypted_dataz = data.map(lambda x: smudge(x), na_action=None)
        # Append the encrypted data to the same file
        encrypted_dataz.to_csv(paths['output_s'], index=False, mode='a', header=False)
        logger.warning("The output has been smudged, it is not encrypted.")
        logger.warning("Anyone can retranslate the data.")
        logger.info("Smudging complete.")
        msg = "Find output in " + paths['output_s']
        logger.info(msg)
# # # # # # # # # # # # # # #


if __name__ == "__main__":
    main()
