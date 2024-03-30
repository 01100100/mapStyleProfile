# Vector Map Style Profiler 🗺️📏🎨

## Website

The Vector Map Style Profiler is a tool that allows you to profile the performance of different vector map styles. It takes a [MapLibre style](https://maplibre.org/maplibre-style-spec/) as a input and displays timing information about how long it took to load and render the map on the page.

### External Resources

The site depends on [MapLibre GL](https://github.com/maplibre/maplibre-gl-js) to draw the map on the page. The library is included in the site through a content delivery network (CDN) link.

### Hosting

The Vector Map Style Profiler is hosted on GitHub Pages. You can access the app by visiting the following URL: [https://01100100.github.io/mapStyleProfile](https://01100100.github.io/mapStyleProfile).

## Automated browser testing

There is a python script that uses [playwright](https://playwright.dev/python/docs/intro) to automate browser testing for a number of different styles and prints the loading time of each style to the terminal.

## Docker

The Vector Map Style Profiler can be run in a Docker container. The Dockerfile is included in the repository. To build the Docker image, run the following command:

```bash
docker build -t map-style-profiler .
```

To run the Docker container, run the following command:

```bash
docker run --env-file=.env --rm --ipc=host map-style-profiler
```

To open a shell in a Docker container with playwright installed and the working directory mounted inside the container, run the following command:

```bash
sudo docker run -it --rm --ipc=host -v ${PWD}/:/project --env-file=.env mcr.microsoft.com/playwright/python:v1.42.0-jammy /bin/bash
```

NOTE: You must install the requirement.txt file in the container before you can run the python script.

```bash
pip install -r requirements.txt
python /usr/src/app/main.py
```

## Contributions

Contributions to the Vector Map Style Profiler project are welcome. If you find any issues or have suggestions for improvements, please feel free to submit a pull request or open an issue.

## License

This project is licensed under the [Unlicense](https://github.com/01100100/mapStyleProfile/blob/main/LICENSE).
