# Open Autonomy Compose

A framework for working with FSM based ABCI applications

## Install

```bash
pip3 install open-autonomy-compose
```

## Generate FSM Specification

If you have an ABCI app composition and you want to generate a specification for the same run

```bash
compose fsm from-app PATH_TO_ABCI_APP
```

## Perform consistency checks

To peform consistency check on an ABCI app run

```bash
compose check PATH_TO_ABCI_APP
```

Supported consistency checks

- SyncDB
  - Pre/Post Conditions for round transitions
  - Static analyser for checking if the required updates are being performed or not

## Inspect the ABCI App

To inspect the ABCI app run

```bash
compose inspect PATH_TO_ABCI_APP
```

Running this will start an http server, open the URL for HTTP server and you can inspect the ABCI app in the browser

## Development

- Ensure your machine satisfies the following requirements:

    - Python `>= 3.8`
    - [Pip](https://pip.pypa.io/en/stable/installation/)
    - [Poetry](https://python-poetry.org/docs/#installation)

- Clone the repository:

    ```bash
    git clone git@github.com:valory-xyz/open-autonomy.git
    ```

- Create a development environment

    ```bash
    poetry install
    ```

- Launch poetry shell in start developing

    ```bash
    poetry shell
    ```

## Cite

If you are using our software in a publication, please consider to cite it with the following BibTex entry:

```
@misc{open-autonomy-compose,
  Author = {Viraj Patel},
  Title = {Open Autonomy Compose},
  Year = {2023},
}
```
