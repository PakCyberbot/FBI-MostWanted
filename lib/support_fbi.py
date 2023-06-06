import fbi      # Credits @rly0nheart GitHub 
import argparse
import requests
import re
from tqdm import tqdm
import logging
from datetime import datetime
import os
from git import Repo
import subprocess

# Support for MultiThreading
from concurrent.futures import ThreadPoolExecutor

# Support for slow download to mimic human traffic, reducing the risk of being banned or flagged
import random
import time

# Setting up rich library
from rich.console import Console
from rich.table import Table
from rich.theme import Theme
from rich.style import Style
from rich_argparse import RichHelpFormatter
custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red"
})
console = Console(theme=custom_theme)
# this console for saving to file
consoleSave = Console(record=True)

VERSION="v3.1.0"
API_URL = "https://api.github.com/repos/PakCyberbot/FBI-MostWanted/releases/latest"

class Fbi:
    def __init__(self,args):
        if args.wanted:
            if args.records:
                self.response = fbi.wanted(page_size=args.records, page=1, sort_order="asc")
            else:
                self.response = fbi.wanted(page_size=10, page=1, sort_order="asc")

        elif args.wanted_person:
        	self.response = fbi.wanted_person(person_id=args.wanted_person)
        
        	
        self.attrs = ['uid','ncic','sex','eyes_raw','hair_raw','weight','height_min','height_max','build','race_raw','nationality','complexion',
                             'scars_and_marks','languages','age_range','place_of_birth','dates_of_birth_used','aliases','legat_names','occupations','locations',
                             'possible_countries','possible_states','coordinates','status','person_classification','subjects','details','description',
                             'suspects','caution','warning_message','reward_text','field_offices','remarks','publication','modified']
                             
        self.attr_dict = {'uid': 'ID#',
                                    'ncic': 'NCIC',
                                    'sex': 'Sex',
                                    'eyes_raw': 'Eyes',
                                    'hair_raw': 'Hair',
                                    'weight': 'Weight',
                                    'height_min': 'Height (minimum)',
                                    'height_max': 'Height (maximum)',
                                    'build': 'Build',
                                    'race_raw': 'Race',
                                    'nationality': 'Nationality',
                                    'complexion': 'Complexion',
                                    'scars_and_marks': 'Scars & Marks',
                                    'languages': 'Language(s)',
                                    'age_range': 'Age range',
                                    'place_of_birth': 'Place of birth',
                                    'dates_of_birth_used': 'Date(s) of Birth Used',
                                    'aliases': 'Alias(es)',
                                    'legat_names': 'Legal name(s)',
                                    'occupations': 'Occupation(s)',
                                    'locations': 'Location(s)',
                                    'possible_countries': 'Possible countries',
                                    'possible_states': 'Possible state(s)',
                                    'coordinates': 'Co-ordinates',
                                    'status': 'Status',
                                    'person_classification': 'Classification',
                                    'subjects': 'Subject(s)',
                                    'details': 'Details',
                                    'description': 'Description',
                                    'suspects': 'Suspect(s)',
                                    'caution': 'Caution',
                                    'warning_message': 'Warning!',
                                    'reward_text': 'Reward',
                                    'field_offices': 'Field office(s)',
                                    'remarks': 'Remarks',
                                    'publication': 'Published on',
                                    'modified': 'Modified on'}
        # Author dictionary
        self.author_dict = {'Alias': 'rly0nheart',
                                     'Country': 'Zambia, Africa [🇿🇲]',
                                     'Github': 'https://github.com/rly0nheart',
                                     'Twitter': 'https://twitter.com/rly0nheart',
                                     'Facebook': 'https://fb.me/rly0nheart',
                                     'About.me': 'https://about.me/rly0nheart'}
        self.contibuter = { 'Alias': 'pakcyberbot',
                            'Github': 'https://github.com/pakcyberbot',
                            'Twitter': 'https://twitter.com/pakcyberbot',}

    # Main conditions    	                         
    def on_connection(self):
        console.print(f'VERSION: [bold]{VERSION}[bold]',style="info" )
        if args.wanted:
            self.wanted()
        elif args.wanted_person:
            self.wanted_person()
        elif args.licence:
        	print(self.licence_license())
        elif args.author:
        	self.author()
        elif args.update:
            self.check_for_update()
            exit()
        else:
            console.print(f'use [info]-h/--help[/info] to show help message.')
            console.print(f'Don\'t forget to follow me on: https://github.com/PakCyberbot')
            exit()

    # Reusable code to show the records/entries in a table format
    def table_view(self, property_dict, item, Count=0):
        if Count==0:
            table = Table(title=f"[bold]Record[/bold]")
        else:
            table = Table(title=f"[bold]Record# {Count}[/bold]")
        table.add_column("Name", style="blue", no_wrap=True)
        table.add_column(f"{item['title']}")
        for attr in self.attrs:
            # Different colors on different properties
            if property_dict[attr] =='Reward' and item[attr] != None:
                table.add_row(f"{property_dict[attr]}",f"[green]{item[attr]}[/green]")                
            elif property_dict[attr] =='Warning!' and item[attr] != None:
                table.add_row(f"[red]{property_dict[attr]}[/red]",f"[red]{item[attr]}[/red]")
            elif property_dict[attr] == 'Sex':
                if item[attr] == "Female":
                    table.add_row(f"{property_dict[attr]}",f"[plum1]{item[attr]}[/plum1]")
                elif item[attr] == "Male":
                    table.add_row(f"{property_dict[attr]}",f"[bright_cyan]{item[attr]}[/bright_cyan]")
            else:    
                table.add_row(f"{property_dict[attr]}",f"{item[attr]}")
            
                    
        #printing file_name for finding image or pdf
        file_name = re.sub(r"http.+/([^/]+)/.+.pdf",r'\1',item['files'][0]['url'])
        table.add_row(f"[red]FileName[/red]",f"[green]{file_name}[/green]")
        return table

    # Getting list and information of top wanted persons        
    def wanted(self):
        if not args.silent:
            count=0
            
            for item in self.response:
                # reward filter
                if args.reward:
                    if not self.reward(item):
                        continue
                count += 1 
                consoleSave.print(self.table_view(self.attr_dict,item,Count=count))
                # records seperator
                consoleSave.print(f'\n\n{"*"*100}\n', justify="center")
        
        
        # Storing images seperately
        if args.images:

        # Support for slow download to mimic human traffic, reducing the risk of being banned or flagged
            if args.slow:
                for item in self.response:
                    print(self.images(item))
                    time.sleep(random.randint(20, 70))
                    
            else:
                # Multithreading implementation for downloading files   
                with ThreadPoolExecutor() as executor:
                    img_results = executor.map(self.images, self.response)
                    for i in img_results:
                        print(i)

        # Dumping output to a file; invoked with --dump
        if args.dump:
            self.dump()
        elif args.download:
            current_directory = os.getcwd()
            final_directory = os.path.join(current_directory, "wanted_list")
            if not os.path.exists(final_directory):
                os.makedirs(final_directory)

            # Support for slow download to mimic human traffic, reducing the risk of being banned or flagged
            if args.slow:
                for item in self.response:
                    print(self.download(item,dir=final_directory))
                    time.sleep(random.randint(20, 70))
            else:
                # Multithreading implementation for downloading files   
                with ThreadPoolExecutor() as executor:
                    item_results = executor.map(self.download, self.response, (final_directory for i in range(0,len(self.response))))
                    for i in item_results:
                        print(i)

            exit()

            

    # Getting information of a wanted person, given their uid/ID            
    def wanted_person(self):
        # reward filter
        if args.reward:
            if not self.reward(response):
                print(f"[X] No reward Here")
                return None
        
        if not args.silent:
            consoleSave.print(self.table_view(self.attr_dict,self.response))

        # storing images seperately
        if args.images:
            print(self.images(self.response))
        # Dumping output to a file; invoked with --dump
        # Or downloading casefile; invoked with --download
        if args.dump:
            self.dump()
        elif args.download:
            print(self.download(self.response))

    # Dump output to a specified file      
    # supports downloading data in text, HTML and PDF
    def dump(self):
        if 'pdf' in args.dump.lower():
            if args.wanted_person:
                print(self.download(self.response))
            else:
                current_directory = os.getcwd()
                final_directory = os.path.join(current_directory, os.path.splitext(args.dump)[0])
                if not os.path.exists(final_directory):
                    os.makedirs(final_directory)
                for item in self.response:
                    print(self.download(item,dir=final_directory))
                exit()
        elif 'html' in args.dump.lower():
            if args.wanted_person:
                with open(args.dump, 'w', encoding='utf-8') as file:
                    file.write(consoleSave.export_html())
                    file.close()
                                
            else:
                with open(args.dump, 'a', encoding='utf-8') as file:
                    for item in self.response:
                        file.write(consoleSave.export_html())
                    file.close()
                    exit()
        else:
            if args.wanted_person:
                with open(args.dump, 'w', encoding='utf-8') as file:
                    
                    file.write(consoleSave.export_text())
                    file.close()
                                
            else:
                with open(args.dump, 'a', encoding='utf-8') as file:
                    for item in self.response:
                        file.write(consoleSave.export_text())
                    file.close()
                    exit()

        if args.verbose:
            print(f'\n[✓] Output dumped to {args.dump}')
            exit()
        
    # Download casefile of a wanted person                              
    def download(self, response, dir='./'):
        # reward filter
        if args.reward:
            if not self.reward(response):
                return f"[X] No reward Here"
        uri = requests.get(response['files'][0]['url'], stream=True)
        # name extraction from URL to avoid file naming errors
        file_name = re.sub(r"http.+/([^/]+)/.+.pdf",r'\1',response['files'][0]['url'])

        with open(dir+'/'+file_name+'.pdf', 'wb') as file:
            # Getting at least 1MB chunk size (if possible) for the file per iteration
            # And saving it to the opened file
            for chunk in tqdm(uri.iter_content(chunk_size=1024),desc=f"[~] Downloading {file_name}.pdf"):
                if chunk:
                    file.write(chunk)
            
            return f"[✓] File saved to {file_name}.pdf"
    
    # Download images for each person in a seperate folder
    def images(self, response):
        # reward filter
        if args.reward:
            if not self.reward(response):
                return f"[X] No reward Here"
        # creating directory
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, "wanted_images")
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)
        
        # extracting name from pdf download file because there aren't any pattern in image url
        file_name = re.sub(r"http.+/([^/]+)/.+.pdf",r'\1',response['files'][0]['url'])
        for count, img in enumerate(response['images']):
            uri = requests.get(img['original'], stream=True)
            
            if 'png' in img['original']:
                file_type = 'png'
            elif 'jpg' in img['original']:
                file_type = 'jpg'
            else:
                file_type = 'jpeg'

            # fetching image caption
            caption = img['caption'] if img['caption'] != None else 'None'
            with open(final_directory+'/'+file_name+"-"+str(count)+'___Caption '+caption+'.'+file_type, 'wb') as file:
                 # Getting at least 1MB chunk size (if possible) for the file per iteration
                # And saving it to the opened file
                for chunk in tqdm(uri.iter_content(chunk_size=1024),desc=f"[~] Downloading {file_name}.{file_type}"):
                    if chunk:
                        file.write(chunk)
            
            # Also gives some time to download images of the single record 
            if args.slow:
                time.sleep(random.randint(5, 15))
                

                
        return f"[✓] Images saved with the name {file_name}-<number>__<caption>"

    def reward(self, item):
        if item['reward_text'] == None:
            return False
        else:
            return True
    # Checks for updates using git api and then pull the latest version
    def check_for_update(self):
        
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            latest_version = response.json()["tag_name"]
            if latest_version != VERSION:

                print(f"[i] An update is available: {latest_version}")

                # BUG FIXED : The update now works correctly even if the file location is different from the execution start point.
                program_path = os.path.abspath(os.path.join(__file__, "..", ".."))

                if not os.path.isdir(program_path):
                    os.mkdir(program_path)
                    Repo.clone_from(appRepo, program_path)
                else:
                    repo = Repo(program_path)
                    subprocess.run(['git', 'reset', '--hard', 'HEAD'], cwd=program_path)
                    repo.remotes.origin.pull()
                console.print(f"[green]Updated Successfully![/green]")
                exit()
            else:
                print(f"[i] You are already using the latest version.")

        except requests.exceptions.RequestException as e:
            print(f"[X] Failed to check for updates: {str(e)}")

    
    # Open and read the LICENSE file     
    def licence_license(self):
        with open('./LICENSE','r') as file:
            content = file.read()
            file.close()
            return content
            
    # Author info        
    def author(self):
        print(f'Richard Mwewa (Ritchie)')
        for key,value in self.author_dict.items():
            print(f'├─ {key}: {value}') 

        print(f'\nPakCyberbot (Contributer)')
        for key,value in self.contibuter.items():
            print(f'├─ {key}: {value}')


