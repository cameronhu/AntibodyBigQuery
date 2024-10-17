import sys

sys.path.insert(0, "/home/cameronhu/oas_onboarding/utils")
from timing_decorator import timing_decorator

from transform.batch import Batch

from const_directories import *

if __name__ == "__main__":
    max_batch_size = 1 * 1024 * 1024 * 1024  # 1 GB
    batch_generator = Batch(UNPAIRED_HEAVY_DIR, max_batch_size)
    timed_generate_batches = timing_decorator(batch_generator.generate_batches)
    timed_generate_batches()

    batches = batch_generator.get_batches()

    # Output the batches
    for i, batch in enumerate(batches):
        print(f"Batch {i + 1}:")
        for file in batch:
            print(f"  {file}")
