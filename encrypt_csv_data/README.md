# Encrypt or smudge a CSV file 

- **Usage**

  - __venv__ suggested virtual environment setup

    ```bash
    python -m venv venv             # once per project
    pip install -r requirements.txt # once every time there is a package update
    . venv/bin/activate             # required once before running the script
    echo $VIRTUAL_ENV               # fyi
    deactivate                      # when the venv is not longer needed
    ```

  - __Help__


    ```bash
    python3 scripts/main.py -h
    python3 scripts/main.py --augmented_help | less -R # rich print from the README.md
    ```

  - __Data__

    Place your well formed csv files in the data/ directory before running this script.

  - __Filenames__

    Where FILENAMES is a python style list of filenames in data/, like [example-100.csv].
    This version of the script only retrieves the first item of the list.  Omiting
    your filename will result in the `example-100.csv` being used as the default.

    ```bash
    python3 scripts/main.py -f [FILENAMES]
    python3 scripts/main.py --filenames [FILENAMES]
    ```

  - __Smudge__ obfuscates the data by shifting each ASCII character code by +1.
    The data is not encrypted! Anyone can figure out how to retranslate the smudge.
    No secret key is expected.  Kind of like Lorem Ipsum for data!  The first
    line of the CSV is expected to contain a header describing the data.  The
    header line is not encrypted.


    ```bash
    python3 scripts/main.py -f [FILENAMES] -s
    python3 scripts/main.py --filenames [FILENAMES] --smudge
    ```

  - __Encrypt__ with Fernet, which "guarantees that a message encrypted
    using it cannot be manipulated or read without the key. Fernet is an
    implementation of symmetric (also known as “secret key”) authenticated
    cryptography." This option encrypts all lines of the input file.


    ```bash
    python3 scripts/main.py -f [FILENAMES] -e with_my_super_secret_key
    python3 scripts/main.py --filenames [FILENAMES] --encrypt with_my_super_secret_key
    ```



- Data locations

1. Input CSV files
   > Found in the `data/` directory

2. Output encrypted or smudged files
   > To the `output_data/` directory


- Reference

1. Fernet [:link:](https://cryptography.io/en/latest/fernet/)
