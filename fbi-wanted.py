
# import fbi      # Credits @rly0nheart GitHub 

# import argparse

#!/usr/bin/env python3
import argparse
from lib.support_fbi import *
from lib import banner, colors

print(banner.banner)



if __name__ == '__main__':
    while True:
        try:
        	Fbi(args).on_connection()
        	break
        	
        except KeyboardInterrupt:
        	if args.verbose:
        		print(f'\n{colors.white}[{colors.red}x{colors.white}] Process interrupted with {colors.red}Ctrl{colors.white}+{colors.red}C{colors.reset}')
        		break
        	break
        	
        except Exception as e:
        	if args.verbose:
        		print(f'{colors.white}[{colors.red}!{colors.white}] Error: {colors.red}{e}{colors.reset}')
    
    if args.verbose:
    	exit(f'{colors.white}[{colors.green}-{colors.white}] Finished in {colors.green}{datetime.now()-start_time}{colors.white} seconds.{colors.reset}')



