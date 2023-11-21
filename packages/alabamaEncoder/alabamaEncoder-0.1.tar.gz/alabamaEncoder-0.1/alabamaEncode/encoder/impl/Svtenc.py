import os.path
from typing import List

from alabamaEncode.core.bin_utils import get_binary
from alabamaEncode.core.cli_executor import run_cli
from alabamaEncode.encoder.encoder import Encoder
from alabamaEncode.encoder.rate_dist import EncoderRateDistribution


class AvifEncoderSvtenc:
    """
    AVIF Encoder but SvtAv1 inside ffmpeg.
    """

    def __init__(self, **kwargs):
        self.DEFAULT_PARAMS = {
            "vf": " ",
            "grain_synth": 0,
            "speed": 3,
            "bit_depth": 8,
            "crf": 13,
            "passes": 1,
            "threads": 1,
        }

        self.params = {**self.DEFAULT_PARAMS, **kwargs}

    def get_params(self):
        return self.params

    def update(self, **kwargs):
        self.params = {**self.params, **kwargs}

    def get_encode_commands(self) -> str:
        if not self.params["output_path"].endswith(".avif"):
            raise Exception("FATAL: output_path must end with .avif")

        if self.params["bit_depth"] not in (8, 10):
            raise Exception("FATAL: bit must be 8 or 10")

        pix_fmt = "yuv420p" if self.params["bit_depth"] == 8 else "yuv420p10le"

        ratebit = (
            f"-b:v {self.params['bitrate']}k"
            if self.params["bitrate"] is not None and self.params["bitrate"] != -1
            else f"-crf {self.params['crf']}"
        )

        return (
            f'{get_binary("ffmpeg")} -hide_banner -y -i "{self.params["in_path"]}" {self.params["vf"]} '
            f"-c:v libsvtav1 {ratebit} "
            f'-svtav1-params tune=0:lp={self.params["threads"]}:film-grain={self.params["grain_synth"]}'
            f' -preset {self.params["speed"]} -pix_fmt {pix_fmt} "{self.params["output_path"]}"'
        )

    def run(self):
        out = run_cli(self.get_encode_commands()).get_output()
        if (
            not os.path.exists(self.params["output_path"])
            or os.path.getsize(self.params["output_path"]) < 1
        ):
            print(self.get_encode_commands())
            raise Exception(
                f"FATAL: SVTENC ({self.get_encode_commands()}) FAILED with " + out
            )


