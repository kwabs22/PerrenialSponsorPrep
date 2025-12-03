"""
Mapbox Trip Planner
Showcases: Standard Maps + Navigation
"""
import os
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from dotenv import load_dotenv

load_dotenv()

MAPBOX_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")

class MapHandler(BaseHTTPRequestHandler):
    """Serve the trip planner map."""

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Mapbox Trip Planner</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <script src="https://api.mapbox.com/mapbox-gl-js/v3.0.0/mapbox-gl.js"></script>
                <link href="https://api.mapbox.com/mapbox-gl-js/v3.0.0/mapbox-gl.css" rel="stylesheet">
                <style>
                    body {{ margin: 0; padding: 0; }}
                    #map {{ position: absolute; top: 0; bottom: 0; width: 100%; }}
                    .sidebar {{
                        position: absolute; top: 10px; left: 10px; z-index: 1;
                        background: white; padding: 15px; border-radius: 8px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.2); max-width: 300px;
                    }}
                    .sidebar h3 {{ margin-top: 0; }}
                    .waypoint {{ margin: 10px 0; }}
                    input {{ width: 100%; padding: 8px; margin: 5px 0; }}
                    button {{ width: 100%; padding: 10px; background: #4264fb;
                             color: white; border: none; border-radius: 4px; cursor: pointer; }}
                    #route-info {{ margin-top: 15px; padding-top: 15px; border-top: 1px solid #eee; }}
                </style>
            </head>
            <body>
                <div id="map"></div>

                <div class="sidebar">
                    <h3>Trip Planner</h3>

                    <div class="waypoint">
                        <label>Start</label>
                        <input type="text" id="start" value="San Francisco, CA">
                    </div>

                    <div class="waypoint">
                        <label>Destination</label>
                        <input type="text" id="end" value="Los Angeles, CA">
                    </div>

                    <button onclick="planRoute()">Plan Route</button>

                    <div id="route-info"></div>
                </div>

                <script>
                    mapboxgl.accessToken = '{MAPBOX_TOKEN or "YOUR_TOKEN"}';

                    const map = new mapboxgl.Map({{
                        container: 'map',
                        style: 'mapbox://styles/mapbox/standard',  // New Standard style!
                        center: [-119.4179, 36.7783],  // California
                        zoom: 5,
                        pitch: 45,  // 3D view
                        bearing: 0
                    }});

                    // Add navigation controls
                    map.addControl(new mapboxgl.NavigationControl());
                    map.addControl(new mapboxgl.GeolocateControl({{
                        positionOptions: {{ enableHighAccuracy: true }},
                        trackUserLocation: true
                    }}));

                    // Enable 3D terrain
                    map.on('load', () => {{
                        map.addSource('mapbox-dem', {{
                            type: 'raster-dem',
                            url: 'mapbox://mapbox.mapbox-terrain-dem-v1',
                            tileSize: 512
                        }});
                        map.setTerrain({{ source: 'mapbox-dem', exaggeration: 1.5 }});

                        // Add sky layer
                        map.addLayer({{
                            id: 'sky',
                            type: 'sky',
                            paint: {{
                                'sky-type': 'atmosphere',
                                'sky-atmosphere-sun': [0.0, 90.0],
                                'sky-atmosphere-sun-intensity': 15
                            }}
                        }});
                    }});

                    // Markers
                    let startMarker, endMarker;

                    async function planRoute() {{
                        const start = document.getElementById('start').value;
                        const end = document.getElementById('end').value;

                        // Geocode locations
                        const startCoords = await geocode(start);
                        const endCoords = await geocode(end);

                        if (!startCoords || !endCoords) {{
                            alert('Could not find locations');
                            return;
                        }}

                        // Add markers
                        if (startMarker) startMarker.remove();
                        if (endMarker) endMarker.remove();

                        startMarker = new mapboxgl.Marker({{ color: 'green' }})
                            .setLngLat(startCoords)
                            .addTo(map);

                        endMarker = new mapboxgl.Marker({{ color: 'red' }})
                            .setLngLat(endCoords)
                            .addTo(map);

                        // Get directions
                        const directions = await getDirections(startCoords, endCoords);

                        if (directions) {{
                            drawRoute(directions.routes[0].geometry);
                            showRouteInfo(directions.routes[0]);
                        }}
                    }}

                    async function geocode(query) {{
                        const response = await fetch(
                            `https://api.mapbox.com/geocoding/v5/mapbox.places/${{encodeURIComponent(query)}}.json?access_token=${{mapboxgl.accessToken}}`
                        );
                        const data = await response.json();
                        return data.features[0]?.center;
                    }}

                    async function getDirections(start, end) {{
                        const response = await fetch(
                            `https://api.mapbox.com/directions/v5/mapbox/driving/${{start.join(',')}}%3B${{end.join(',')}}?geometries=geojson&access_token=${{mapboxgl.accessToken}}`
                        );
                        return response.json();
                    }}

                    function drawRoute(geometry) {{
                        if (map.getSource('route')) {{
                            map.getSource('route').setData({{ type: 'Feature', geometry }});
                        }} else {{
                            map.addSource('route', {{
                                type: 'geojson',
                                data: {{ type: 'Feature', geometry }}
                            }});
                            map.addLayer({{
                                id: 'route',
                                type: 'line',
                                source: 'route',
                                paint: {{
                                    'line-color': '#4264fb',
                                    'line-width': 5
                                }}
                            }});
                        }}

                        // Fit map to route
                        const bounds = geometry.coordinates.reduce(
                            (bounds, coord) => bounds.extend(coord),
                            new mapboxgl.LngLatBounds()
                        );
                        map.fitBounds(bounds, {{ padding: 50 }});
                    }}

                    function showRouteInfo(route) {{
                        const distance = (route.distance / 1609.34).toFixed(1);
                        const duration = Math.round(route.duration / 60);

                        document.getElementById('route-info').innerHTML = `
                            <strong>Route Info</strong><br>
                            Distance: ${{distance}} miles<br>
                            Duration: ${{duration}} minutes
                        `;
                    }}
                </script>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        print(f"[Mapbox] {args[0]}")

def main():
    print("=" * 50)
    print("Mapbox Trip Planner")
    print("=" * 50)

    if not MAPBOX_TOKEN:
        print("\nSetup required:")
        print("1. Create Mapbox account at https://mapbox.com")
        print("2. Get access token from Account page")
        print("3. Copy token to .env file")

        print("\n🗺️ Features demonstrated:")
        print("  - Standard Maps (new 2024 style)")
        print("  - 3D Terrain visualization")
        print("  - Geocoding API")
        print("  - Directions API")
        print("  - Navigation controls")
        return

    print(f"\nMapbox Token: {MAPBOX_TOKEN[:15]}...")

    server = HTTPServer(("localhost", 3000), MapHandler)
    print("\nServer running at http://localhost:3000")

    webbrowser.open("http://localhost:3000")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")

if __name__ == "__main__":
    main()
