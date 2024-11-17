from datetime import datetime
from django.utils.timezone import make_aware


class LoggingRequestTimeMiddleware:
    """
    Middleware to log the time taken to process each request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = make_aware(datetime.now())  # Get current time
        response = self.get_response(request)  # Process the request
        end_time = make_aware(datetime.now())  # Get the end time

        time_taken = end_time - start_time
        print(f"Request processed in: {time_taken}")

        return response