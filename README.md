# FilmAffinity backup to CSV

[![tests](https://github.com/IgnacioHeredia/filmaffinity-backup/actions/workflows/main.yml/badge.svg)](https://github.com/IgnacioHeredia/filmaffinity-backup/actions/workflows/main.yml)

These are some _minimal_ scripts to backup your [FilmAffinity](https://www.filmaffinity.com/) data to a CSV.

Information saved:
* **list movies**: For each movie in the list, it saves:
    - `movie title`
    - `movie year`
    - `movie country`
    - `movie directors`
    - `user score`
    - `Filmaffinity score`
    - `Filmaffinity movie id`
* **watched movies**: same as list movies, plus the `movie genre`

To perform the backup, install the required packages and run `main.py` with your `user_id` [^1]:

[^1]: To find your `user_id`, go to `Mis votaciones` and copy the ID from the url `https://www.filmaffinity.com/es/userratings.php?user_id={........}`.

```bash
pip install -r requirements.txt
python main.py 861134
```
You data will be saved to the [./data](./data) folder.

![alt text](console.png)

The script intentionally waits 5s between each parsing request to avoid getting the IP blocked by the FilmAffinity server.

Some related repos include:
* [mx-psi/fa-scraper](https://github.com/mx-psi/fa-scraper)
* [xsga/filmaffinity-api](https://github.com/xsga/filmaffinity-api)
* [gism/filmaffinity2CSV](https://github.com/gism/filmaffinity2CSV)
