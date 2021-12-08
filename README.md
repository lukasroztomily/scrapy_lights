# scrapy_lights

Účelem skriptu je stahnout z webu https://www.lights.co.uk/innr-smart-outdoor-led-ground-spike-light-rgbw-3x.html obrázky, video a dokument. 

Skript je napsaný v programu python3.8. Využívá moduly **scrapy** a **selenium**. Proto je nutné si před spuštěním skriptu nainstalovat tyto moduly.
Závislosti jsou definované v sobouru **requirements.txt**, který se spouští ```pip install -r requirements.txt```

Skript se spouští příkazem ```scrapy crawl lights_co_uk```. 

Knihovna selenium byla zvolena proto, že web obsahuje skryté media odkazy, které se v html kodu objeví až po určité interakci s webem. Selenium tuto interakci zajištuje.
Selenium vyžaduje pro svuj běh **chromedriver**, který se nachází v projektu v **lights\lights\spiders\drivers**. Ve folderu se nachází drivers
pro systemové platformy Windows, Linux, MacOS. Program byl vyvíjen a testován na platformě Windows.
