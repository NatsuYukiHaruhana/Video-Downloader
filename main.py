import PySimpleGUI as gui
import colors as COLORS
import config
import subprocess

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

if __name__ == "__main__":
    # Layout components
    # components for inputting the url
    url_input_layout = [
        [
            gui.Text(text = "Input a valid YouTube URL link: ", # displayed text
                        background_color = COLORS.BLACK # make the background color black
                        ),
            gui.In(key = "-URL_LINK-", # id for later use
                    enable_events = True, # let it trigger an event
                    expand_x = True, # expand the text box in case it's needed
                    background_color = COLORS.DARK_PURPLE, # make the input box's background dark purple
                    text_color = COLORS.WHITE # make the text's color white
                    )
        ]
    ]
    
    # components for actually downloading the video
    download_layout = [
        [
            gui.Button(button_text = "Download", # displayed text over button
                        enable_events = True, # let it trigger an event
                        key = "-URL_DOWNLOAD-", # id for later use
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

    # Window's layout
    layout = [
        CenterLayout(url_input_layout),
        CenterLayout(browse_folder_layout),
        CenterLayout(download_layout)
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
            case "-URL_LINK-":
                # Validate video at specified link
                link = values["-URL_LINK-"]
                
                if link == "":
                    # just skip if it's empty
                    continue

                # if the link is valid, enable the button
                main_window["-URL_DOWNLOAD-"].update(disabled = not yt_downloader.ValidateLink(link = link))
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
                
            case "-URL_DOWNLOAD-":
                output_path = values["-BROWSE-DOWNLOAD-"]
                yt_downloader.Download(output_path = output_path)
    
    # Close window, buh-baaai!
    main_window.close()
