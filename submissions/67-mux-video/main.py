"""
Mux Video Streaming Demo
Showcases: Video upload, playback, analytics
"""

import os
from dotenv import load_dotenv

load_dotenv()

MUX_TOKEN_ID = os.getenv("MUX_TOKEN_ID")
MUX_TOKEN_SECRET = os.getenv("MUX_TOKEN_SECRET")

mux = None
try:
    import mux_python
    if MUX_TOKEN_ID and MUX_TOKEN_SECRET:
        config = mux_python.Configuration()
        config.username = MUX_TOKEN_ID
        config.password = MUX_TOKEN_SECRET
        mux = mux_python.ApiClient(config)
        print("Mux initialized")
    else:
        print("Warning: Mux credentials not set. Running in demo mode.")
except ImportError:
    print("mux_python not installed. Running in demo mode.")

def create_asset_demo():
    """Create a video asset"""
    print("\nCreate Asset Demo:")

    if mux:
        assets_api = mux_python.AssetsApi(mux)
        create_asset_request = mux_python.CreateAssetRequest(
            input=[mux_python.InputSettings(url="https://example.com/video.mp4")],
            playback_policy=[mux_python.PlaybackPolicy.PUBLIC]
        )
        asset = assets_api.create_asset(create_asset_request)
        print(f"  Asset ID: {asset.data.id}")
        print(f"  Status: {asset.data.status}")
    else:
        print("  [Demo] Create asset from URL:")
        print("    Input: https://example.com/video.mp4")
        print("    Asset ID: abc123xyz")
        print("    Playback ID: def456uvw")

def playback_demo():
    """Get playback URL"""
    print("\nPlayback Demo:")

    playback_id = "demo-playback-id"
    urls = {
        "HLS": f"https://stream.mux.com/{playback_id}.m3u8",
        "Thumbnail": f"https://image.mux.com/{playback_id}/thumbnail.jpg",
        "GIF": f"https://image.mux.com/{playback_id}/animated.gif",
        "Storyboard": f"https://image.mux.com/{playback_id}/storyboard.vtt",
    }

    print("  Playback URLs:")
    for name, url in urls.items():
        print(f"    {name}: {url}")

def player_demo():
    """Mux Player integration"""
    print("\nMux Player Demo:")

    code = '''
<!-- Mux Player Web Component -->
<script src="https://cdn.jsdelivr.net/npm/@mux/mux-player"></script>

<mux-player
  playback-id="YOUR_PLAYBACK_ID"
  metadata-video-title="My Video"
  metadata-viewer-user-id="user-123"
  accent-color="#FF0000"
  autoplay
></mux-player>
'''
    print(code)

def live_stream_demo():
    """Create live stream"""
    print("\nLive Stream Demo:")

    if mux:
        live_api = mux_python.LiveStreamsApi(mux)
        create_request = mux_python.CreateLiveStreamRequest(
            playback_policy=[mux_python.PlaybackPolicy.PUBLIC],
            new_asset_settings=mux_python.CreateAssetRequest(
                playback_policy=[mux_python.PlaybackPolicy.PUBLIC]
            )
        )
        stream = live_api.create_live_stream(create_request)
        print(f"  Stream Key: {stream.data.stream_key}")
        print(f"  RTMP URL: rtmps://global-live.mux.com:443/app")
    else:
        print("  [Demo] Live stream config:")
        print("    Stream Key: live_xxx_secret")
        print("    RTMP URL: rtmps://global-live.mux.com:443/app")
        print("    Playback: https://stream.mux.com/xxx.m3u8")

def realtime_demo():
    """Real-time video (WebRTC)"""
    print("\nReal-time Video Demo:")

    print("  Mux Real-Time enables WebRTC video:")
    print("    - Ultra-low latency (<500ms)")
    print("    - Browser-to-browser calls")
    print("    - Broadcasting to thousands")

    code = '''
// Client-side WebRTC
import MuxRealTime from "@mux/spaces-web";

const space = new MuxRealTime.Space("space-id", {
  token: "jwt-token"
});

const localParticipant = await space.join();
const localTracks = await localParticipant.publishTracks({
  video: true,
  audio: true
});
'''
    print(f"\n  Example:\n{code}")

def analytics_demo():
    """Video analytics"""
    print("\nAnalytics Demo:")

    print("  Mux Data provides:")
    print("    - Views and watch time")
    print("    - Buffering metrics")
    print("    - Quality of experience")
    print("    - Error tracking")

    print("\n  Sample metrics:")
    print("    Total views: 10,245")
    print("    Avg watch time: 4m 32s")
    print("    Rebuffer %: 0.8%")
    print("    Error rate: 0.2%")

def main():
    print("=" * 50)
    print("Mux Video Streaming Demo")
    print("=" * 50)

    print("\nAvailable demos:")
    print("  1. Create Asset")
    print("  2. Playback URLs")
    print("  3. Mux Player")
    print("  4. Live Streaming")
    print("  5. Real-time Video")
    print("  6. Analytics")

    choice = input("\nSelect demo (1-6): ").strip()

    demos = {"1": create_asset_demo, "2": playback_demo, "3": player_demo,
             "4": live_stream_demo, "5": realtime_demo, "6": analytics_demo}

    if choice in demos:
        demos[choice]()
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
