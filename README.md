# Silwadi Dental Center Website

## Run locally

Double-click:

`START-SILWADI.bat`

No Python or Node.js is required.

The launcher uses Windows PowerShell's built-in HTTP server functionality and opens:

`http://127.0.0.1:5500`

Keep the black terminal window open while previewing the site.

## GitHub repository

Configured repository:

`https://github.com/cuenext/silwadi-website.git`

If the folder has not been connected to GitHub yet, double-click:

`CONNECT-GITHUB.bat`

## Automatic updates

When this folder is connected to GitHub, `START-SILWADI.bat`:

1. Pulls the newest version at startup.
2. Starts the local site.
3. Checks GitHub every ~5 seconds while running.
4. Auto-pulls new commits when your local working tree is clean.

After an update lands, refresh the browser to see the newest version.

## If the server says port 5500 is busy

Close any older Silwadi server/terminal windows and run `START-SILWADI.bat` again.
