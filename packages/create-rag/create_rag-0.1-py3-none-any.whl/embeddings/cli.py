import argparse
from .core import init, configure_index 

def main():
    parser = argparse.ArgumentParser(description='Embeddings CLI')
    parser.add_argument('--init', help='Initialize API key', required=False)

    
    args = parser.parse_args()
    
    if args.init:
        init(args.init)

if __name__ == '__main__':
    main()
