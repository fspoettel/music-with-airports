import argparse
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import sys
import time
import mpv

def parse_args():
  parser = argparse.ArgumentParser(description='listen to airport radio chatter and music simultaneously via mpv')
  parser.add_argument('-a', metavar="airport", default="rjtt_app_dep", help='code of a liveatc.net feed (e.g. rjtt_app_dep). See README for instructions on how to find these')
  parser.add_argument('url', help='url that can be played by `mpv` (e.g. link to a YouTube playlist)')
  return parser.parse_args()

class Player:
  is_stopped = False

  def play(self, url):
    print("Playing: {}".format(url))
    player = mpv.MPV(video=False, input_default_bindings=False, ytdl=True)
    player.play(url)

    try:
      while not self.is_stopped:
        # see: https://git.io/JJNFW
        if player._get_property("idle-active"):
          self.stop()
        else:
          time.sleep(1)

    except mpv.ShutdownError:
      raise
    except:
      pass

    if not player.core_shutdown:
      player.terminate()
      print("Stopped: {}".format(url))

    player.wait_for_shutdown()

  def stop(self):
    if not self.is_stopped:
      self.is_stopped = True

  def start(self):
    args = parse_args()

    print("ATC feeds are provided by https://www.liveatc.net")

    with ThreadPoolExecutor(max_workers=2) as executor:
      playback_futures = [
        executor.submit(self.play, args.url),
        executor.submit(self.play, "https://www.liveatc.net/play/{}.pls".format(args.a))
      ]

      try:
        wait(playback_futures, return_when=FIRST_COMPLETED)
        self.stop()
      except KeyboardInterrupt:
        self.stop()
      except:
        self.stop()
        raise

def main():
  player = Player()
  player.start()

if __name__ == "__main__":
  main()
