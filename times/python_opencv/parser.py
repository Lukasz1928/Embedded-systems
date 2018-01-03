import argparse
from IncorrectArgumentsException import *

class ArgParser:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.parser = argparse.ArgumentParser(description="""Movement Detection,
                                         choose fragment to process""")
                                         
        self.parser.add_argument("-tl", nargs=2, type=int, required=False, default=[0, 0], metavar=("x1", "y1"), help="X and Y coordinates of the top left corner of proceeded area")
        self.parser.add_argument("-br", nargs=2, type=int, required=False, default=[height, width], metavar=("x2", "y2"), help="X and Y coordinates of the bottom right corner of proceeded area")
        
    def parse(self):
        args = self.parser.parse_args()
        if args.tl[0] >= args.br[0] or args.tl[1] >= args.br[1]:
            raise IncorrectArgumentsException("Coordinates must satisfy:\n0 <= x1 < x2 < {} and 0 <= y1 < y2 < {}".format(self.width, self.height)) 
        return args.tl[0], args.tl[1], args.br[0], args.br[1]
