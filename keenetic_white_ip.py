import asyncio
import telnetlib3
import re
import requests


async def shell(reader, writer):
    # Get external IP
    ip_external = requests.get('https://api.ipify.org').text

    # Get PPPoE IP
    await reader.readuntil(b":")
    writer.write("admin\n")
    await reader.readuntil(b":")
    writer.write("admin\n")
    await reader.readuntil(b">")
    writer.write("show interface PPPoE0\n")
    outp = await reader.readuntil(b">")
    ip_pppoe = re.search(r'address: (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', outp.decode("ascii")).group(1)

    # Check white IP
    while ip_pppoe != ip_external:
        # Reconnect PPPoE
        print("Reconnecting")

        # Wait 5 minutes
        exit()

    print("White IP:", ip_external)

    # Disconnect Keenetic
    writer.write("exit\n")


async def main():
    reader, writer = await telnetlib3.open_connection('192.168.0.1', 23, shell=shell)
    await writer.protocol.waiter_closed


if __name__ == '__main__':
    asyncio.run(main())
