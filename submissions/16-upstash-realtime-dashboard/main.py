"""
Upstash Real-time Dashboard
Showcases: REST API with MONITOR via SSE
"""
import os
from upstash_redis import Redis
from dotenv import load_dotenv

load_dotenv()

def main():
    print("=" * 50)
    print("Upstash Real-time Dashboard")
    print("=" * 50)

    redis = Redis(
        url=os.getenv("UPSTASH_REDIS_REST_URL"),
        token=os.getenv("UPSTASH_REDIS_REST_TOKEN")
    )

    # Demo: Track page views
    page = "/home"
    redis.incr(f"pageviews:{page}")
    views = redis.get(f"pageviews:{page}")
    print(f"\n📊 Page views for {page}: {views}")

    # Demo: User activity tracking
    redis.zadd("active_users", {"user:123": 1, "user:456": 2, "user:789": 3})
    active = redis.zrange("active_users", 0, -1, withscores=True)
    print(f"\n👥 Active users: {active}")

    # Demo: Real-time events (would use SSE in production)
    redis.lpush("events", '{"type": "click", "element": "button"}')
    events = redis.lrange("events", 0, 5)
    print(f"\n📡 Recent events: {events}")

    print("\n💡 For real-time MONITOR, use SSE endpoint:")
    print("   curl -N https://your-url.upstash.io/monitor")

if __name__ == "__main__":
    main()
