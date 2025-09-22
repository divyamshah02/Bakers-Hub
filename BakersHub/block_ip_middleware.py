from django.shortcuts import redirect
import time,datetime
class BlockIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of IP addresses to block
        blocked_ips = ['185.234.216.114',
                        '176.111.174.153',
                        '85.209.11.117',
                        '2.57.149.115',
                        '122.182.205.193',
                        '85.209.11.20',
                        # '49.36.66.73',
                        ]

        # Get the client's IP address
        client_ip = self.get_client_ip(request)

        # Check if the client's IP is in the blocked_ips list
        if client_ip in blocked_ips:
            with open("logs/ip_log.txt",'a') as ip_log:
                date_time = datetime.datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
                ip_log.write(f"[{date_time}] -> [Blocked IP:- {request.method}] {client_ip} - {request.META.get('HTTP_USER_AGENT', '')}\n")
                # raise Exception("Automated requests are not allowed.")
            time.sleep(5)
            return redirect("https://www.google.com")

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        return ip
