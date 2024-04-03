import asyncio
import os
import re
import json
from playwright.async_api import async_playwright

MAPTILER_API_KEY = os.environ.get("MAPTILER_API_KEY")
STADIA_API_KEY = os.environ.get("STADIA_API_KEY")
GEOAPIFY_API_KEY = os.environ.get("GEOAPIFY_API_KEY")

if MAPTILER_API_KEY is None:
    raise ValueError("MAPTILER_API_KEY environment variables must be set")

if STADIA_API_KEY is None:
    raise ValueError("STADIA_API_KEY environment variables must be set")

if GEOAPIFY_API_KEY is None:
    raise ValueError("GEOAPIFY_API_KEY environment variables must be set")

STYLES = {
    "MapTiler - backdrop": "https://api.maptiler.com/maps/backdrop/style.json?key={MAPTILER_API_KEY}",
    "MapTiler - basic": "https://api.maptiler.com/maps/basic/style.json?key={MAPTILER_API_KEY}",
    "Maptiler - bright": "https://api.maptiler.com/maps/bright/style.json?key={MAPTILER_API_KEY}",
    "Maptiler - dataviz": "https://api.maptiler.com/maps/dataviz/style.json?key={MAPTILER_API_KEY}",
    "Maptiler - landscape": "https://api.maptiler.com/maps/landscape/style.json?key={MAPTILER_API_KEY}",
    "Maptiler - ocean": "https://api.maptiler.com/maps/ocean/style.json?key={MAPTILER_API_KEY}",
    "Maptiler - openstreetmap": "https://api.maptiler.com/maps/openstreetmap/style.json?key={MAPTILER_API_KEY}",
    "Maptiler - outdoor": "https://api.maptiler.com/maps/outdoor/style.json?key={MAPTILER_API_KEY}",
    "Maptiler - satellite": "https://api.maptiler.com/maps/satellite/style.json?key={MAPTILER_API_KEY}",
    "Maptiler - streets": "https://api.maptiler.com/maps/streets/style.json?key={MAPTILER_API_KEY}",
    "Maptiler - toner": "https://api.maptiler.com/maps/toner/style.json?key={MAPTILER_API_KEY}",
    "Maptiler - topo": "https://api.maptiler.com/maps/topo/style.json?key={MAPTILER_API_KEY}",
    "Maptiler - winter": "https://api.maptiler.com/maps/winter/style.json?key={MAPTILER_API_KEY}",
    "StadiaMaps - Alidade Smooth": "https://tiles.stadiamaps.com/styles/alidade_smooth.json?api_key={STADIA_API_KEY}",
    "StadiaMaps - Alidade Smooth Dark": "https://tiles.stadiamaps.com/styles/alidade_smooth_dark.json?api_key={STADIA_API_KEY}",
    "StadiaMaps - Alidade Satellite": "https://tiles.stadiamaps.com/styles/alidade_satellite.json?api_key={STADIA_API_KEY}",
    "StadiaMaps - Stadia Outdoors": "https://tiles.stadiamaps.com/styles/outdoors.json?api_key={STADIA_API_KEY}",
    "StadiaMaps - Stamen Toner": "https://tiles.stadiamaps.com/styles/stamen_toner.json?api_key={STADIA_API_KEY}",
    "StadiaMaps - Stamen Terrain": "https://tiles.stadiamaps.com/styles/stamen_terrain.json?api_key={STADIA_API_KEY}",
    "StadiaMaps - Stamen Watercolor": "https://tiles.stadiamaps.com/styles/stamen_watercolor.json?api_key={STADIA_API_KEY}",
    "StadiaMaps - OSM Bright": "https://tiles.stadiamaps.com/styles/osm_bright.json?api_key={STADIA_API_KEY}",
    "Geoapify - osm-carto": "https://maps.geoapify.com/v1/styles/osm-carto/style.json?apiKey={GEOAPIFY_API_KEY}",
    "Geoapify - osm-bright": "https://maps.geoapify.com/v1/styles/osm-bright/style.json?apiKey={GEOAPIFY_API_KEY}",
    "Geoapify - osm-bright-grey": "https://maps.geoapify.com/v1/styles/osm-bright-grey/style.json?apiKey={GEOAPIFY_API_KEY}",
    "Geoapify - osm-bright-smooth": "https://maps.geoapify.com/v1/styles/osm-bright-smooth/style.json?apiKey={GEOAPIFY_API_KEY}",
    "Geoapify - klokantech-basic": "https://maps.geoapify.com/v1/styles/klokantech-basic/style.json?apiKey={GEOAPIFY_API_KEY}",
    "Geoapify - osm-liberty": "https://maps.geoapify.com/v1/styles/osm-liberty/style.json?apiKey={GEOAPIFY_API_KEY}",
    "Geoapify - maptiler-3d": "https://maps.geoapify.com/v1/styles/maptiler-3d/style.json?apiKey={GEOAPIFY_API_KEY}",
    "Geoapify - toner": "https://maps.geoapify.com/v1/styles/toner/style.json?apiKey={GEOAPIFY_API_KEY}",
    "Geoapify - toner-grey": "https://maps.geoapify.com/v1/styles/toner-grey/style.json?apiKey={GEOAPIFY_API_KEY}",
    "Geoapify - positron": "https://maps.geoapify.com/v1/styles/positron/style.json?apiKey={GEOAPIFY_API_KEY}",
    "Geoapify - positron-blue": "https://maps.geoapify.com/v1/styles/positron-blue/style.json?apiKey={GEOAPIFY_API_KEY}",
    "Geoapify - positron-red": "https://maps.geoapify.com/v1/styles/positron-red/style.json?apiKey={GEOAPIFY_API_KEY}",
    "Geoapify - dark-matter": "https://maps.geoapify.com/v1/styles/dark-matter/style.json?apiKey={GEOAPIFY_API_KEY}",
    "Geoapify - dark-matter-brown": "https://maps.geoapify.com/v1/styles/dark-matter-brown/style.json?apiKey={GEOAPIFY_API_KEY}",
    "Geoapify - dark-matter-dark-grey": "https://maps.geoapify.com/v1/styles/dark-matter-dark-grey/style.json?apiKey={GEOAPIFY_API_KEY}",
    "Geoapify - dark-matter-dark-purple": "https://maps.geoapify.com/v1/styles/dark-matter-dark-purple/style.json?apiKey={GEOAPIFY_API_KEY}",
    "Geoapify - dark-matter-purple-roads": "https://maps.geoapify.com/v1/styles/dark-matter-purple-roads/style.json?apiKey={GEOAPIFY_API_KEY}",
    "Geoapify - dark-matter-yellow-roads": "https://maps.geoapify.com/v1/styles/dark-matter-yellow-roads/style.json?apiKey={GEOAPIFY_API_KEY}",
}


