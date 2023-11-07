from pytube import YouTube


def Download(link : str, output_path = "") -> None:
    ytObj = YouTube(link)
    ytObj = ytObj.streams.get_highest_resolution() # only filter for the highest resolution for now
    
    try:
        ytObj.download(output_path=output_path)
    except Exception as err:
        print(f"ERROR: Exception occured: {type(err).__name__} - {err}")
    
    print("Download has been completed successfully!")
