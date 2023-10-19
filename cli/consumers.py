from channels.generic.websocket import AsyncWebsocketConsumer
import json
from subprocess import Popen, PIPE
from .helper import py_command, sherlock_dir

class UsernameSearchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Extract the username from the received data
        data = json.loads(text_data)
        username = data['args']

        # Use the Sherlock tool to search for the username
        full_cmd = f"{py_command()} {sherlock_dir()}/sherlock {username}"
        proc = Popen(full_cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        outs, errs = proc.communicate()

        # Process the results and send them back via WebSocket
        if outs:
            sites = outs.decode().strip().split('\n')
            site_results = []
            for site in sites:
                if ': ' in site:
                    site_name, site_link = site.split(': ', 1)
                    site_entry = {
                        "name": site_name.lstrip('[+] '),
                        "link": site_link
                    }
                    site_results.append(site_entry)
                    # Send each result immediately to the client
                    await self.send(text_data=json.dumps(site_entry))
        else:
            error_message = {"error": errs.decode()}
            await self.send(text_data=json.dumps(error_message))
