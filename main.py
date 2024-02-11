import PySimpleGUI as gui
import colors as COLORS
import config
import subprocess
from tkinter import Tk

from youtube import YouTubeDownloader

def CenterLayout(layout : list) -> list:
    """ Generate a centered layout """
    
    return [
        [gui.VPush(background_color=COLORS.BLACK)],
        [gui.Push(background_color=COLORS.BLACK), 
            gui.Column(layout, element_justification = 'c', background_color=COLORS.BLACK), 
            gui.Push(background_color=COLORS.BLACK)],
        [gui.VPush(background_color=COLORS.BLACK)]
    ]

def CopyToClipboard(text_to_copy : str) -> None:
    """ Copy text_to_copy to clipboard """
    
    clipboard = Tk()
    clipboard.withdraw()
    clipboard.clipboard_clear()
    clipboard.clipboard_append(text_to_copy)
    clipboard.update() # now it stays on the clipboard after the window is closed
    clipboard.destroy()
    
def GetFromClipboard() -> str:
    """ Get string from clipboard """
    
    clipboard = Tk()
    clipboard.withdraw()
    try:
        return_string = clipboard.clipboard_get()
    except Exception: # Usually occurs if given a picture instead of text
        return_string = ""
    finally:
        clipboard.destroy()
    
    return return_string


def UpdateVideoDetails(main_window : gui.Window, yt_obj : YouTubeDownloader) -> None:
    """ Updates video details upon link validation """
    
    main_window["-VIDEO-TITLE-"].update(value = f"Video Title: {yt_obj.GetVideoTitle()}")
    
    video_res = yt_obj.GetVideoResolutions()
    main_window["-RESOLUTIONS-"].update(values = video_res, 
                                        value = video_res[0] if len(video_res) > 0 else "N/A")
    
    main_window["-IMAGE-VALUE-"].update(source = yt_obj.GetVideoThumbnail())
    

