import argparse

class ArgParser:

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="""Edge detection. Choose algorithm""")
        
        self.parser.add_argument("-c", action='store_true', help="Use Canny method")                                
        self.parser.add_argument("-r", action='store_true', help="Use Roberts cross algorithm")
        self.parser.add_argument("-l", action='store_true', help="Use Laplacian algorithm")
        self.parser.add_argument("-s", action='store_true', help="Use Sobel algorithm")
        self.parser.add_argument("-sc", action='store_true', help="Use Scharr algorithm")
        
    def parse(self):
        args = self.parser.parse_args()
        if args.c:
            return 'canny'
        elif args.r:
            return 'cross'
        elif args.l:
            return 'laplacian'
        elif args.sc:
            return 'scharr'
        else:
            return 'sobel'
        
