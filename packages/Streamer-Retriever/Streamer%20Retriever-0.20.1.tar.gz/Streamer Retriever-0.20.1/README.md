# Streamer Retriever

Stream Retriever allows you to search if a stream is online. It also allows you to
start playing the stream or even its vod.


## Usage

* `streamretriever -h` or `--help` to list all possible arguments
* `streamretriever -v` or `--version` to show installed streamretriever version
* `streamretriever -c` or `--check` show follows that are streaming
* `streamretriever -l` or `--link` links of follows that are streaming
* `streamretriever -p` or `--play` show online streams and choose one to play
* `streamretriever -d` or `--vod` choose vod to play
* `streamretriever -w` or `--web` use default webbrowser regardless of your
  configurations, use with `-p` or `-d`
* `streamretriever -m` or `--mobile` mobile twitch links of follows that are
  streaming, works also with `-p` and `-d`
* `streamretriever -t` or `--twitch-follows` print your follows from twitch


### Check if Your Follows are Online

Output names of streams that are online.
```
streamretriever -c
streamretriever --check
```


### Show and Start Playing

Use the option `-p` or `--play` to see who is online and choose if you want to
start playing a stream.

```
streamretriever -p
streamretriever --play
```

### Show Vods and Start Playing

The `-d` or `--vod` allows you to chooce a vod from your followed streamer and
start playing it.

```
streamretriever -d
streamretriever --vod
```


### Additional Options for Playing

You can use the additional `-m` or `--mobile` to use twitch mobile link. To
force use default webbrowser regardless of your configurations us `-w` or
`--web` options. Or you can use bot optional playing arguments.

```
streamretriever -pmw
streamretriever --play --web --mobile
```

The additional options also work with vod option.

```
streamretriever -dwm
streamretriever --web --vod --mobile
```

## Requirements

* Python 3.8 or newer
  * In Ubuntu `sudo apt install python3`
  * In Windows install [Python 3](https://www.python.org/)
    * You should consider selecting `Add Python to PATH` during install


## Install

1.  Install [Python 3](https://www.python.org/) from the [Requirements][1]
2.  Run `pip install streamretriever` to install from [PyPI][3]
3.  Run `streamretriever -v` to show installed streamretriever version number
4.  Create your streamer list [Configuration][2]


## Configuration

Add "streamer name" into your follows csv file. Separate each streamer with a
comma.

**Linux:** `~/.config/StreamRetriever/follows.csv`

**Windows:** `%USERPROFILE%\Documents\StreamRetriever\follows.csv`

The "streamer name" can be found at the end of a Twitch link:
`https://www.twitch.tv/<streamer_name>`

**follows.csv**
```
esamarathon,gamesdonequick,esl_csgo
```


### CLI Play

Add your player of choice to CLI configuration file.

**Linux:** `~/.config/StreamRetriever/cli_conf.json`

**Windows** `%USERPROFILE%\Documents\StreamRetriever\cli_conf.json`

**cli.json**
```
{"player": ["/usr/bin/firefox", "--private-window"]}
```



[1]: #requirements
[2]: #configuration
[3]: https://pypi.org/project/streamretriever
[4]: #usage
[5]: #cli-play
