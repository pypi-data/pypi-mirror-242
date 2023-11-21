import pandas as pd


from vembed import calculate_similarities, plot_similarities


import unittest
import os


class TestSimilarity(unittest.TestCase):
    """
    @Test
    - Tests the calculate_similarities function to convert a String to an Embedding
    """

    def test_calculate_similarities(self):
        queries = ["What is the capital of France?", "How is the weather today?"]
        data = [
            "Paris is the capital of France.",
            "The weather is sunny.",
            "Berlin is the capital of Germany.",
            "It is raining in Berlin.",
        ]

        cos_df, dot_df = calculate_similarities(queries, data, sorted=True)

        self.assertIsNotNone(cos_df)
        self.assertIsNotNone(dot_df)


class TestPlotting(unittest.TestCase):
    """
    @Test
    - Tests the plot_similarities package to visualize the similarities for Entities
    """

    def test_plot_similarities(self):
        queries = ["Test Query 1", "Test Query 2"]
        data = ["Data 1", "Data 2", "Data 3"]
        cos_df, dot_df = calculate_similarities(queries, data)

        try:
            plot_similarities(cos_df, dot_df)
        except Exception as e:
            self.fail(f"plot_similarities raised an exception: {e}")

    def test_similarity_plot_creation(self):
        queries = ["Query 1", "Query 2"]
        data = ["Data 1", "Data 2", "Data 3"]
        cos_df, dot_df = calculate_similarities(queries, data)

        plot_file = "test_plot.png"
        plot_similarities(cos_df, dot_df, save_path=plot_file)

        self.assertTrue(os.path.exists(plot_file))
        if os.path.exists(plot_file):
            os.remove(plot_file)

    def test_relevant_plot_similarities(self):
        customer_feedback = [
            "Loved the recent update",
            "The app is user-friendly",
            "Facing issues after the update",
            "The new interface is great",
        ]
        themes = [
            "positive feedback",
            "negative feedback",
            "app interface",
            "app functionality",
        ]

        cos_df, dot_df = calculate_similarities(customer_feedback, themes)
        plot_file = "customer_feedback_similarity.png"
        plot_similarities(cos_df, dot_df, save_path=plot_file)

        self.assertTrue(os.path.exists(plot_file))
        if os.path.exists(plot_file):
            os.remove(plot_file)


if __name__ == "__main__":
    unittest.main()
