import random
from pathlib import Path
from typing import Union, List

from torch.nn.utils.rnn import pad_sequence

from ..core.transforms_interface import BaseWaveformTransform, EmptyPathException
from ..utils.convolution import convolve
from ..utils.file import find_audio_files
from ..utils.io import Audio


class ApplyImpulseResponse(BaseWaveformTransform):
    """
    Convolve the given audio with impulse responses.
    """

    # Note: This transform has only partial support for multichannel audio. IRs that are not
    # mono get mixed down to mono before they are convolved with all channels in the input.
    supports_multichannel = True
    requires_sample_rate = True

    def __init__(
        self,
        ir_paths: Union[List[Path], List[str], Path, str],
        convolve_mode: str = "full",
        mode: str = "per_example",
        p: float = 0.5,
        p_mode: str = None,
        sample_rate: int = None,
    ):
        """

        :param ir_paths: Either a path to a folder with audio files or a list of paths to audio files.
        :param convolve_mode:
        :param mode:
        :param p:
        :param p_mode:
        :param sample_rate:
        """

        super().__init__(mode, p, p_mode, sample_rate)

        if isinstance(ir_paths, (list, tuple, set)):
            # TODO: check that one can read audio files
            self.ir_paths = list(ir_paths)
        else:
            self.ir_paths = find_audio_files(ir_paths)

        if sample_rate is not None:
            self.audio = Audio(sample_rate=sample_rate, mono=True)

        if len(self.ir_paths) == 0:
            raise EmptyPathException("There are no supported audio files found.")

        self.convolve_mode = convolve_mode

    def randomize_parameters(self, selected_samples, sample_rate: int = None):

        batch_size, _, _ = selected_samples.shape

        audio = self.audio if hasattr(self, "audio") else Audio(sample_rate, mono=True)

        self.transform_parameters["ir"] = pad_sequence(
            [
                audio(ir_path).transpose(0, 1)
                for ir_path in random.choices(self.ir_paths, k=batch_size)
            ],
            batch_first=True,
            padding_value=0.0,
        ).transpose(1, 2)

    def apply_transform(self, selected_samples, sample_rate: int = None):

        batch_size, num_channels, num_samples = selected_samples.shape

        # (batch_size, max_ir_length, 1)
        ir = self.transform_parameters["ir"].to(selected_samples.device)

        convolved_samples = convolve(
            selected_samples, ir.expand(-1, num_channels, -1), mode=self.convolve_mode
        )

        return convolved_samples[..., :num_samples]
