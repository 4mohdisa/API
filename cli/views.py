import os
from subprocess import *

from rest_framework.response import Response
from rest_framework.views import APIView

from helper import *
import json
from django.http import HttpResponse, JsonResponse
import threading

# class CliView(APIView):
#     """Pass in command directly to sherlock."""
#     def post(self, request):
#         data = json.loads(request.body)
#         args = data['args']

#         if valid_args(args) == False:
#             output = "Invalid argument string"
#         # else:
#         #     full_cmd = f"{py_command()} {sherlock_dir()}/sherlock {args}"
#         #     proc = Popen(full_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
#         #     outs, errs = proc.communicate()
#         #     output = outs if outs else errs

#         else:
#             full_cmd = f"{py_command()} {sherlock_dir()}/sherlock {args}"
#             proc = Popen(full_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
#             outs, errs = proc.communicate()

#         if outs:
#                 # Split the output by line and create a list of sites
#                 sites = outs.decode().strip().split('\n')

#                 # Create a dictionary with site names as keys and results as values
#                 site_results = []
#                 for site in sites:
#                     print(site)
                    
#                     if ': ' in site:
#                         site_name, site_link = site.split(': ', 1)
#                         site_entry = {
#                             "name": site_name.lstrip('[+] '),
#                             "link": site_link
#                         }
#                         site_results.append(site_entry)

#                 output = {"results": site_results}
#         else:
#                 output = {"error": errs.decode()}

#         return JsonResponse(output)

class DataView(APIView):
    """Request JSON data from sherlock resources."""

    def get(self, request):
        # Create a thread pool with 10 threads
        thread_pool = threading.ThreadPool(10)

        # Start 10 threads to fetch JSON data from sherlock resources
        tasks = []
        for resource in sherlock_resources():
            tasks.append(thread_pool.apply_async(get_sherlock_data, args=(resource,)))

        # Get the results of the threads
        results = [task.get() for task in tasks]

        # Return the JSON data as a response
        return JsonResponse(results)


def get_sherlock_data(resource):
    full_cmd = f"{py_command()} {sherlock_dir()}/sherlock {resource}"
    proc = Popen(full_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    outs, errs = proc.communicate()
    data = outs if outs else errs
    return data