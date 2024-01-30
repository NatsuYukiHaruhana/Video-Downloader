from pytube import YouTube
from pytube.exceptions import RegexMatchError


class YouTubeDownloader:
    # this class saves a YouTube object containing the current link's video
    def __init__(self):
        self.yt_obj = None
    
    def ValidateLink(self, link : str) -> bool:
        # this function checks if the given link is valid
        # Params:
        # link: str - YouTube link to validate
        # return: bool - True if link is valid, False otherwise

        try:
            self.yt_obj = YouTube(link)
            # past this means the link is valid, but we need to check if the video is also valid
            try:
                self.yt_obj.check_availability()
                # past this check means the video is available
                return True
            except Exception as err:
                print(f"ERROR: Video unavailable: {type(err).__name__} - {err}")
                return False
        except RegexMatchError:
            # link is not accepted by pytube's internal regex check
            print(f"ERROR: RegexMatchError, link is invalid!")
            return False


    def GetVideoTitle(self) -> str:
        # function that returns the video title. This function can't
        # be called through normal means unless the video is known to already be valid,
        # so no extra checks are performed
        # Params: none
        # return: str - the title of the video
        return self.yt_obj.title


    def Download(self, output_path = "") -> None:
        # this function downloads the given video
        # Params: 
        # output_path: str - the path to which to download the video
        # return: None
        video_obj = self.yt_obj.streams.get_highest_resolution() # only filter for the highest resolution for now
        
        try:
            video_obj.download(output_path=output_path)
        except Exception as err:
            print(f"ERROR: Exception occured: {type(err).__name__} - {err}")
        
        print("Download has been completed successfully!")
