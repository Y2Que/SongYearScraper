
from pathlib import WindowsPath
from mutagen.id3 import ID3

#songPath = WindowsPath('E:/Music/Jaimito_Library/2000s/2000s_Slow/2000s_Slow_DONE')
songPath = WindowsPath('D:\Git\SongYearScraper\songs')

def print_file_year(strInputPath):
    for file in strInputPath.iterdir():  # loop thru files in directory
        if file.is_dir():                # do not act on folders
            print_file_year(file)        # recusive call for folders
        else:
            if file.name.endswith('.mp3'):                             
                song = ID3(file)
                print()
                print()
                #print(song.getall)
                print(f"File Name:            {file.name}")
                print(f"Title:                {song.get('TIT2')}")
                print(f"Contributing Artists: {song.get('TPE1')}")
                print(f"Album Artist:         {song.get('TPE2')}")
                print(f"Genre:                {song.get('TCON')}")
                print(f"Beats per min:        {song.get('TBPM')}")
                print(f"Year:                 {song.get('TDRC')}")
                print(f"Image:                {song.get('APIC')}")

print_file_year(songPath)