#!/usr/bin/env python3
import asyncio, telnetlib3
import concurrent.futures
import os, random, sys
from subprocess import Popen, PIPE

dir = '/usr/share/video'

def play(writer):
    rows = writer.get_extra_info('rows')
    cols = writer.get_extra_info('cols')
    video_file = random.choice(os.listdir(dir))
    mpv = [
        '/usr/bin/mpv',
        '--vo=tct',
        '--vo-tct-width={}'.format(cols),
        '--vo-tct-height={}'.format(rows),
        '--ao=null',
        dir + '/' + video_file
    ]
    with Popen(mpv, stdout=PIPE, stdin=PIPE, stderr=PIPE) as p:
        for line in p.stdout:
            try:
                writer.write(line.decode('utf-8'))
            except UnicodeEncodeError:
                # Just ignore any garbage data.
                pass
    writer.close()

@asyncio.coroutine
def shell(reader, writer):
    loop.run_in_executor(None, play, writer)

loop = asyncio.get_event_loop()
coro = telnetlib3.create_server(port=24, shell=shell, encoding='utf-8')
server = loop.run_until_complete(coro)

loop.run_until_complete(server.wait_closed())
