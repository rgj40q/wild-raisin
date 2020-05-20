Requires python v3, and packages 'pypeg2' and 'lxml' to run. To install the packages, run in the terminal (e.g. Cygwin):

    python -m pip install --upgrade pip
    pip install --upgrade pypeg2
    pip install --upgrade lxml

Usage:

    echo "some text to be parsed" | ./parser.py

or:

    ./parser.py < input.txt > output.txt
