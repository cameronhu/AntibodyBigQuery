import os


class Batch:
    def __init__(self, directory: str, max_batch_size: int):
        self.directory = directory
        self.max_batch_size = max_batch_size
        self.batches = []

    def _get_file_sizes(self):
        """Return a list of (filename, size) tuples for all files in the directory."""
        file_sizes = []
        for filename in os.listdir(self.directory):
            file_path = os.path.join(self.directory, filename)
            if os.path.isfile(file_path):
                file_sizes.append((file_path, os.path.getsize(file_path)))
        return file_sizes

    def generate_batches(self):
        """Generate batches of filenames based on the maximum batch size."""
        file_sizes = self._get_file_sizes()
        current_batch = []
        current_batch_size = 0

        for file_path, size in file_sizes:
            if current_batch_size + size > self.max_batch_size:
                # If adding the current file exceeds the batch size, save the current batch
                self.batches.append(current_batch)
                # Start a new batch
                current_batch = []
                current_batch_size = 0

            # Add the current file to the batch
            current_batch.append(file_path)
            current_batch_size += size

        # Add the last batch if it contains files
        if current_batch:
            self.batches.append(current_batch)

    def get_batches(self):
        """Return the generated batches."""
        return self.batches
