from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
from urllib.error import URLError
from ruamel.yaml import YAMLError
import logging

from .utils import (
    fetch_contributors_yaml,
    get_recent_contributors,
    generate_github_avatar_url,
    generate_github_profile_url,
    ContributorDataError,
    fetch_packages_yaml,
    get_recent_packages,
    PackageDataError
)

# Disable logging during tests for cleaner output
logging.disable(logging.CRITICAL)


class ContributorYAMLParsingTests(TestCase):
    """Test cases for contributor YAML parsing functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.sample_contributors = [
            {
                'name': 'John Doe',
                'github_username': 'johndoe',
                'github_image_id': 12345,
                'bio': 'Test contributor',
                'organization': 'Test Org',
                'date_added': '2024-01-01'
            },
            {
                'name': 'Jane Smith',
                'github_username': 'janesmith',
                'github_image_id': 67890,
                'bio': 'Another test contributor',
                'organization': 'Another Org',
                'date_added': '2024-01-02'
            },
            {
                'github_username': 'Philip N.',
                'github_image_id': 11111,
                'bio': 'Contributor without name',
                'date_added': '2024-01-03'
            }
        ]

    @patch('core.utils.urlopen')
    @patch('core.utils.yaml.load')
    def test_fetch_contributors_yaml_success(self, mock_yaml_load, mock_urlopen):
        """Test successful fetching of contributors YAML."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.read.return_value.decode.return_value = 'yaml content'
        mock_urlopen.return_value.__enter__.return_value = mock_response
        mock_yaml_load.return_value = self.sample_contributors

        result = fetch_contributors_yaml()

        self.assertEqual(result, self.sample_contributors)
        mock_urlopen.assert_called_once()
        mock_yaml_load.assert_called_once_with('yaml content')

    @patch('core.utils.urlopen')
    def test_fetch_contributors_yaml_custom_url(self, mock_urlopen):
        """Test fetching contributors with custom URL."""
        custom_url = 'https://example.com/custom.yml'
        mock_response = MagicMock()
        mock_response.read.return_value.decode.return_value = '[]'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        with patch('core.utils.yaml.load') as mock_yaml_load:
            mock_yaml_load.return_value = []
            fetch_contributors_yaml(custom_url)

        mock_urlopen.assert_called_once_with(custom_url)

    @patch('core.utils.urlopen')
    def test_fetch_contributors_yaml_network_error(self, mock_urlopen):
        """Test handling of network errors."""
        mock_urlopen.side_effect = URLError('Network error')

        with self.assertRaises(ContributorDataError) as context:
            fetch_contributors_yaml()

        self.assertIn('Network error', str(context.exception))

    @patch('core.utils.urlopen')
    @patch('core.utils.yaml.load')
    def test_fetch_contributors_yaml_parse_error(self, mock_yaml_load, mock_urlopen):
        """Test handling of YAML parsing errors."""
        mock_response = MagicMock()
        mock_response.read.return_value.decode.return_value = 'invalid yaml'
        mock_urlopen.return_value.__enter__.return_value = mock_response
        mock_yaml_load.side_effect = YAMLError('YAML parse error')

        with self.assertRaises(ContributorDataError) as context:
            fetch_contributors_yaml()

        self.assertIn('YAML parsing error', str(context.exception))

    @patch('core.utils.urlopen')
    @patch('core.utils.yaml.load')
    def test_fetch_contributors_yaml_invalid_data_type(self, mock_yaml_load, mock_urlopen):
        """Test handling of invalid data type (not a list)."""
        mock_response = MagicMock()
        mock_response.read.return_value.decode.return_value = 'yaml content'
        mock_urlopen.return_value.__enter__.return_value = mock_response
        mock_yaml_load.return_value = {'not': 'a list'}

        with self.assertRaises(ContributorDataError) as context:
            fetch_contributors_yaml()

        self.assertIn('should be a list', str(context.exception))

    @patch('core.utils.fetch_contributors_yaml')
    def test_get_recent_contributors_success(self, mock_fetch):
        """Test successful retrieval of recent contributors."""
        mock_fetch.return_value = self.sample_contributors

        result = get_recent_contributors(2)

        # Should return reversed list (most recent first) limited to 2
        expected = list(reversed(self.sample_contributors))[:2]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 2)

    @patch('core.utils.fetch_contributors_yaml')
    def test_get_recent_contributors_default_count(self, mock_fetch):
        """Test default count of 4 contributors."""
        mock_fetch.return_value = self.sample_contributors

        result = get_recent_contributors()

        # Should return all 3 contributors (less than default 4)
        self.assertEqual(len(result), 3)

    @patch('core.utils.fetch_contributors_yaml')
    def test_get_recent_contributors_fetch_error(self, mock_fetch):
        """Test handling of fetch error."""
        mock_fetch.side_effect = ContributorDataError('Fetch failed')

        result = get_recent_contributors()

        self.assertEqual(result, [])

    @patch('core.utils.fetch_contributors_yaml')
    def test_get_recent_contributors_unexpected_error(self, mock_fetch):
        """Test handling of unexpected errors."""
        mock_fetch.side_effect = ValueError('Unexpected error')

        result = get_recent_contributors()

        self.assertEqual(result, [])