start_time = datetime.now()
# Parsing command line arguments                                                                        
parser = argparse.ArgumentParser(description=f'FBI Wanted Persons Program CLI',epilog=f'Gets lists and dossiers of top wanted persons and unidentified victims from the FBI Wanted Persons Program. Developed by Richard Mwewa & Improved by PakCyberbot',formatter_class=RichHelpFormatter)
parser.add_argument('--dump','-d',help='dump output to a specified file, behaves differently for pdf & html',metavar='<path/to/file>')
parser.add_argument('--wanted','-w',help='return a list of the top wanted persons\' dossiers',action='store_true')
parser.add_argument('--records','-e',help='number of records to fetch with --wanted, DEFAULT = 10 records',dest='records',metavar='<number>')
parser.add_argument('--wanted-person','-p',help='return a dossier of a single wanted person; provide person\'s ID#',dest='wanted_person',metavar='<ID#>')
parser.add_argument('--images','-i',help='download images seperately in a folder. FileName Format: name+number+caption',action='store_true')
parser.add_argument('--download','-g',help='download persons\' casefile (beta)',action='store_true')
parser.add_argument('--slow', help='Downloads records slowly and mimics human traffic.',action='store_true')
parser.add_argument('--reward','-r',help='Filter out records that contain a reward',action='store_true')
parser.add_argument('--silent','-s',help='Disable Output',action='store_true')
parser.add_argument('--verbose','-v',help='enable verbosity',action='store_true')
parser.add_argument('--update','-u',help='Update to the latest version',action='store_true')
parser.add_argument('--version',version=f'{VERSION}',action='version')
parser.add_argument('--author','-a',help='show author\'s information and exit',action='store_true')
parser.add_argument('--licence','--license',help='show program\'s licen[cs]e and exit',action='store_true')

args = parser.parse_args()

# if --verbose is passed, logging will run in debug mode
if args.verbose:
    logging.basicConfig(format=f"[~] %(message)s",level=logging.DEBUG)
