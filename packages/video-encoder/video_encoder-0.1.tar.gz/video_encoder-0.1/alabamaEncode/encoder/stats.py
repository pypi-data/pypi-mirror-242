import json

from alabamaEncode.metrics.vmaf.result import VmafResult


class EncodeStats:
    """
    Stats class for encoders
    """

    def __init__(
        self,
        time_encoding: int = -1,
        bitrate: int = -1,
        vmaf: float = -1,
        ssim: float = -1,
        size: int = -1,
        total_fps: int = -1,
        target_miss_proc: int = -1,
        rate_search_time: int = -1,
        chunk_index: int = -1,
        vmaf_percentile_1: float = -1,
        vmaf_percentile_5: float = -1,
        vmaf_percentile_10: float = -1,
        vmaf_percentile_25: float = -1,
        vmaf_percentile_50: float = -1,
        vmaf_avg: float = -1,
        basename: str = "",
        version: str = "",
        vmaf_result: VmafResult = None,
    ):
        self.time_encoding = time_encoding
        self.bitrate = bitrate
        self.vmaf = vmaf
        self.ssim = ssim
        self.size = size
        self.total_fps = total_fps
        self.target_miss_proc = target_miss_proc
        self.rate_search_time = rate_search_time
        self.chunk_index = chunk_index
        self.vmaf_percentile_1 = vmaf_percentile_1
        self.vmaf_percentile_5 = vmaf_percentile_5
        self.vmaf_percentile_10 = vmaf_percentile_10
        self.vmaf_percentile_25 = vmaf_percentile_25
        self.vmaf_percentile_50 = vmaf_percentile_50
        self.vmaf_avg = vmaf_avg
        self.basename = basename
        self.version = version
        self.vmaf_result = vmaf_result

    def get_dict(self):
        stats = {
            "time_encoding": self.time_encoding,
            "bitrate": self.bitrate,
            "vmaf": self.vmaf,
            "ssim": self.ssim,
            "size": self.size,
            "total_fps": self.total_fps,
            "target_miss_proc": self.target_miss_proc,
            "rate_search_time": self.rate_search_time,
            "chunk_index": self.chunk_index,
            "vmaf_percentile_1": self.vmaf_percentile_1,
            "vmaf_percentile_5": self.vmaf_percentile_5,
            "vmaf_percentile_10": self.vmaf_percentile_10,
            "vmaf_percentile_25": self.vmaf_percentile_25,
            "vmaf_percentile_50": self.vmaf_percentile_50,
            "vmaf_avg": self.vmaf_avg,
            "basename": self.basename,
            "version": self.version,
        }
        return stats

    def save(self, path):
        """
        Save stats to a file
        :param path: json file path
        :return: nun
        """
        with open(path, "w") as f:
            json.dump(self.get_dict(), f)

    def __str__(self):
        return str(self.__dict__)
