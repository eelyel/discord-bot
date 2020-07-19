from unittest.mock import patch
from searches import GOOGLE_SEARCH_ENGINE_IDS, NO_RESULTS_FOUND_MESSAGE
import searches
import unittest


@patch.dict(GOOGLE_SEARCH_ENGINE_IDS, {None: None}, clear=True)
class TestSearches(unittest.TestCase):
    @patch('searches.requests')
    def test_google_search_will_return_search_items_when_given_search_parameters(self, requests):
        expected_return = 123
        requests.get().json.return_value = {
            'items': expected_return,
            'searchInformation': {
                'totalResults': 1
            }
        }

        output = searches.google_search(None, None, None)

        self.assertEqual(expected_return, output)

    @patch('searches.requests')
    def test_google_search_will_return_empty_list_when_error_occurs(self, requests):
        requests.get().json.return_value = {'error': None}

        output = searches.google_search(None, None, None)

        self.assertFalse(output)

    @patch('searches.google_search')
    def test_search_will_return_no_results_found_when_google_search_returns_no_result(self, google_search):
        google_search.return_value = []

        output = searches.search(None, [], [], None)

        self.assertEqual(NO_RESULTS_FOUND_MESSAGE, output)

    @patch('searches.discord')
    @patch('searches.google_search')
    def test_search_will_return_embed_response_with_google_search_result_when_google_search_returns_some_result(self, google_search, discord):
        test_title = 'Test title'
        test_snippet = 'Test snippet'
        test_link = 'Test link'
        google_search.return_value = [{
            'title': test_title,
            'snippet': test_snippet,
            'link': test_link,
        }]
        discord.Embed.side_effect = lambda title, description: description

        output = searches.search(None, [], [], None)

        self.assertEqual(f"**{test_title}**\n{test_snippet}\n{test_link}\n\n", output)

    @patch('searches.google_search')
    def test_search_will_call_google_search_with_specified_num_result_when_num_results_specified_in_arguments(self, google_search):
        searches.search(None, {'1'}, [], None)

        google_search.assert_called_with('', 1, None)

    @patch('searches.randint')
    @patch('searches.google_search')
    def test_search_will_call_google_search_with_additional_scp_input_when_scp_num_specified_in_arguments(self, google_search, randint):
        randint.return_value = 1001

        searches.search(None, {'r'}, [], None)

        google_search.assert_called_with('1001', 3, None)