class EncoderSvtenc(Encoder):
    def get_encode_commands(self) -> List[str]:
        if (
            self.keyint == -1 or self.keyint == -2
        ) and self.rate_distribution == EncoderRateDistribution.VBR:
            print("WARNING: keyint must be set for VBR, setting to 240")
            self.keyint = 240

        kommand = (
            f"{self.get_ffmpeg_pipe_command()} | "
            f"{get_binary('SvtAv1EncApp')}"
            f" -i stdin"
            f" --input-depth {self.bit_override}"
        )

        if self.override_flags == "" or self.override_flags is None:
            kommand += f" --keyint {self.keyint}"

            def crf_check():
                """
                validate crf fields
                """
                if self.crf is None or self.crf == -1:
                    raise Exception("FATAL: crf is not set")
                if self.crf > 63:
                    raise Exception("FATAL: crf must be less than 63")

            kommand += f" --color-primaries {self.color_primaries}"
            kommand += f" --transfer-characteristics {self.transfer_characteristics}"
            kommand += f" --matrix-coefficients {self.matrix_coefficients}"

            if self.hdr:
                kommand += f" --enable-hdr 1"
                kommand += f" --chroma-sample-position {self.chroma_sample_position}"
                kommand += (
                    f" --content-light "
                    f"{self.maximum_content_light_level},{self.maximum_frame_average_light_level}"
                )
                if self.svt_master_display != "":
                    kommand += f' --mastering-display "{self.svt_master_display}"'

            def bitrate_check():
                """
                validate bitrate fields
                """
                if self.bitrate is None or self.bitrate == -1:
                    raise Exception("FATAL: bitrate is not set")

            match self.rate_distribution:
                case EncoderRateDistribution.CQ:
                    if self.passes != 1:
                        print("WARNING: passes must be 1 for CQ, setting to 1")
                        self.passes = 1
                    crf_check()
                    kommand += f" --crf {self.crf} --rc 0"
                case EncoderRateDistribution.VBR:
                    bitrate_check()
                    kommand += f" --rc 1 --tbr {self.bitrate} --undershoot-pct 95 --overshoot-pct 10 "
                case EncoderRateDistribution.CQ_VBV:
                    bitrate_check()
                    crf_check()
                    kommand += f" --crf {self.crf} --mbr {self.bitrate}"
                case EncoderRateDistribution.VBR_VBV:
                    raise Exception("FATAL: VBR_VBV is not supported")

            kommand += f" --tune {self.svt_tune}"
            kommand += f" --bias-pct {self.svt_bias_pct}"
            kommand += f" --lp {self.threads}"

            kommand += f" --aq-mode {self.svt_aq_mode}"

            if self.svt_supperres_mode != 0:
                kommand += f" --superres-mode {self.svt_supperres_mode}"
                kommand += f" --superres-denom {self.svt_superres_denom}"
                kommand += f" --superres-kf-denom {self.svt_superres_kf_denom}"
                kommand += f" --superres-qthres {self.svt_superres_qthresh}"
                kommand += f" --superres-kf-qthres {self.svt_superres_kf_qthresh}"

            if self.svt_sframe_interval > 0:
                kommand += f" --sframe-dist {self.svt_sframe_interval}"
                kommand += f" --sframe-mode {self.svt_sframe_mode}"

            if 0 <= self.grain_synth <= 50:
                kommand += f" --film-grain {self.grain_synth}"

            kommand += f" --preset {self.speed}"
            kommand += f" --film-grain-denoise 0"
            if self.qm_enabled:
                kommand += f" --qm-min {self.qm_min}"
                kommand += f" --qm-max {self.qm_max}"
                kommand += " --enable-qm 1"
            else:
                kommand += " --enable-qm 0"

            kommand += f" --enable-tf {self.svt_tf}"

            if self.svt_open_gop and self.passes == 1:
                kommand += " --irefresh-type 1"

            if self.svt_overlay == 1:
                if self.passes == 1:
                    kommand += f" --enable-overlays {self.svt_overlay}"
                else:
                    print("WARNING: overlays only supported in 1 pass crf")
        else:
            kommand += self.override_flags

        stats_bit = ""

        if self.passes > 1:
            stats_bit = f"--stats {self.output_path}.stat"

        match self.passes:
            case 2:
                commands = [
                    f"{kommand} --pass 1 {stats_bit}",
                    f"{kommand} --pass 2 {stats_bit} -b {self.output_path}",
                    f"rm {self.output_path}.stat",
                ]
            case 1:
                commands = [f'{kommand} -b "{self.output_path}"']
            case 3:
                commands = [
                    f"{kommand} --pass 1 {stats_bit}",
                    f"{kommand} --pass 2 {stats_bit}",
                    f"{kommand} --pass 3 {stats_bit} -b {self.output_path}",
                    f"rm {self.output_path}.stat",
                ]
            case _:
                raise Exception(f"FATAL: invalid passes count {self.passes}")

        return commands

    def get_chunk_file_extension(self) -> str:
        return ".ivf"

    def get_version(self) -> str:
        # Svt[info]: -------------------------------------------
        # Svt[info]: SVT [version]:	SVT-AV1 Encoder Lib v1.7.0-2-g09df835
        o = run_cli(get_binary("SvtAv1EncApp")).get_output()
        return o.split("\n")[1].split(" ")[-1]
