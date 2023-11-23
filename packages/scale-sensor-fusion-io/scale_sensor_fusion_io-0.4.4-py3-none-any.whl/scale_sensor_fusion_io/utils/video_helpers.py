import os
import numpy.typing as npt
import numpy as np
from typing import Any, Dict, List, Iterable, Optional, Union
from dataclasses import dataclass
from subprocess import Popen, PIPE
from tqdm import tqdm

import ffmpeg
from turbojpeg import TurboJPEG
import tempfile

turbo_jpeg = TurboJPEG()


DATA_DIR: str = (
    os.environ["DATA_DIR"] if "DATA_DIR" in os.environ else f'{os.environ["HOME"]}/data'
)


@dataclass
class VideoReader:
    video: Union[str, bytes]
    target_file_prefix: str
    cache_dir: str
    threads: Optional[int] = 0

    def __init__(
        self,
        video: Union[str, bytes],
        target_file_prefix: str,
        threads: Optional[int] = 0,
        cache_dir: Optional[str] = None,
    ) -> None:
        self.video = video
        self.target_file_prefix = target_file_prefix
        self.threads = threads
        self.cache_dir = self.cache_dir if cache_dir else tempfile.gettempdir()

        os.makedirs(self.cache_dir, exist_ok=True)

    def full_path_prefix(self) -> str:
        return f"{self.cache_dir}/{self.target_file_prefix}"

    def build_cmd(self, video_file: str) -> List[str]:
        params = [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel error",
            "-f mp4",
            "-i " + video_file,
            self.full_path_prefix() + "_%d.jpg",
        ]

        print(" ".join(params))

        return [item for param in params for item in param.split(" ", 1)]

    def load(self, frame_num: int) -> npt.NDArray[np.uint8]:
        image_file = f"{self.full_path_prefix()}_{frame_num+1}.jpg"

        # Note: I tried to pipe through stdin, but was running into all kinda of errors getting ffmpeg to dmux the raw bytes
        if not os.path.exists(image_file):
            video_file = tempfile.mktemp(suffix=".mp4")
            if isinstance(self.video, str):
                video_file = self.video
            else:
                with open(video_file, "wb") as fp:
                    fp.write(self.video)

            cmd = self.build_cmd(video_file)

            # start ffmpeg process
            process = Popen(cmd, stdin=PIPE)
            if process.stdin is None:
                raise ValueError("Failed to open ffmpeg process")

            # wait for process to finish
            process.wait()

        with open(image_file, "rb") as fd:
            return turbo_jpeg.decode(fd.read(), 0)


@dataclass
class VideoWriter:
    target_file: str
    fps: Optional[int] = 10
    threads: Optional[int] = 0
    crf: Optional[int] = 24
    show_progress: Optional[bool] = True
    count: int = 0

    def build_cmd(self) -> List[str]:
        params = [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel error",
            "-f image2pipe",
            f"-r {self.fps}",
            "-i -",
            "-vcodec libx264",
            "-x264-params keyint=2:scenecut=0",
            "-pix_fmt yuv420p",
            f"-crf {self.crf}",
            f"-r {self.fps}",
            f"-threads {self.threads}",
            "-preset fast",
            self.target_file,
        ]

        return [item for param in params for item in param.split(" ", 1)]

    def encode(self, images: Iterable[Union[str, bytes]]) -> None:
        cmd = self.build_cmd()

        # start ffmpeg process
        process = Popen(cmd, stdin=PIPE)
        if process.stdin is None:
            raise ValueError("Failed to open ffmpeg process")

        if self.show_progress:
            images = tqdm(images)

        # stream images to ffmpeg
        for image in images:
            if isinstance(image, str):
                with open(image, "rb") as fp:
                    image = fp.read()

            process.stdin.write(image)
        process.stdin.close()

        # wait for process to finish
        process.wait()

    def get_video(self) -> bytes:
        with open(self.target_file, "rb") as fp:
            return fp.read()

    def writeFrame(self, im: npt.NDArray) -> None:
        self.jpeg_bytes.append(turbo_jpeg.encode(im, quality=95))
        self.count += 1

    def __enter__(self) -> "VideoWriter":
        self.jpeg_bytes: List[bytes] = []
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
        if self.count > 0:
            self.encode(self.jpeg_bytes)


# Util function to generate a video from a list of images
def generate_video(
    image_files: List[str],
    target_file: str,
    fps: Optional[int] = 10,
    threads: Optional[int] = 0,
) -> None:
    encoder = VideoWriter(target_file, fps, threads)
    encoder.encode(image_files)


def write_audio_and_video(audio_file: str, video_file: str, output_file: str) -> None:
    if not os.path.isfile(audio_file) or not os.path.isfile(video_file):
        raise ValueError("Audio or video file does not exist")

    input_video = ffmpeg.input(video_file)
    input_audio = ffmpeg.input(audio_file)
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(
        output_file, loglevel="error"
    ).overwrite_output().run()
