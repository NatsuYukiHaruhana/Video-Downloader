<h1 align="center">🖥️Video Download Application in Python🖥️</h1>

<h2 align="center">💡Project Description💡</h2>


Welcome! I present to you a simple video download program. All you need is the video's URL and you're good to go!
If you're like me and want to provide a safe, ad-free video downloading experience for your close ones, then this project is just the right tool for you! Below you have the current and planned features, as well as instructions on how to use the program.


###

<br clear="both">

---

<h2 align="center">✨Current Features✨</h2>
<ul>
  <li>Download any YouTube video (video or short)</li>
</ul>

###

<br clear="both">

---

<h2 align="center">✍️Currently Working On✍️</h2>
<ul>
  <li>YouTube videos: Select preferred resolution</li>
  <li>YouTube videos: Select preferred format (audio or video)</li>
  <li>YouTube videos: Display video details</li>
</ul>

###

<br clear="both">

---

<h2 align="center">🗒️Planned Features🗒️</h2>
<ul>
  <li>More details, like progress bar and success/error output.</li>
  <li>Download Facebook videos</li>
  <li>Download any video from a website</li>
  <li>Big maybe, but maybe make a Chrome Extension variant?</li>
</ul>

###

<br clear="both">

---

<h2 align="center">🐞Known Bugs🐞</h2>
<ul>
  <li>For some reason, you can't right-click -> paste the video link. I'll see why this is and hopefully fix it. For now, just use CTRL+V.</li>
</ul>

###

<br clear="both">

---

<h2 align="center">✔️How To Use✔️</h2>
<ol>
  <li> Download* the program from the "Releases" tab (or build it yourself).</li>
  <li> Insert a YouTube link in the text box (only CTRL+V works for now, I'll look into why later).</li>
  <li> Select your download location (this is saved when closing the program). The default is the current working directory of the program.</li>
  <li> If the link is valid, then the Download button will light up. Press it, and your vidoe will be downloaded in the highest resolution available! (Progress bar and output will be added later)</li>
</ol>

*NOTE: The executable might be detected as a virus by some antivirus programs (**[here's a link to the VirusTotal scan](https://www.virustotal.com/gui/file/9530a18420df678ed7eabe0ce78e35228d3bbee55349d17dd9c8f1ade5788988/detection)**).
This is due to how bundlers like pyinstaller generate .exe files from Python code. There is sadly no workaround for this and I'll have to personally ask these companies to whitelist the program, but I'll only do this after I at least add 
Facebook video downloads in the mix as well. In the meantime, if you know your way around building Python code, I suggest you'd rather do that. If you want to use pyinstaller, first do a
~~~
pip install pyinstaller
~~~
then in the directory with the source files
~~~
pyinstaller -F --hide-console hide-early -n NAME_OF_EXECUTABLE main.py
~~~
This will create a dist folder in the folder you ran the command in. In it you'll find the .exe file with the name you gave it.

###
