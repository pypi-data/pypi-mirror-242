# postodon

[![PyPI](https://img.shields.io/pypi/v/postodon.svg)](https://pypi.org/project/postodon/)
[![Changelog](https://img.shields.io/github/v/release/msleigh/postodon?include_prereleases&label=changelog)](https://github.com/msleigh/postodon/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/msleigh/postodon/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

Randomly posts things to Mastadon from a pre-defined list, using the Mastodon API.

The list of posts is a JSON file:

    [
        {"content": "Text of the post", "id": 1, "status": "unposted"},
        ...,
    ]

The command `postodon` randomly selects an unposted post, posts it to Mastodon,
and marks it as posted in the list. If there are no unposted items, an already-
posted item is used instead.

---

## Requirements

Postodon requires Python 3.7+. It is tested on Linux and macOS.

## Installation

Postodon is published as a Python package and can be installed with `pipx`
(recommended), or `pip` within a virtual environment. Open up a terminal and
install with:

    pipx install postodon

## Configuration

 - Register an application on Mastodon as described here:
   <https://docs.joinmastodon.org/client/token/#app>
 - Get an access token as described here:
   <https://docs.joinmastodon.org/client/authorized/#flow>
 - Securely store the returned `access_token` for future reference
 - Run `postodon init` to create an empty config file (note the location)
 - Edit the config file to point to the name of the Mastodon instance (e.g.
   `botsin.space`) and the path to the posts file, e.g. `/path/to/posts.json`
 - Put the access token in an environment variable called `AUTH_TOKEN`

      export AUTH_TOKEN=<your_access_token_here>

## Usage

To publicly post a random post from the list (marked as English), and update
the list (i.e. mark the post having been posted):

    postodon

This is a shortcut for `postodon post`. NB if there are no unposted items left
in the list, a randomly-selected item from the 'posted' selection will be
posted instead.

To randomly select an item from the list without either updating the list or
posting (dry-run mode):

    postodon post -n

To add new posts to the list for future posting:

    postodon add "Text of post"

## Development

To contribute to this library, first checkout the code. Then create a new
virtual environment:

    cd postodon
    python -m venv .venv
    source .venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[dev,tests]'

To run the tests:

    pytest
