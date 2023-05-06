#!/usr/bin/env python -u

import asyncio
import logging
import string

import janus
import nltk
import speech_recognition as sr
from nltk.tokenize import word_tokenize

logger = logging.getLogger("computer")


def recognize_audio(r, source):
    # read the audio data from the default microphone
    print("Ready")
    try:
        audio_data = r.listen(source, timeout=5)
        # play(audio_data)
        # convert speech to text
        text = r.recognize_whisper(audio_data)
    except sr.WaitTimeoutError:
        text = ""
    return text


def listen(queue, args):
    r = sr.Recognizer()
    with sr.Microphone(sample_rate=8000) as source:
        r.adjust_for_ambient_noise(source, duration=5)
        while True:
            try:
                text = recognize_audio(r, source)
            except KeyboardInterrupt:
                return

            text = text.strip()
            text = text.lower()
            # remove all punctuation
            text = text.translate(str.maketrans("", "", string.punctuation))
            if text == "":
                continue

            print(f"You said '{text}'")

            queue.put(dict(text=text, tokens=nltk.pos_tag(word_tokenize(text))))


async def main(output_queue, args):
    queue = janus.Queue()

    loop = asyncio.get_event_loop()

    loop.run_in_executor(None, listen, queue.sync_q, args)

    while True:
        try:
            data = await queue.async_q.get()
            await output_queue.put(data)
        except KeyboardInterrupt:
            return


if __name__ == "__main__":

    class MockQueue:
        async def put(self, event):
            print(event)

    asyncio.run(main(MockQueue(), dict()))
