import asyncio
import os
from playwright.async_api import async_playwright

MAPTILER_API_KEY = os.environ.get("MAPTILER_API_KEY")
STADIA_API_KEY = os.environ.get("STADIA_API_KEY")

if MAPTILER_API_KEY is None or STADIA_API_KEY is None:
    raise ValueError(
        "MAPTILER_API_KEY and STADIA_API_KEY environment variables must be set"
    )

STYLES = {
    "MapTiler - backdrop": f"https://api.maptiler.com/maps/backdrop/style.json?key={MAPTILER_API_KEY}",
    "MapTiler - basic": f"https://api.maptiler.com/maps/basic/style.json?key={MAPTILER_API_KEY}",
    "Maptiler - bright": f"https://api.maptiler.com/maps/bright/style.json?key={MAPTILER_API_KEY}",
    "Maptiler - dataviz": f"https://api.maptiler.com/maps/dataviz/style.json?key={MAPTILER_API_KEY}",
    "Maptiler - landscape": f"https://api.maptiler.com/maps/landscape/style.json?key={MAPTILER_API_KEY}",
    "Maptiler - ocean": f"https://api.maptiler.com/maps/ocean/style.json?key={MAPTILER_API_KEY}",
    "Maptiler - openstreetmap": f"https://api.maptiler.com/maps/openstreetmap/style.json?key={MAPTILER_API_KEY}",
    "Maptiler - outdoor": f"https://api.maptiler.com/maps/outdoor/style.json?key={MAPTILER_API_KEY}",
    "Maptiler - satellite": f"https://api.maptiler.com/maps/satellite/style.json?key={MAPTILER_API_KEY}",
    "Maptiler - streets": f"https://api.maptiler.com/maps/streets/style.json?key={MAPTILER_API_KEY}",
    "Maptiler - toner": f"https://api.maptiler.com/maps/toner/style.json?key={MAPTILER_API_KEY}",
    "Maptiler - topo": f"https://api.maptiler.com/maps/topo/style.json?key={MAPTILER_API_KEY}",
    "Maptiler - winter": f"https://api.maptiler.com/maps/winter/style.json?key={MAPTILER_API_KEY}",
    "StadiaMaps - Alidade Smooth": f"https://tiles.stadiamaps.com/styles/alidade_smooth.json?api_key={STADIA_API_KEY}",
    "StadiaMaps - Alidade Smooth Dark": f"https://tiles.stadiamaps.com/styles/alidade_smooth_dark.json?api_key={STADIA_API_KEY}",
    "StadiaMaps - Alidade Satellite": f"https://tiles.stadiamaps.com/styles/alidade_satellite.json?api_key={STADIA_API_KEY}",
    "StadiaMaps - Stadia Outdoors": f"https://tiles.stadiamaps.com/styles/outdoors.json?api_key={STADIA_API_KEY}",
    "StadiaMaps - Stamen Toner": f"https://tiles.stadiamaps.com/styles/stamen_toner.json?api_key={STADIA_API_KEY}",
    "StadiaMaps - Stamen Terrain": f"https://tiles.stadiamaps.com/styles/stamen_terrain.json?api_key={STADIA_API_KEY}",
    "StadiaMaps - Stamen Watercolor": f"https://tiles.stadiamaps.com/styles/stamen_watercolor.json?api_key={STADIA_API_KEY}",
    "StadiaMaps - OSM Bright": f"https://tiles.stadiamaps.com/styles/osm_bright.json?api_key={STADIA_API_KEY}",
}


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
                style: "{style_url}",
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
        page = await browser.new_page()

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
            load_time = await page.evaluate("() => { return window.loadTime; }")
            print(f"{style_name}: {load_time}")

        except asyncio.TimeoutError:
            print(f"Timeout occurred for {style_name}")

        except Exception as e:
            print(f"An error occurred for {style_name}: {str(e)}")

        finally:
            await browser.close()


for k, v in STYLES.items():
    asyncio.run(time_style(k, v))