class UtilityFunctionTests(TestCase):
    """Test cases for utility functions."""

    def test_generate_github_avatar_url(self):
        """Test GitHub avatar URL generation."""
        image_id = 12345
        expected_url = f'https://avatars.githubusercontent.com/u/{image_id}?s=400&v=4'
        
        result = generate_github_avatar_url(image_id)
        
        self.assertEqual(result, expected_url)

    def test_generate_github_profile_url(self):
        """Test GitHub profile URL generation."""
        username = 'johndoe'
        expected_url = f'https://github.com/{username}'
        
        result = generate_github_profile_url(username)
        
        self.assertEqual(result, expected_url)


class HomeViewIntegrationTests(TestCase):
    """Test cases for view integration with contributor data."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = Client()
        self.sample_contributors = [
            {
                'name': 'John Doe',
                'github_username': 'johndoe',
                'github_image_id': 12345,
                'bio': 'Test contributor'
            },
            {
                'github_username': 'janesmith',
                'github_image_id': 67890
            }
        ]

    @patch('core.views.get_recent_contributors')
    def test_home_view_with_contributors(self, mock_get_contributors):
        """Test home view with contributor data."""
        mock_get_contributors.return_value = self.sample_contributors

        response = self.client.get(reverse('core:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
        self.assertContains(response, '@janesmith')
        self.assertIn('recent_contributors', response.context)
        self.assertEqual(len(response.context['recent_contributors']), 2)

    @patch('core.views.get_recent_contributors')
    def test_home_view_with_contributor_data_enhancement(self, mock_get_contributors):
        """Test that contributor data is properly enhanced in view."""
        mock_get_contributors.return_value = self.sample_contributors

        response = self.client.get(reverse('core:home'))

        contributors = response.context['recent_contributors']
        
        # Check first contributor (has name)
        first_contributor = contributors[0]
        self.assertIn('github_avatar_url', first_contributor)
        self.assertIn('github_profile_url', first_contributor)
        self.assertIn('display_name', first_contributor)
        self.assertEqual(first_contributor['display_name'], 'John Doe')
        
        # Check second contributor (no name)
        second_contributor = contributors[1]
        self.assertEqual(second_contributor['display_name'], '@janesmith')

    @patch('core.views.get_recent_contributors')
    def test_home_view_with_no_contributors(self, mock_get_contributors):
        """Test home view when no contributors are returned."""
        mock_get_contributors.return_value = []

        response = self.client.get(reverse('core:home'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('recent_contributors', response.context)
        self.assertEqual(len(response.context['recent_contributors']), 0)

    @patch('core.views.get_recent_contributors')
    def test_home_view_contributor_avatar_url_generation(self, mock_get_contributors):
        """Test that avatar URLs are correctly generated."""
        mock_get_contributors.return_value = self.sample_contributors

        response = self.client.get(reverse('core:home'))

        contributors = response.context['recent_contributors']
        first_contributor = contributors[0]
        
        expected_avatar_url = 'https://avatars.githubusercontent.com/u/12345?s=400&v=4'
        self.assertEqual(first_contributor['github_avatar_url'], expected_avatar_url)

    @patch('core.views.get_recent_contributors')
    def test_home_view_contributor_profile_url_generation(self, mock_get_contributors):
        """Test that profile URLs are correctly generated."""
        mock_get_contributors.return_value = self.sample_contributors

        response = self.client.get(reverse('core:home'))

        contributors = response.context['recent_contributors']
        
        for contributor in contributors:
            expected_profile_url = f"https://github.com/{contributor['github_username']}"
            self.assertEqual(contributor['github_profile_url'], expected_profile_url)


class PackageYAMLParsingTests(TestCase):
    """Test cases for package YAML parsing functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.sample_packages = [
            {
                'package_name': 'test-package-1',
                'package_description': 'A test package for testing',
                'date_accepted': '2024-01-15',
                'all_current_maintainers': [
                    {'name': 'Test User 1', 'github_username': 'testuser1'}
                ]
            },
            {
                'package_name': 'another-package',
                'package_description': 'Another test package',
                'date_accepted': '2024-01-10',
                'all_current_maintainers': [
                    {'name': 'Test User 2', 'github_username': 'testuser2'}
                ]
            },
            {
                'package_name': 'old-package',
                'package_description': 'An older test package',
                'date_accepted': '2024-01-05',
                'all_current_maintainers': [
                    {'name': 'Test User 3', 'github_username': 'testuser3'}
                ]
            }
        ]

    @patch('core.utils.urlopen')
    @patch('core.utils.yaml.load')
    def test_fetch_packages_yaml_success(self, mock_yaml_load, mock_urlopen):
        """Test successful fetching of packages YAML."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.read.return_value.decode.return_value = 'yaml content'
        mock_urlopen.return_value.__enter__.return_value = mock_response
        mock_yaml_load.return_value = self.sample_packages

        result = fetch_packages_yaml()

        self.assertEqual(result, self.sample_packages)
        mock_urlopen.assert_called_once()
        mock_yaml_load.assert_called_once_with('yaml content')

    @patch('core.utils.urlopen')
    def test_fetch_packages_yaml_custom_url(self, mock_urlopen):
        """Test fetching packages with custom URL."""
        custom_url = 'https://example.com/custom-packages.yml'
        mock_response = MagicMock()
        mock_response.read.return_value.decode.return_value = '[]'
        mock_urlopen.return_value.__enter__.return_value = mock_response

        with patch('core.utils.yaml.load') as mock_yaml_load:
            mock_yaml_load.return_value = []
            fetch_packages_yaml(custom_url)

        mock_urlopen.assert_called_once_with(custom_url)

    @patch('core.utils.urlopen')
    def test_fetch_packages_yaml_network_error(self, mock_urlopen):
        """Test handling of network errors."""
        mock_urlopen.side_effect = URLError('Network error')

        with self.assertRaises(PackageDataError) as context:
            fetch_packages_yaml()

        self.assertIn('Network error', str(context.exception))

    @patch('core.utils.urlopen')
    @patch('core.utils.yaml.load')
    def test_fetch_packages_yaml_parse_error(self, mock_yaml_load, mock_urlopen):
        """Test handling of YAML parsing errors."""
        mock_response = MagicMock()
        mock_response.read.return_value.decode.return_value = 'invalid yaml'
        mock_urlopen.return_value.__enter__.return_value = mock_response
        mock_yaml_load.side_effect = YAMLError('YAML parse error')

        with self.assertRaises(PackageDataError) as context:
            fetch_packages_yaml()

        self.assertIn('YAML parsing error', str(context.exception))

    @patch('core.utils.urlopen')
    @patch('core.utils.yaml.load')
    def test_fetch_packages_yaml_invalid_data_type(self, mock_yaml_load, mock_urlopen):
        """Test handling of invalid data type (not a list)."""
        mock_response = MagicMock()
        mock_response.read.return_value.decode.return_value = 'yaml content'
        mock_urlopen.return_value.__enter__.return_value = mock_response
        mock_yaml_load.return_value = {'not': 'a list'}

        with self.assertRaises(PackageDataError) as context:
            fetch_packages_yaml()

        self.assertIn('should be a list', str(context.exception))

    @patch('core.utils.fetch_packages_yaml')
    def test_get_recent_packages_success(self, mock_fetch):
        """Test successful retrieval of recent packages."""
        mock_fetch.return_value = self.sample_packages

        result = get_recent_packages(2)

        # Should return 2 most recent packages (sorted by date_accepted descending)
        expected = [
            self.sample_packages[0],  # 2024-01-15
            self.sample_packages[1]   # 2024-01-10
        ]
        self.assertEqual(result, expected)
        self.assertEqual(len(result), 2)

    @patch('core.utils.fetch_packages_yaml')
    def test_get_recent_packages_default_count(self, mock_fetch):
        """Test default count of 3 packages."""
        mock_fetch.return_value = self.sample_packages

        result = get_recent_packages()

        # Should return all 3 packages (equals default of 3)
        self.assertEqual(len(result), 3)
        # Verify they're sorted by date_accepted descending
        self.assertEqual(result[0]['date_accepted'], '2024-01-15')
        self.assertEqual(result[1]['date_accepted'], '2024-01-10')
        self.assertEqual(result[2]['date_accepted'], '2024-01-05')

    @patch('core.utils.fetch_packages_yaml')
    def test_get_recent_packages_fetch_error(self, mock_fetch):
        """Test handling of fetch error."""
        mock_fetch.side_effect = PackageDataError('Fetch failed')

        result = get_recent_packages()

        self.assertEqual(result, [])

    @patch('core.utils.fetch_packages_yaml')
    def test_get_recent_packages_unexpected_error(self, mock_fetch):
        """Test handling of unexpected errors."""
        mock_fetch.side_effect = ValueError('Unexpected error')

        result = get_recent_packages()

        self.assertEqual(result, [])


class PackageViewIntegrationTests(TestCase):
    """Test cases for view integration with package data."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = Client()
        self.sample_packages = [
            {
                'package_name': 'test-package',
                'package_description': 'A test package',
                'date_accepted': '2024-01-15',
                'all_current_maintainers': [
                    {'name': 'Test User', 'github_username': 'testuser'}
                ]
            },
            {
                'package_name': 'another-package',
                'package_description': 'Another package',
                'date_accepted': '2024-01-10',
                'all_current_maintainers': [
                    {'name': 'User 2', 'github_username': 'user2'}
                ]
            }
        ]

    @patch('core.views.get_recent_packages')
    def test_home_view_with_packages(self, mock_get_packages):
        """Test home view with package data."""
        mock_get_packages.return_value = self.sample_packages

        response = self.client.get(reverse('core:home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test-package')
        self.assertContains(response, 'another-package')
        self.assertIn('recent_packages', response.context)
        self.assertEqual(len(response.context['recent_packages']), 2)

    @patch('core.views.get_recent_packages')
    def test_home_view_with_no_packages(self, mock_get_packages):
        """Test home view when no packages are returned."""
        mock_get_packages.return_value = []

        response = self.client.get(reverse('core:home'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('recent_packages', response.context)
        self.assertEqual(len(response.context['recent_packages']), 0)
