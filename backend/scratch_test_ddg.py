import sys
try:
    from duckduckgo_search import DDGS
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "duckduckgo-search"])
    from duckduckgo_search import DDGS

def test_ddg():
    try:
        print("Searching DuckDuckGo for Germany vs Curacao 14 June 2026 score...")
        with DDGS() as ddgs:
            results = list(ddgs.text("Germany vs Curacao June 14 2026 score", max_results=3))
            for r in results:
                print(r['title'])
                print(r['href'])
                print(r['body'])
                print("---")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_ddg()