if __name__ == "__main__":
    # Layout components
    # components for inputting the url
    url_input_layout = [
        [
            gui.Text(text = "Input a valid YouTube URL link: ", # displayed text
                        background_color = COLORS.BLACK # make the background color black
                        ),
            gui.In(key = "-URL-LINK-", # id for later use
                    enable_events = True, # let it trigger an event
                    expand_x = True, # expand the text box in case it's needed
                    background_color = COLORS.DARK_PURPLE, # make the input box's background dark purple
                    text_color = COLORS.WHITE, # make the text's color white
                    right_click_menu = ['Input_URL', ['&Copy', 'C&ut', '&Paste', '&Delete All']]
                    )
        ]
    ]
    
    # components for actually downloading the video
    download_layout = [
        [
            gui.Button(button_text = "Download", # displayed text over button
                        enable_events = True, # let it trigger an event
                        key = "-URL-DOWNLOAD-", # id for later use
                        disabled = True, # only enable it once the link has been checked to be valid
                        button_color = COLORS.BLACK, # make the button's color black
                        mouseover_colors = COLORS.DARK_PURPLE # make the button's color dark purple once highlighted
                        ),
            gui.Button(button_text = "Open Download Folder", # displayed text over button
                        enable_events = True, # let it trigger an event
                        key = "-OPEN-DOWNLOAD-FOLDER-", # id for later use
                        button_color = COLORS.BLACK, # make the button's color black
                        mouseover_colors = COLORS.DARK_PURPLE # make the button's color dark purple once highlighted
                        )
        ]
    ]
    
    
    download_folder = config.INIFileRead()
    browse_folder_layout = [
        [
            gui.Text(text = f"Download Folder: {download_folder}", # displayed text
                        key = "-BROWSE-DOWNLOAD-TEXT-", # id for later use
                        background_color = COLORS.BLACK # make the background color black
                        ),
            gui.FolderBrowse(button_text = "Select Download Folder",
                                            key = "-BROWSE-DOWNLOAD-BUTTON-", # id for later use
                                            target = "-BROWSE-DOWNLOAD-", # workaround because this does not trigger an event on its own
                                            button_color = COLORS.BLACK
                        ),
            gui.Input(key = "-BROWSE-DOWNLOAD-", # id for later use
                        enable_events = True, # let it trigger an event
                        visible = False # it's only here for a workaround, so it shouldn't be visible
                        )
        ]
    ]

    video_details_column = gui.pin(
                                gui.Column(
                                    [
                                        [
                                            gui.Text(text = "Video Title: ", # displayed text
                                                    background_color = COLORS.BLACK, # make the background color black
                                                    key = "-VIDEO-TITLE-" # id for later use
                                                    )
                                        ],
                                        [
                                            gui.Text(text = "Video Resolutions: ", # displayed text
                                                    background_color = COLORS.BLACK, # make the background color black
                                                    key = "-VIDEO-RESOLUTIONS-" # id for later use
                                                    ),
                                            gui.Combo(background_color = COLORS.BLACK,
                                                    text_color = COLORS.WHITE,
                                                    values = [],
                                                    expand_x = True,
                                                    key = '-RESOLUTIONS-'
                                                    )
                                        ],
                                        [
                                            gui.Text(background_color = COLORS.BLACK, # make the background color black
                                                        text = "Video Thumbnail: ",
                                                        key = "-IMAGE-TEXT-"),
                                            gui.Image(background_color = COLORS.BLACK,
                                                        key = "-IMAGE-VALUE-")
                                        ]
                                    ],
                                    background_color = COLORS.BLACK
                                )
                            )

    # modify column details
    video_details_column.BackgroundColor = COLORS.BLACK
    video_details_column.Key = "-VIDEO-DETAILS-LAYOUT-"
    video_details_column._visible = False

    video_details_layout = [
        [
            video_details_column
        ]
    ]

    # Window's layout
    layout = [
        CenterLayout(url_input_layout),
        CenterLayout(browse_folder_layout),
        CenterLayout(download_layout),
        CenterLayout(video_details_layout)
    ]
    
    # Create main window
    main_window = gui.Window(title = "Python Video Downloader", # window title
                                layout = layout, # layout created above
                                background_color = COLORS.BLACK, # make the background color black
                                #margins = (512, 256), # size in pixels
                                resizable = True) # make it resizable

    # Create YoutubeDownloader object
    yt_downloader = YouTubeDownloader()
    # Main window loop
    while True:
        event, values = main_window.read()

        match(event):
            case gui.WIN_CLOSED:
                # Close main window loop
                break
            case "-URL-LINK-":
                # Validate video at specified link
                link = values["-URL-LINK-"]
                
                if link == "":
                    # just skip if it's empty
                    continue

                # if the link is valid, enable the button
                video_link_valid = yt_downloader.ValidateLink(link = link)
                
                main_window["-URL-DOWNLOAD-"].update(disabled = not video_link_valid)
                
                if video_link_valid:
                    UpdateVideoDetails(main_window, yt_downloader)
                    
                main_window["-VIDEO-DETAILS-LAYOUT-"].update(visible = video_link_valid)
            case "-BROWSE-DOWNLOAD-":    
                # Change download folder
                download_folder = values["-BROWSE-DOWNLOAD-BUTTON-"]
                
                download_folder = download_folder.replace("/", "\\") # Replace Windows path separators with Unix path separators
                
                # First change it in the INI file
                config.INIFileWrite(download_folder)
                
                # then in the current window
                main_window["-BROWSE-DOWNLOAD-TEXT-"].update(value = f"Download Folder: {download_folder}")
                
            case "-OPEN-DOWNLOAD-FOLDER-":
                # This only works in Windows, as far as I'm aware
                subprocess.Popen(f'explorer "{download_folder}"')
                
            case "-URL-DOWNLOAD-":
                output_path = values["-BROWSE-DOWNLOAD-"]
                yt_downloader.Download(output_path = output_path)
                
            case "Copy":
                CopyToClipboard(values["-URL-LINK-"])
            
            case "Cut":
                CopyToClipboard(values["-URL-LINK-"])
                main_window["-URL-LINK-"].update(value = "")
                
            case "Paste":
                main_window["-URL-LINK-"].update(value = GetFromClipboard())
                
            case "Delete All":
                main_window["-URL-LINK-"].update(value = "")
    
    # Close window, buh-baaai!
    main_window.close()
