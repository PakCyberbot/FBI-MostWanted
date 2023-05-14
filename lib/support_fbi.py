import fbi      # Credits @rly0nheart GitHub 
import argparse
import requests
import re
from tqdm import tqdm
import logging
from datetime import datetime
import os
from lib.colors import red,white,green,reset,blue


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
        if args.wanted:
            self.wanted()
        elif args.wanted_person:
            self.wanted_person()
        elif args.licence:
        	print(self.licence_license())
        elif args.author:
        	self.author()
        else:
            exit(f'{white}use{green} -h{white}/{green}--help{white} to show help message.{reset}')
    
    # Getting list and information of top wanted persons        
    def wanted(self):
        for item in self.response:
            # reward filter
            if args.reward:
                if not self.reward(item):
                    continue
            print(f"\n{white}{item['title']}{reset}")
            for attr in self.attrs:
                print(f'{white}├─ {self.attr_dict[attr]}: {green}{item[attr]}{reset}')
            #printing file_name for finding image or pdf
            file_name = re.sub(r"http.+/([^/]+)/.+.pdf",r'\1',item['files'][0]['url'])
            print(f'{blue}├─ FileName: {file_name}{reset}')
            # records seperator
            print(f'\n\n{"*"*100}\n')

        # Storing images seperately
        if args.images:
            for item in self.response:
                print(self.images(item))
        # Dumping output to a file; invoked with --dump
        if args.dump:
            self.dump()
        elif args.download:
            current_directory = os.getcwd()
            final_directory = os.path.join(current_directory, "wanted_list")
            if not os.path.exists(final_directory):
                os.makedirs(final_directory)
            for item in self.response:
                print(self.download(item,dir=final_directory))
            exit()

            

    # Getting information of a wanted person, given their uid/ID            
    def wanted_person(self):
        # reward filter
        if args.reward:
            if not self.reward(response):
                print(f"{white}[{green}X{white}] No reward Here{reset}")
                return None
        print(f"\n{white}{self.response['title']}{reset}")
        for attr in self.attrs:
            print(f'{white}├─ {self.attr_dict[attr]}: {green}{self.response[attr]}{reset}')
        #printing file_name for finding image or pdf
        file_name = re.sub(r"http.+/([^/]+)/.+.pdf",r'\1',self.response['files'][0]['url'])
        print(f'{blue}├─ FileName: {file_name}{reset}')
        
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
    # supports downloading data in text and PDF
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
        else:
            if args.wanted_person:
                with open(args.dump, 'w', encoding='utf-8') as file:
                    file.write(f"{self.response['title']}\n")
                    for attr in self.attrs:
                        file.write(f'├─ {self.attr_dict[attr]}: {self.response[attr]}\n')
                    #printing file_name for finding image or pdf
                    file_name = re.sub(r"http.+/([^/]+)/.+.pdf",r'\1',response['files'][0]['url'])
                    file.write(f'├─ FileName: {file_name}')
                    file.close()
                                
            else:
                with open(args.dump, 'a', encoding='utf-8') as file:
                    for item in self.response:
                         # reward filter
                        if args.reward:
                            if not self.reward(item):
                                continue
                        file.write(f"\n\n{item['title']}\n")
                        for attr in self.attrs:
                            file.write(f'├─ {self.attr_dict[attr]}: {item[attr]}\n')
                        file_name = re.sub(r"http.+/([^/]+)/.+.pdf",r'\1',item['files'][0]['url'])
                        file.write(f'├─ FileName: {file_name}')
                        # records seperator
                        file.write(f'\n\n{"*"*100}\n')
                    file.close()
                    exit()

        if args.verbose:
            print(f'\n{white}[{green}✓{white}] Output dumped to {args.dump}{reset}')
            exit()
        
    # Download casefile of a wanted person                              
    def download(self, response, dir='./'):
        # reward filter
        if args.reward:
            if not self.reward(response):
                return f"{white}[{green}X{white}] No reward Here{reset}"
        uri = requests.get(response['files'][0]['url'], stream=True)
        # name extraction from URL to avoid file naming errors
        file_name = re.sub(r"http.+/([^/]+)/.+.pdf",r'\1',response['files'][0]['url'])

        with open(dir+'/'+file_name+'.pdf', 'wb') as file:
            # Getting at least 1MB chunk size (if possible) for the file per iteration
            # And saving it to the opened file
            for chunk in tqdm(uri.iter_content(chunk_size=1024),desc=f"{white}[{green}~{white}] Downloading {file_name}.pdf{reset}"):
                if chunk:
                    file.write(chunk)
            
            return f"{white}[{green}✓{white}] File saved to {file_name}.pdf{reset}"
    
    # Download images for each person in a seperate folder
    def images(self, response):
        # reward filter
        if args.reward:
            if not self.reward(response):
                return f"{white}[{green}X{white}] No reward Here{reset}"
        # creating directory
        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, "wanted_images")
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)
        
        # extracting name from pdf download file because there aren't any pattern in image url
        file_name = re.sub(r"http.+/([^/]+)/.+.pdf",r'\1',response['files'][0]['url'])
        for count, img in enumerate(response['images']):
            print("testing images: ",count, img['original'])
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
                for chunk in tqdm(uri.iter_content(chunk_size=1024),desc=f"{white}[{green}~{white}] Downloading {file_name}.{file_type}{reset}"):
                    if chunk:
                        file.write(chunk)
                
        return f"{white}[{green}✓{white}] Images saved with the name {file_name}-<number>__<caption>{reset}"

    def reward(self, item):
        if item['reward_text'] == None:
            return False
        else:
            return True
    
    # Open and read the LICENSE file     
    def licence_license(self):
        with open('./LICENSE','r') as file:
            content = file.read()
            file.close()
            return content
            
    # Author info        
    def author(self):
        print(f'{white}Richard Mwewa (Ritchie){reset}')
        for key,value in self.author_dict.items():
            print(f'{white}├─ {key}: {green}{value}{reset}') 

        print(f'{white}\nPakCyberbot (Contributer){reset}')
        for key,value in self.contibuter.items():
            print(f'{white}├─ {key}: {green}{value}{reset}')


