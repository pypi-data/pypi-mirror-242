from typing import Callable

from sonusai.mixture import ClassCount
from sonusai.mixture import MixtureDatabase


def print_mixture_details(mixdb: MixtureDatabase,
                          mixid: int = None,
                          desc_len: int = 1,
                          print_fn: Callable = print) -> None:
    import numpy as np

    from sonusai import SonusAIError
    from sonusai.mixture import SAMPLE_RATE
    from sonusai.utils import seconds_to_hms

    if mixid is not None:
        if 0 < mixid >= mixdb.num_mixtures:
            raise SonusAIError(f'Given mixid is outside valid range of 0:{mixdb.num_mixtures - 1}.')

        print_fn(f'Mixture {mixid} details')
        mixture = mixdb.mixtures[mixid]
        targets = [mixdb.targets[idx] for idx in mixture.target_id]
        target_augmentations = [mixdb.target_augmentations[idx] for idx in mixture.target_augmentation_id]
        noise = mixdb.noises[mixture.noise_id]
        for t_idx, target in enumerate(targets):
            print_fn(f'  Target {t_idx}')
            print_fn(f'{"    Name":{desc_len}} {target.name}')
            print_fn(f'{"    Duration":{desc_len}} {seconds_to_hms(target.duration)}')
            for ts_idx, truth_setting in enumerate(target.truth_settings):
                print_fn(f'    Truth setting {ts_idx}')
                print_fn(f'{"      Index":{desc_len}} {truth_setting.index}')
                print_fn(f'{"      Function":{desc_len}} {truth_setting.function}')
                print_fn(f'{"      Config":{desc_len}} {truth_setting.config}')
            print_fn(f'{"    Augmentation":{desc_len}} {target_augmentations[t_idx]}')
        print_fn(f'{"  Samples":{desc_len}} {mixture.samples}')
        print_fn(f'{"  Feature frames":{desc_len}} {mixdb.mixture_feature_frames(mixid)}')
        print_fn(f'{"  Noise file":{desc_len}} {noise.name}')
        noise_offset_percent = int(np.round(100 * mixture.noise_offset / float(noise.duration * SAMPLE_RATE)))
        print_fn(f'{"  Noise offset":{desc_len}} {mixture.noise_offset} samples ({noise_offset_percent}%)')
        print_fn(f'{"  SNR":{desc_len}} {mixture.snr} dB{" (random)" if mixture.random_snr else ""}')
        print_fn(f'{"  Target gain":{desc_len}} {mixture.target_gain}')
        print_fn(f'{"  Target SNR gain":{desc_len}} {mixture.target_snr_gain}')
        print_fn(f'{"  Noise SNR gain":{desc_len}} {mixture.noise_snr_gain}')
        print_fn('')


def print_class_count(class_count: ClassCount,
                      length: int,
                      print_fn: Callable = print,
                      all_class_counts: bool = False) -> None:
    from sonusai.utils import max_text_width

    print_fn(f'Class count:')
    idx_len = max_text_width(len(class_count))
    for idx, count in enumerate(class_count):
        if all_class_counts or count > 0:
            desc = f'  class {idx + 1:{idx_len}}'
            print_fn(f'{desc:{length}} {count}')
