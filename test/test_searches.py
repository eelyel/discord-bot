from unittest.mock import patch
from searches import NO_RESULTS_FOUND_MESSAGE
import searches
import unittest


class TestSearches(unittest.TestCase):

    def setUp(self):
        patch('searches.logger', auto_spec=True).start()

    @patch('searches.os', auto_spec=True)
    @patch('searches.requests', auto_spec=True)
    def test_google_search_will_return_search_items_when_given_search_parameters(self, mock_requests, _):
        expected_return = 123
        mock_requests.get().json.return_value = {
            'items': expected_return,
            'searchInformation': {
                'totalResults': 1
            }
        }

        output = searches.google_search(None, None, "")

        self.assertEqual(expected_return, output)

    @patch('searches.os', auto_spec=True)
    @patch('searches.requests', auto_spec=True)
    def test_google_search_will_return_empty_list_when_error_occurs(self, mock_requests, _):
        mock_requests.get().json.return_value = {'error': None}

        output = searches.google_search(None, None, "")

        self.assertFalse(output)

    @patch('searches.google_search', auto_spec=True)
    def test_search_will_return_no_results_found_when_google_search_returns_no_result(self, mock_google_search):
        mock_google_search.return_value = []

        output = searches.search(None, [], [], None)

        self.assertEqual(NO_RESULTS_FOUND_MESSAGE, output)

    @patch('searches.discord', auto_spec=True)
    @patch('searches.google_search', auto_spec=True)
    def test_search_will_return_embed_response_with_google_search_result_when_google_search_returns_some_result(self, mock_google_search, discord):
        test_title = 'Test title'
        test_snippet = 'Test snippet'
        test_link = 'Test link'
        mock_google_search.return_value = [{
            'title': test_title,
            'snippet': test_snippet,
            'link': test_link,
        }]
        discord.Embed.side_effect = lambda title, description: description

        output = searches.search(None, [], [], None)

        self.assertEqual(f"**{test_title}**\n{test_snippet}\n{test_link}\n\n", output)

    @patch('searches.google_search', auto_spec=True)
    def test_search_will_call_google_search_with_specified_num_result_when_num_results_specified_in_arguments(self, mock_google_search):
        searches.search(None, {'1'}, [], None)

        mock_google_search.assert_called_with('', 1, None)

    @patch('searches.randint', auto_spec=True)
    @patch('searches.google_search', auto_spec=True)
    def test_search_will_call_google_search_with_additional_scp_input_when_scp_num_specified_in_arguments(self, mock_google_search, randint):
        randint.return_value = 1001

        searches.search(None, {'r'}, [], None)

        mock_google_search.assert_called_with('1001', 3, None)
