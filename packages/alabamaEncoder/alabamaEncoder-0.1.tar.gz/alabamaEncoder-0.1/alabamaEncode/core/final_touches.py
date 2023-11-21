import os
import random

from torf import Torrent
from tqdm import tqdm

from alabamaEncode.core.bin_utils import get_binary
from alabamaEncode.core.cli_executor import run_cli
from alabamaEncode.core.ffmpeg import Ffmpeg
from alabamaEncode.core.path import PathAlabama


def print_stats(
    output_folder: str,
    output: str,
    input_file: str,
    grain_synth: int,
    title: str,
    tonemaped: bool,
    croped: bool,
    scaled: bool,
    cut_intro: bool,
    cut_credits: bool,
):
    # sum up all the time_encoding variables
    time_encoding = 0

    # remove old stat.txt
    result_file = f"{output_folder}/stat.txt"
    if os.path.exists(result_file):
        os.remove(result_file)

    def print_and_save(s: str):
        print(s)
        with open(result_file, "a") as stat_file:
            stat_file.write(s + "\n")

    print_and_save(f"Total encoding time across chunks: {time_encoding} seconds\n\n")

    total_bitrate = int(Ffmpeg.get_total_bitrate(PathAlabama(output))) / 1000

    print_and_save("\n\n")

    def sizeof_fmt(num, suffix="B"):
        for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
            if abs(num) < 1024.0:
                return f"{num:3.1f}{unit}{suffix}"
            num /= 1024.0
        return f"{num:.1f}Yi{suffix}"

    print("Encode finished message \n\n")

    print_and_save(f"## {title}")

    print_and_save(f"- total bitrate `{total_bitrate} kb/s`")
    print_and_save(f"- total size `{sizeof_fmt(os.path.getsize(output)).strip()}`")
    print_and_save(
        f"- length `{Ffmpeg.get_video_length(PathAlabama(output), True).split('.')[0]}`"
    )
    size_decrease = round(
        (os.path.getsize(output) - os.path.getsize(input_file))
        / (os.path.getsize(input_file))
        * 100,
        2,
    )
    print_and_save(
        f"- sause `{os.path.basename(input_file)}`, size `{sizeof_fmt(os.path.getsize(input_file))}`, size decrease "
        f"from source `{size_decrease}%`"
    )
    print_and_save(f"- grain synth `{grain_synth}`")

    string = ""

    if tonemaped:
        string += "tonemaped "
    if croped:
        string += " & croped "
    if scaled:
        string += " & scaled"

    print_and_save(f"- {string}")

    if cut_intro and cut_credits is False:
        print_and_save(f"- intro cut")
    elif cut_intro is False and cut_credits:
        print_and_save(f"- credits cut")
    elif cut_intro and cut_credits:
        print_and_save(f"- intro & credits cut")

    print_and_save("\n")
    print_and_save(
        f"https://autocompressor.net/av1?v=https://badidea.kokoniara.software/{os.path.basename(output)}&i= poster_url "
        f"&w={Ffmpeg.get_width(PathAlabama(output))}&h={Ffmpeg.get_height(PathAlabama(output))}"
    )
    print_and_save("\n")
    print_and_save("ALABAMAENCODES © 2024")

    print("\n\n Finished!")


def generate_previews(
    input_file: str, output_folder: str, num_previews: int, preview_length: int
):
    # get total video length
    # total_length =  get_video_lenght(input_file)
    total_length = Ffmpeg.get_video_length(PathAlabama(input_file))

    # create x number of offsets that are evenly spaced and fit in the video
    offsets = []
    # for i in range(num_previews):
    #     offsets.append(int(i * total_length / num_previews))

    # pick x randomly and evenly offseted offsets
    for i in range(num_previews):
        offsets.append(int(random.uniform(0, total_length)))

    for i, offset in tqdm(enumerate(offsets), desc="Generating previews"):
        run_cli(
            f'{get_binary("ffmpeg")} -y -ss {offset} -i "{input_file}" -t {preview_length} '
            f'-c copy "{output_folder}/preview_{i}.avif"'
        )


def create_torrent_file(video: str, encoder_name: str, output_folder: str):
    trackers = [
        "udp://tracker.opentrackr.org:1337/announce",
        "https://tracker2.ctix.cn:443/announce",
        "https://tracker1.520.jp:443/announce",
        "udp://opentracker.i2p.rocks:6969/announce",
        "udp://tracker.openbittorrent.com:6969/announce",
        "http://tracker.openbittorrent.com:80/announce",
        "udp://open.demonii.com:1337/announce",
        "udp://open.stealth.si:80/announce",
        "udp://exodus.desync.com:6969/announce",
        "udp://tracker.torrent.eu.org:451/announce",
        "udp://tracker.moeking.me:6969/announce",
        "udp://explodie.org:6969/announce",
        "udp://tracker.opentrackr.org:1337/announce",
        "http://tracker.openbittorrent.com:80/announce",
        "udp://opentracker.i2p.rocks:6969/announce",
        "udp://tracker.internetwarriors.net:1337/announce",
        "udp://tracker.leechers-paradise.org:6969/announce",
        "udp://coppersurfer.tk:6969/announce",
        "udp://tracker.zer0day.to:1337/announce",
    ]

    print("Creating torrent file")

    t = Torrent(path=video, trackers=trackers)
    t.comment = f"Encoded by {encoder_name}"

    t.private = False

    t.generate()

    if os.path.exists(os.path.join(output_folder, "torrent.torrent")):
        os.remove(os.path.join(output_folder, "torrent.torrent"))
    t.write(os.path.join(output_folder, "torrent.torrent"))
