#!/usr/bin/env python3
import argparse
from lib.support_fbi import *
from rich import print
from lib import banner
print(banner.banner)


if __name__ == '__main__':
    while True:
        try:
        	Fbi(args).on_connection()
        	break
        	
        except KeyboardInterrupt:
        	if args.verbose:
        		print(f'\n[x] Process interrupted with Ctrl+C')
        		break
        	break
        	
        except Exception as e:
        	if args.verbose:
        		print(f'[!] Error: {e}')
    
    if args.verbose:
    	exit(f'[-] Finished in {datetime.now()-start_time} seconds.')



