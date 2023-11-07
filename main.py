import PySimpleGUI as gui
import colors as COLORS

from YouTube.yt_download import Download



if __name__ == "__main__":
    # Window's layout
    layout = [
        [ # first, an input box for the link
            gui.Text(text = "Input a valid YouTube URL link: ", # displayed text
                        background_color = COLORS.BLACK # make the background color black
                        ),
            gui.In(key = "-URL_LINK-", # id for later use
                    expand_x = True, # expand the text box in case it's needed
                    background_color = COLORS.DARK_PURPLE, # make the input box's background dark purple
                    text_color = COLORS.WHITE # make the text's color white
                    ),
            gui.Button(button_text = "Download", # displayed text over button
                        enable_events = True, # let it trigger an event
                        key = "-URL-", # id for later use
                        button_color = COLORS.BLACK, # make the button's color black
                        mouseover_colors = COLORS.DARK_PURPLE # make the button's color dark purple once highlighted
                        )
        ]
    ]
    
    # Create main window
    main_window = gui.Window(title = "Python Video Downloader", # window title
                                layout = layout, # layout created above
                                background_color = COLORS.BLACK, # make the background color black
                                #margins = (512, 256), # size in pixels
                                resizable = True) # make it resizable

    # Main window loop
    while True:
        event, values = main_window.read()

        match(event):
            case gui.WIN_CLOSED:
                # Close main window loop
                break
            case "-URL-":
                # Download video at specified link
                link = values["-URL_LINK-"]
                Download(link = link)
    
    # Close window, buh-baaai!
    main_window.close()
