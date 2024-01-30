import configparser
from pathlib import Path
import subprocess

INI_FILENAME = "video_downloader.ini"

def INIFileCreate(download_path : str = "") -> None:
    ''' Create and populate the program's .ini file'''
    
    with open(INI_FILENAME, 'w') as ini_file:
        # write useful readable info at the top of the ini file
        ini_file.write('# This INI file stores the most recent download path used\n')
        ini_file.write('# If no download path was ever selected, the directory of the program is used instead\n')
        ini_file.write('# Please do NOT edit this unless you know what you\'re doing!\n')
        ini_file.write("# The program will still run as expected, but there's no reason not to change the value from the program.\n\n")
        ini_file.write("[PATHS]\n")
        # save the download path
        
        if download_path == "":
            download_path = Path.cwd()
            
        ini_file.write(f'DOWNLOAD_PATH={download_path}\n')
        
        ini_file.close()
        
        # hide .ini file
        subprocess.run(["attrib", "+H", INI_FILENAME], check=True)


def INIFileWrite(download_path : str) -> None:
    ''' Write to an existing .ini file '''
    
    if not Path(INI_FILENAME).exists():
        INIFileCreate(download_path = download_path)
        return
    
    with open(INI_FILENAME, 'r') as ini_file:
        lines = ini_file.readlines()
        
    for i in range(len(lines)):
        if lines[i].startswith("DOWNLOAD_PATH="):
            lines[i] = f"DOWNLOAD_PATH={download_path}"
            break
    
    # unhide .ini file (this is so we don't require admin priviliges. Kind of hacky, but eh, it works.)
    subprocess.run(["attrib", "-H", INI_FILENAME], check=True)

    with open(INI_FILENAME, "w") as ini_file:
        ini_file.writelines(lines)
    
    # hide .ini file
    subprocess.run(["attrib", "+H", INI_FILENAME], check=True)


def INIFileRead() -> str:
    ''' Read the saved download path from the INI_FILENAME.ini file'''
    if not Path(INI_FILENAME).exists():
        INIFileCreate()
    
    config = configparser.ConfigParser()
    config.read(INI_FILENAME)
    
    return config['PATHS']['DOWNLOAD_PATH']
