import os
import pickle
import time

import alabamaEncode.core
from alabamaEncode.adaptive.util import get_probe_file_base
from alabamaEncode.encoder.rate_dist import EncoderRateDistribution
from alabamaEncode.metrics.ssim.calc import get_video_ssim


def get_ideal_bitrate(
    chunk,
    config,
    convex_speed=10,
    show_rate_calc_log=False,
    clamp_complexity=True,
) -> int:
    """
    Gets the ideal bitrate for a chunk
    """

    rate_search_start = time.time()

    probe_file_base = get_probe_file_base(chunk.chunk_path)
    cache_filename = f"{probe_file_base}.complexity.speed{convex_speed}.pt"

    ideal_rate = None

    # check if we have already done this
    if os.path.exists(cache_filename):
        try:
            ideal_rate = pickle.load(open(cache_filename, "rb"))
        except:
            print("Error loading complexity cache file, recalculating")

    if not ideal_rate:
        encoder = config.get_encoder()

        test_probe_path = (
            f"{probe_file_base}complexity.probe.{encoder.get_chunk_file_extension()}"
        )

        encoder.update(
            speed=convex_speed,
            passes=1,
            temp_folder=config.temp_folder,
            chunk=chunk,
            grain_synth=0,
            current_scene_index=chunk.chunk_index,
            output_path=test_probe_path,
            threads=1,
            video_filters=config.video_filters,
            bitrate=config.bitrate,
            rate_distribution=EncoderRateDistribution.VBR,
        )

        alabamaEncode.execute_context.run(override_if_exists=False)

        try:
            (ssim, ssim_db) = get_video_ssim(
                test_probe_path, chunk, get_db=True, video_filters=config.video_filters
            )
        except Exception as e:
            print(f"Error calculating ssim for complexity rate estimation: {e}")
            # this happens when the scene is fully black, the best solution here is just setting the complexity to 0,
            # and since its all black anyway it won't matter
            ssim_db = config.ssim_db_target

        # Calculate the ratio between the target ssim dB and the current ssim dB
        ratio = 10 ** ((config.ssim_db_target - ssim_db) / 10)

        # Clamp the ratio to the complexity clamp
        if clamp_complexity:
            ratio = max(
                min(ratio, 1 + config.bitrate_overshoot), 1 - config.bitrate_undershoot
            )

        # Interpolate the ideal rate using the ratio
        ideal_rate = config.bitrate * ratio
        ideal_rate = int(ideal_rate)

        if show_rate_calc_log:
            print(
                f"{chunk.log_prefix()}===============\n"
                f"{chunk.log_prefix()} encode rate: {config.bitrate}k/s\n"
                f"{chunk.log_prefix()} ssim dB when using target bitrate: {ssim_db} (wanted: {config.ssim_db_target})\n"
                f"{chunk.log_prefix()} ratio = 10 ** (dB_target - dB) / 10 = {ratio}\n"
                f"{chunk.log_prefix()} ideal rate: max(min(encode_rate * ratio, upper_clamp), bottom_clamp) = {ideal_rate:.2f}k/s\n"
                f"{chunk.log_prefix()}==============="
            )

        try:
            pickle.dump(ideal_rate, open(cache_filename, "wb"))
        except:
            pass

    if ideal_rate == -1:
        raise Exception("ideal_rate is -1")

    config.log(
        f"{chunk.log_prefix()}rate search took: {int(time.time() - rate_search_start)}s, ideal bitrate: {ideal_rate}"
    )

    return int(ideal_rate)
