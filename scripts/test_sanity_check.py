import sys

from transform.batch import Batch

from const_directories import *

if __name__ == "__main__":

    num_batches = 5

    max_batch_size = 1 * 1024 * 1024 * 1024  # 1 GB
    paired_batch = Batch(PAIRED_DIR, max_batch_size)
    unpaired_heavy_batch = Batch(UNPAIRED_HEAVY_DIR, max_batch_size)
    unpaired_light_batch = Batch(UNPAIRED_LIGHT_DIR, max_batch_size)

    # Generate batches
    paired_batch.generate_batches()
    unpaired_heavy_batch.generate_batches()
    unpaired_light_batch.generate_batches()

    # Splice batch list to num_batches parsed
    paired_batch_list = paired_batch.get_batches()[:num_batches]
    unpaired_heavy_batch_list = unpaired_heavy_batch.get_batches()[:num_batches]
    unpaired_light_batch_list = unpaired_light_batch.get_batches()[:num_batches]

    totalFiles = 0

    totalFiles += sum(len(sublist) for sublist in paired_batch_list)
    totalFiles += sum(len(sublist) for sublist in unpaired_heavy_batch_list)
    totalFiles += sum(len(sublist) for sublist in unpaired_light_batch_list)

    print(f"Total number of files processed and uploaded is: {totalFiles}")
