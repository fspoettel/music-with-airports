# `music-with-airports`

> simultaneously listen to airport radio chatter and music via mpv

## Prerequisites

* `python^3.7`
* `mpv`
* `youtube-dl`
* `libmpv` (see: https://git.io/JJNbG if this is not present after `mpv` installation)

## Install

1. Clone this repository
2. Install dependencies from `pyproject.toml`
3. Make sure `run.py` is executable

## Use

```sh
# basic usage
./run.py -a [live_atc_feed_code] [url]
```
`url` can be anything that `mpv` can play (e.g. YouTube videos, YouTube playlists, Soundcloud, local files). `-a` is optional and expects the id of a [LiveATC.net](liveatc.net/) feed. See below for instructions on how to find these. The player defaults to the Tokyo Airport Arrival/Departure feed.

```sh
# example: Dublin Airport + "Eno/Budd - Music for Airports 2"
./run.py -a eidw3 https://www.youtube.com/playlist?list=PLzWmNYF6L9EFZ27Gu-0cky-sAFjSEWqN3
```

```sh
# example: JFK Airport + "William Basinski - Disintegration Loops"
./run.py -a kjfk_twr https://www.youtube.com/watch?v=mjnAE5go9dI
```

```sh
# help
./run.py -h
```

## Finding airport codes

To print a list of popular airport feeds and their codes, go to the [LiveATC.net top feeds page](https://www.liveatc.net/topfeeds.php) and run the following script in your browser console.

```js
function getAirportCodes() {
  const rows = Array.from(document.querySelectorAll('.topTable tbody > tr:not(:first-child'))

  const results = []

  for (let i = 0; i < rows.length; i += 1) {
    const row = rows[i]
    const fields = row.querySelectorAll('td')

    const city = fields[3].innerText
    const country = fields[5].innerText
    const description = fields[2].innerText

    const code = /^.*\('(.*?)'/.exec(fields[6].querySelector('a').getAttribute('onclick'))[1]

    console.log(code, `${city}, ${country}: ${description}`)
  }
}

getAirportCodes()
```
