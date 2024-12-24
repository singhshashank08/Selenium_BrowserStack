
# Selenium Web Scraping and BrowserStack Integration

This project demonstrates how to use Selenium for web scraping in combination with BrowserStack for cross-browser testing, and Google's Translation API to translate the scraped content. The application scrapes articles, translates titles, and analyzes repeated words.

## Features
- Web scraping with Selenium
- Cross-browser testing on BrowserStack
- Google Translation API integration
- Image downloading from scraped articles

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.x
- Selenium
- BrowserStack credentials
- Google Translation API key

### 1. Install Dependencies

You will need to install the necessary Python libraries:

```bash
pip install selenium requests
```

### 2. Set Up BrowserStack Credentials

Create a file named `credentials.py` and add your BrowserStack credentials:

```python
BROWSERSTACK_USERNAME = 'your_browserstack_username'
BROWSERSTACK_ACCESS_KEY = 'your_browserstack_access_key'
```

### 3. Set Up Google API Key

Obtain a Google Translation API key from the Google Cloud Console and add it to your project:

```python
TRANSLATION_API_KEY = 'your_google_api_key'
```

### 4. Running the Project

Run the project using the following command:

```bash
python main.py
```

### 5. Output

The script will print the following:

- Original Titles of articles
- Translated Titles
- Repeated Words Analysis

Additionally, images from the scraped articles will be downloaded to the project directory.

## Troubleshooting

- Ensure that all necessary dependencies are installed.
- Check if your BrowserStack credentials are correct.
- Make sure you have an active internet connection for API calls.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