start_time = datetime.now()
# Parsing command line arguments                                                                        
parser = argparse.ArgumentParser(description=f'{white}FBI Wanted Persons Program CLI{reset}',epilog=f'{white}Gets lists and dossiers of top wanted persons and unidentified victims from the FBI Wanted Persons Program. Developed by {green}Richard Mwewa{white} | https://about.me/{green}rly0nheart{reset}')
parser.add_argument('--dump','-d',help='dump output to a specified file, behaves differently for pdf',metavar='<path/to/file>')
parser.add_argument('--wanted','-w',help='return a list of the top wanted persons\' dossiers',action='store_true')
parser.add_argument('--records','-e',help='number of records to fetch with --wanted, DEFAULT = 10 records',dest='records',metavar='<number>')
parser.add_argument('--wanted-person','-p',help='return a dossier of a single wanted person; provide person\'s ID#',dest='wanted_person',metavar='<ID#>')
parser.add_argument('--images','-i',help='download images seperately in a folder. FileName Format: name+number+caption',action='store_true')
parser.add_argument('--download','-g',help='download persons\' casefile (beta)',action='store_true')
parser.add_argument('--reward','-r',help='Filter out records that contain a reward',action='store_true')
parser.add_argument('--verbose','-v',help='enable verbosity',action='store_true')
parser.add_argument('--version',version='v1.2.0-caesar',action='version')
parser.add_argument('--author','-a',help='show author\'s information and exit',action='store_true')
parser.add_argument('--licence','--license',help='show program\'s licen[cs]e and exit',action='store_true')

args = parser.parse_args()

# if --verbose is passed, logging will run in debug mode
if args.verbose:
    logging.basicConfig(format=f"{white}[{green}~{white}] %(message)s{reset}",level=logging.DEBUG)