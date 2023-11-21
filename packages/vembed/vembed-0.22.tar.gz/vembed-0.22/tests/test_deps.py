import unittest
import importlib.util


class TestDependencies(unittest.TestCase):
    def test_dependencies_installed(self):
        dependencies = ["sentence_transformers", "torch", "transformers"]
        for lib in dependencies:
            with self.subTest(lib=lib):
                self.assertTrue(
                    importlib.util.find_spec(lib) is not None, f"{lib} is not installed"
                )


if __name__ == "__main__":
    unittest.main()