def format(template):
    return eval(f"f'{template}'")


def convert_to_snake_case(string):
    string = string.replace("-", "")
    string = re.sub(" +", "_", string)
    string = string.lower()
    return string


async def time_style(style_name, style_url):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Vector Map Style Profiler</title>
        <script src="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.js"></script>
        <link href="https://unpkg.com/maplibre-gl@3.6.2/dist/maplibre-gl.css" rel="stylesheet">
    </head>

    <style>
        html {{
            height: 100%;
        }}

        body {{
            height: 100%;
            align-items: stretch;
            margin: 0;
            padding: 0;
        }}

        #map {{
            flex-grow: 1;
            min-height: 100%;
            max-height: 100%;
        }}
    </style>

    <body>
        <div id="map" style="width: 100%; height: 100%;"></div>
        <script>
            const startTime = performance.now();
            const map = new maplibregl.Map({{
                container: "map",
                style: "{format(style_url)}",
                center: [0, 51.4769], // Greenwich meridian
                zoom: 10,
                maxZoom: 18,
                minZoom: 5,
            }});

            map.on('load', (e) => {{
                const endLoadTime = performance.now();
                loadTime = endLoadTime - startTime;
                window.loadTime = loadTime;
            }});

        </script>
    </body>

    </html>
    """

    async with async_playwright() as p:
        browser_type = p.chromium
        browser = await browser_type.launch()
        context = await browser.new_context()
        page = await context.new_page()

        # # Enable network interception
        # await page.route("**/*", lambda route: route.continue_())
        # # Capture and print requests and responses
        # page.on(
        #     "request",
        #     lambda request: print(
        #         f"URL: {request.url}, Method: {request.method}, Headers: {request.headers}"
        #     ),
        # )
        # page.on(
        #     "response",
        #     lambda response: print(
        #         f"URL: {response.url}, Status: {response.status}, Headers: {response.headers}"
        #     ),
        # )

        try:
            await page.set_content(html_content)
            await page.wait_for_function("window.loadTime", timeout=30000)
            load_time = int(await page.evaluate("() => { return window.loadTime; }"))
            await page.screenshot(
                path=f"screenshots/{convert_to_snake_case(style_name)}.png"
            )
            print(f"{style_name}: {load_time}")

        except asyncio.TimeoutError:
            print(f"Timeout occurred for {style_name}")
            load_time = None

        except Exception as e:
            print(f"An error occurred for {style_name}: {str(e)}")
            load_time = None

        finally:
            await context.close()
            await browser.close()

        return {
            "style_id": convert_to_snake_case(style_name),
            "style_name": style_name,
            "load_time": load_time,
            "style_url": style_url,
            "screenshot": f"screenshots/{convert_to_snake_case(style_name)}.png",
        }


async def main():
    dataset = []
    for k, v in STYLES.items():
        dataset.append(await time_style(k, v))

    dataset.sort(key=lambda x: x.get("load_time", float("inf")))
    with open("timing_results.json", "w") as f:
        f.write(json.dumps(dataset, indent=4, sort_keys=True))


if __name__ == "__main__":
    asyncio.run(main())
