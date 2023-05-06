#!/usr/bin/env python -u

import logging
import sys
import speech_recognition as sr
import time
import string
import asyncio
import nltk
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


async def main(queue, args):
    if args is None:
        args = sys.argv[1:]

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

            if text == "15 15 15 15 15 15 15":
                continue

            print(f"You said '{text}'")
            # ok = input("Is this correct? [y/n] ")
            # if ok == "n":
            #    continue

            await queue.put(dict(text=text, tokens=nltk.pos_tag(word_tokenize(text))))

            # generate_response(text)
            time.sleep(1)

    return 0


if __name__ == "__main__":

    class MockQueue:
        async def put(self, event):
            print(event)

    asyncio.run(main(MockQueue(), dict()))
