import asyncio
import aiohttp
import logging
import secrets
import os

from tasksio import TaskPool

if os.name == "posix":
    os.system("clear")
else:
    os.system("cls")
    
logging.basicConfig(
    level=logging.INFO, 
    format="\x1b[38;5;226m[\x1b[0m%(asctime)s\x1b[38;5;226m] \x1b[0m| \x1b[38;5;226m%(message)s", 
    datefmt="%I:%M:%S"
)

class Webhooker(object):

    def __init__(self):
        self.colors = {
            "light_yellow": "\x1b[38;5;226m",
            "soft_orange": "\x1b[38;5;215m",
            "skin_color": "\x1b[38;5;216m",
            "reset": "\x1b[0m"
        }

        self.banner = """
{}╦ ╦╔═╗╔╗ ╦ ╦╔═╗╔═╗╦╔═╔═╗╦═╗
{}║║║║╣ ╠╩╗╠═╣║ ║║ ║╠╩╗║╣ ╠╦╝
{}╚╩╝╚═╝╚═╝╩ ╩╚═╝╚═╝╩ ╩╚═╝╩╚═
        """.format("\x1b[38;5;214m", self.colors["soft_orange"], self.colors["skin_color"])

    async def webhook_flood(self, webhook: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook, json={"content": "`{}`".format(secrets.token_hex(16)), "username": "{}".format(secrets.token_urlsafe(8))}) as response:
                if response.status == 204:
                    logging.info("Sent new message")
                else:
                    logging.error("Ratelimited")
    
    async def webhook_spam(self, message: str, username: str, webhook: str):
        async with aiohttp.ClientSession() as session:
            async with session.post(webhook, json={"content": message, "username": username}) as response:
                if response.status == 204:
                    logging.info("Sent new message")
                else:
                    logging.error("Ratelimited")

    async def user_interface(self):
        async with aiohttp.ClientSession() as session:
            print(self.banner)
            print("""
{}[{}1{}] {}Flood Webhook {}({}Spam webhook with randomized usernames and messages{})
{}[{}2{}] {}Delete Webhook {}({}Deletes given webhook{})
{}[{}3{}] {}Spam Webhook {}({}Spams webhook with given username and message{})
            """.format(self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"]))
            commands = input("{}[{}\033[4mscripted@onTop\033[0m{}]\033[0m {}Your Choice{}:{} ".format(self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"]))
            if commands == "1":
                webhook = input("{}[{}\033[4mscripted@onTop\033[0m{}]\033[0m {}Webhook{}:{} ".format(self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"]))
                
                amount = int(input("{}[{}\033[4mscripted@onTop\033[0m{}]\033[0m {}Amount{}:{} ".format(self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"])))
                tasks = int(input("{}[{}\033[4mscripted@onTop\033[0m{}]\033[0m {}Tasks{}:{} ".format(self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"])))
                print()
                async with TaskPool(tasks) as pool:
                    for i in range(amount):
                        await pool.put(self.webhook_flood(webhook))

            elif commands == "2":
                webhook = input("{}[{}\033[4mscripted@onTop\033[0m{}]\033[0m {}Webhook{}:{} ".format(self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"]))
                async with session.delete(webhook) as response:
                    if response.status == 204:
                        logging.info("Succesfully deleted webhook")
                        input()
                    else:
                        logging.error("Failed to delete webhook for unknown reasons")
                        input()

            elif commands == "3":
                webhook = input("{}[{}\033[4mscripted@onTop\033[0m{}]\033[0m {}Webhook{}:{} ".format(self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"]))
                message = input("{}[{}\033[4mscripted@onTop\033[0m{}]\033[0m {}Message{}:{} ".format(self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"]))
                username = input("{}[{}\033[4mscripted@onTop\033[0m{}]\033[0m {}Username{}:{} ".format(self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"]))
                
                amount = int(input("{}[{}\033[4mscripted@onTop\033[0m{}]\033[0m {}Amount{}:{} ".format(self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"])))
                tasks = int(input("{}[{}\033[4mscripted@onTop\033[0m{}]\033[0m {}Tasks{}:{} ".format(self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"], self.colors["light_yellow"], self.colors["reset"])))
                print()
                async with TaskPool(tasks) as pool:
                    for i in range(amount):
                        await pool.put(self.webhook_spam(message, username, webhook))
            
if __name__ == "__main__":
    client = Webhooker()
    asyncio.run(client.user_interface())
