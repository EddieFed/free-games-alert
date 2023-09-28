# Eddie's "Game Ping"
"Game Ping", (Otherwise known as free-game-alerts) is a web scraper that directly sources info from [Indie game bundles](https://www.indiegamebundles.com/category/free/). Ideally, this will be scraped directly from steam, epic, amazon prime, and more in the future. But for now, this is sufficient.

## Set up
If you want to run a server for this locally, feel free, but honestly just sign up on [my server](https://gameping.eddiefed.me).

### Setup:
Initial setup is actualy pretty complicated depending on what system you're on. Since xvfb is only supported on unix based systems here are the setup instructions for Ubuntu + WSL2

install vxfb:
```
apt install vxfb
```

Install postgresql and setup the db schema provided
```
https://www.postgresql.org/download/linux/ubuntu/
```

This project uses miniconda to create it's virtual python enviroment. The following is the install script from [miniconda](https://docs.conda.io/projects/miniconda/en/latest/)
```
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh

~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh
```

With miniconda installed, we can create the virtual env for the project. Use the following install the dependencies. This will create a conda enviroment named "free-games-alert"
```
conda env create -f environment.yml
activate free-games-alert
```

Now that the conda enviroment is set up, we also need to install chromium so that selenium can drive it's window. This is necessary to bypass anti-bot measures that cloudflare CDN provides to sites. 

This can be done with the [selenium-manager](https://www.selenium.dev/blog/2022/introducing-selenium-manager/) CLI tool (ensure the conda env is active)
```
selenium-manager --browser chrome
```

Now that chrome is installed and linked. We have everything you need!

### Unless you're on WSL! Gotcha!

WSL is more complicated, since it doesnt fully support xvfb, we need to do some wizardry to fix that. 

Add the following to your `~/.bashrc` file
```
# set DISPLAY variable to the IP automatically assigned to WSL2
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2; exit;}'):0.0
export PYVIRTUALDISPLAY_DISPLAYFD=0
```

This will allow the pyvirtualdisplay to still hook into the display if you're on WSL, I have no idea how this works but I found the solution [here](https://shouv.medium.com/how-to-run-cypress-on-wsl2-989b83795fb6)!

## Now you're ready to go!

### To host the website:
First, to start running things, we need an nginx server running, or something similar, it's too complicated for this readme, see instructions [here](https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-ubuntu-20-04)

Once that's all setup, you should be able to simply run
```
gunicorn --workers 2 wsgi:app --daemon
```

To kill the website after it's running as a background process
```
pkill gunicorn
```

If you need to access the site settings for nginx, it should be located at the following, or something similar
```
/etc/nginx/sites-enabled/gameping
```

To access the live database:
```
sudo -u postgres psql gameping
```

### As for the actual alerts, it's quite simple:

I recommend setting a chron job to just run the script provided, this will send alerts to all users who signed up for alerts

```
./run_scripts.sh
```

## To Do
- [X] Bypass cloudflare CDN protection
- [ ] CLI interface for databaseless application (for single person use through config)
- [ ] Seperate db structure from main application, website, db, and scripts should all be seperate
- [ ] Remove scrape from indiegamebundles, instead scrape directly from first party sources
- [ ] Offer option to choose alerts (limit alerts to chosen platform, steam, epic, etc.)
- [ ] Seperate website and cli completely so that cli is a compiled tool that is run off the flask website