# Spotipare

Find songs in common between two Spotify users

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.


### Installing

Getting your development enviroment up and running

Clone this repo

```sh
$ cd ~
$ git clone https://github.com/beachfires/Spotipare.git
```

Create virtual Python enviroment and activate it

```sh
$ python3 -m venv venv && source venv/bin/activate
```

Install Spotipare dependencies

```sh
$ python -m pip install -r requirements.txt
```

Get your credentials from Spotify by [creating a new app](https://developer.spotify.com/my-applications).

Add the client_id and client_secret to a .env file. A sample has been provided named *sample.env*. Just replace the placeholders save the file as `.env`.

Start the Spotipare server locally

```sh
$ python flask_app.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

## Deployment

Coming soon...

## Built With

* [spotipy](https://github.com/plamere/spotipy) - Spoify Python client
* [Flask](https://github.com/pallets/flask) - Web framework used

## Contributing

Please read [CONTRIBUTING.md](https://github.com/beachfires/Spotipare/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Authors

See list of [contributors](https://github.com/beachfires/Spotipare/graphs/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
