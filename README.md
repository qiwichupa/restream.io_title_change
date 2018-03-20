# restream.io_title_change
If you need to change title (dash) on restream.io automatically, this script will help you.

You must create 'chrome_home_dir' and run this script with --manual key, 
it will opened chrome without virtual display and let you authorize 
on restream.io. It is neccessary because of captcha, and you will be forced
to repeat this procedure from time to time =(. But after that you can run

$ scriptname.py "new title"

and "new title" will be applied to your stream.

REQUIREMENTS:

modules: pyvirtualdisplay, selenium

soft: chromium-chromedriver, chromium-browser, xvfb
