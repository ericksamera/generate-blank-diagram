#!/usr/bin/env python3
"""
Purpose: Performs in-silico bisulfite conversion on a given sequence file.
"""
__author__ = "Erick Samera"
__version__ = "1.0.0"
__comments__ = "stable enough"
# --------------------------------------------------
from argparse import (
    Namespace,
    ArgumentParser,
    ArgumentDefaultsHelpFormatter)
from math import floor
from pathlib import Path
# --------------------------------------------------
from pytesseract import pytesseract
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
# --------------------------------------------------
def get_args() -> Namespace:
    """ Get command-line arguments """

    parser = ArgumentParser(
        #usage='%(prog)s',
        description="Performs in-silico bisulfite conversion on a given sequence file.",
        epilog=f"v{__version__} : {__author__} | {__comments__}",
        formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'input_path',
        type=Path,
        help="path of input file (.fasta/.gb) or dir of input files")
    parser.add_argument(
        '-o',
        '--out',
        dest='output_path',
        metavar='DIR',
        type=Path,
        help="path of output dir")

    args = parser.parse_args()

    # parser errors and processing
    # --------------------------------------------------
    args.input_path = args.input_path.resolve()
    if args.output_path:
        args.output_path = args.output_path.resolve()

    return args
# --------------------------------------------------
def _generate_words(tuple_arg: tuple) -> tuple:

    lowers_list = list(set([data[2] for data in tuple_arg]))
    words_list: list = []

    for pos in lowers_list:
        
        letters_list: list = []
        far_left_pos_list: list = []
        far_right_pos_list: list = []
        upper: int
        lower: int


        for data in tuple_arg:
            if data[0].lower() not in 'abcdefghijklmnopqrstuvwxyz': continue
            if data[2] == pos:
                letters_list.append(data[0])
                far_left_pos_list.append(data[1])
                far_right_pos_list.append(data[3])
                upper = data[4]
                lower = data[2]

        if letters_list:
            word = ''.join(letters_list)    
            words_list.append((word, min(far_left_pos_list), lower, max(far_right_pos_list), upper))
    print([i[0] for i in words_list])
    return words_list

    #print(tuple_arg)
def _soft_round(x, base=3): return round(int(x)/base)*base
def main() -> None:
    """ Insert docstring here """

    args = get_args()

    for file in args.input_path.glob('*'):
        imge = Image.open(file)
        data = pytesseract.image_to_boxes(imge)
        data_orig = tuple(tuple(i.split(' ')) for i in data.split('\n'))
        data_adjusted: list = []
        for data in data_orig:
            if len(data) > 1:
                letter = data[0]
                left_bound = _soft_round(data[1])
                right_bound = _soft_round(data[3])
                upper_bound = _soft_round(data[4])
                lower_bound = _soft_round(data[2])

                adjusted_data = tuple([letter, left_bound, lower_bound, right_bound, upper_bound])

                data_adjusted.append(adjusted_data)
        
        
        fig, ax = plt.subplots()
        ax.imshow(imge)
        for i in _generate_words(data_adjusted):
            length = i[3] - i[1]
            height = i[4] - i[2]
            #if i[0].lower() not in 'abcdefghijklmnopqrstuvwxyz': continue
            rect = patches.Rectangle((i[1], imge.height-i[4]), length, -height, linewidth=0, edgecolor='w', facecolor='blue')
            ax.add_patch(rect)
        plt.show()
        
        #for i in 
        #print(x)
# --------------------------------------------------
if __name__ == '__main__':
    main()
