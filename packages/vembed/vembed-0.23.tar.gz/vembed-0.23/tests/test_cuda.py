# python -m unittest discover -s tests -v


import unittest
import torch

from vembed import string_to_embedding


class TestConverter(unittest.TestCase):
    def test_tensor(self):
        tensor = torch.tensor([1, 2, 3])

        # print(f"Type: {type(tensor)}, Device: {tensor.device}")

        # Move tensor to GPU (if available)
        if torch.cuda.is_available():
            gpu_tensor = tensor.to("cuda")
            print(f"Type: {type(gpu_tensor)}, Device: {gpu_tensor.device}")

        numpy_array = tensor.cpu().numpy()
        # print(f"Type: {type(numpy_array)}")

        self.assertIsNotNone(tensor)
        self.assertIsNotNone(numpy_array)

    def test_cuda_available(self):
        is_cuda_available = torch.cuda.is_available()
        # print(f"Is CUDA (GPU) available: {is_cuda_available}")

        # If CUDA is available, print the number of GPUs and the name of the first GPU
        if is_cuda_available:
            num_gpus = torch.cuda.device_count()
            gpu_name = torch.cuda.get_device_name(0)
            # print(f"Number of GPUs: {num_gpus}")
            # print(f"GPU Name: {gpu_name}")


if __name__ == "__main__":
    unittest.main()
