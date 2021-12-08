import os
import logging
import secrets
import asyncio
import aiohttp

from tasksio import TaskPool

os.system('clear')

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s %(message)s", 
    datefmt=f"\t\u001b[38;5;203m[\u001b[38;5;255m%I:%M:%S\u001b[38;5;203m]\u001b[38;5;255m"
)

pink = "\u001b[38;5;198m"
red = "\u001b[38;5;203m"
reset = "\u001b[38;5;255m"

class Webhooker:

    def __init__(self, debug: bool):
        self.debug = debug
        self._banner = """
\t\t\u001b[38;5;203m██╗    ██╗███████╗██████╗ ██╗  ██╗ ██████╗  ██████╗ ██╗  ██╗███████╗██████╗
\t\t\u001b[38;5;203m██║    ██║██╔════╝██╔══██╗██║  ██║██╔═══██╗██╔═══██╗██║ ██╔╝██╔════╝██╔══██╗
\t\t\u001b[38;5;203m██║ █╗ ██║█████╗  ██████╔╝███████║██║   ██║██║   ██║█████╔╝ █████╗  ██████╔╝
\t\t\u001b[38;5;203m██║███╗██║██╔══╝  ██╔══██╗██╔══██║██║   ██║██║   ██║██╔═██╗ ██╔══╝  ██╔══██╗
\t\t\u001b[38;5;203m╚███╔███╔╝███████╗██████╔╝██║  ██║╚██████╔╝╚██████╔╝██║  ██╗███████╗██║  ██║
\t\t\u001b[38;5;203m ╚══╝╚══╝ ╚══════╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

        """

    async def webhook_flood(self, webhook: str, amount: int, message: str, name: str):
        async with aiohttp.ClientSession() as session:
            for i in range(amount):
                async with session.post(webhook, json={"content": "%s -> `%s`" % (message, secrets.token_hex(16)), "username": "%s -> %s" % (name, secrets.token_urlsafe(8))}) as r:
                    if r.status == 204:
                        logging.info("%s-> %sSent New Message %s-> %s%s" % (reset, red, reset, red, i+1))
                    else:
                        logging.error("%s-> %sRatelimited" % (reset, red))
            input()
            exit()

    async def webhook_delete(self, webhook: str):
        async with aiohttp.ClientSession() as session:
            async with session.delete(webhook) as r:
                if r.status == 204:
                    logging.info("-> Succesfully Deleted")
                    input()
                    exit()
                else:
                    logging.error("-> Failed to delete Webhook")
                    input()
                    exit()

    async def webhook_spam(self, webhook: str, amount: int, message: str, name: str):
        async with aiohttp.ClientSession() as session:
            for i in range(amount):
                async with session.post(webhook, json={"content": message, "username": name}) as r:
                    if r.status == 204:
                        logging.info("%s-> %sSent New Message %s-> %s%s" % (reset, red, reset, red, i+1))
                    else:
                        logging.error("%s-> %sRatelimited" % (reset, red))
            input()
            exit()

    async def start(self):
        print(self._banner)
        logging.info("%s-> %s\"%sflood%s\"%s  : %sFloods Webhook with Multiple & Randomized Usernames." % (reset, reset, red, reset, reset, red))
        logging.info("%s-> %s\"%sdelete%s\"%s : %sDeletes given Webhook." % (reset, reset, red, reset, reset, red))
        logging.info("%s-> %s\"%sspam%s\"%s   : %sSpams Webhook with given username and message." % (reset, reset, red, reset, reset, red))
        print()
        choice = input("\t%s[%s?%s] %sYour Choice%s: %s" % (red, reset, red, reset, red, reset))
        if choice == "flood":
            webhook = input("\t%s[%s?%s] %sWebhook%s: %s" % (red, reset, red, reset, red, reset))
            amount = int(input("\t%s[%s?%s] %sAmount%s: %s" % (red, reset, red, reset, red, reset)))
            message = input("\t%s[%s?%s] %sMessage%s: %s" % (red, reset, red, reset, red, reset))
            name = input("\t%s[%s?%s] %sName%s: %s" % (red, reset, red, reset, red, reset))
            threads = int(input("\t%s[%s?%s] %sThreads [high = faster]%s: %s" % (red, reset, red, reset, red, reset)))
            print()
            async with TaskPool(threads) as pool:
                for i in range(amount):
                    await pool.put(self.webhook_flood(webhook, amount, message, name))
        elif choice == "delete":
            webhook = input("\t%s[%s?%s] %sWebhook%s: %s" % (red, reset, red, reset, red, reset))
            print()
            async with TaskPool(9000) as pool:
                for i in range(amount):
                    await pool.put(self.webhook_delete(webhook))
        elif choice == "spam":
            webhook = input("\t%s[%s?%s] %sWebhook%s: %s" % (red, reset, red, reset, red, reset))
            amount = int(input("\t%s[%s?%s] %sAmount%s: %s" % (red, reset, red, reset, red, reset)))
            message = input("\t%s[%s?%s] %sMessage%s: %s" % (red, reset, red, reset, red, reset))
            name = input("\t%s[%s?%s] %sName%s: %s" % (red, reset, red, reset, red, reset))
            threads = int(input("\t%s[%s?%s] %sThreads [high = faster]%s: %s" % (red, reset, red, reset, red, reset)))
            print()
            async with TaskPool(threads) as pool:
                for i in range(amount):
                    await pool.put(self.webhook_spam(webhook, amount, message, name))

if __name__ == "__main__":
    client = Webhooker(
        debug=False
    )
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(client.start())
    except Exception:
        print("Tasks Finished..")
        input()
        exit()
