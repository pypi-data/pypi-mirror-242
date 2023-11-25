from setuptools import setup, find_packages

setup(
    name='best-buy-scraper',
    version='0.1.0',
    packages=find_packages(),
    author='Oxylabs',
    author_email='marketing@oxylabs.io',
    description="Extract exact prices, titles, reviews, and product descriptions with our Best Buy Scraper.",
    long_description="""# Best Buy Scraper


[![Oxylabs promo code](https://user-images.githubusercontent.com/129506779/250792357-8289e25e-9c36-4dc0-a5e2-2706db797bb5.png)](https://oxylabs.go2cloud.org/aff_c?offer_id=7&aff_id=877&url_id=112)


Ensure you stay ahead of your competitors with our real-time [Best Buy Scraper](https://oxy.yt/Baga). Aimed at effortlessly gathering data, it quickly delivers results. We’ve provided a brief guide below that shows precisely how the Best Buy Scraper functions with specific code examples that will help you understand and use the scraper hassle-free.

### How it works

You can get Best Buy results by providing your own URLs to our service. We can return the HTML of any Best Buy page you like.

#### Python code example

The example below illustrates how you can get an eBay product page result in HTML format.

```python
import requests
from pprint import pprint

# Structure payload.
payload = {
    'source': 'universal_ecommerce',
    'url': 'https://www.bestbuy.com/site/samsung-galaxy-z-flip4-128gb-unlocked-graphite/6512618.p?skuId=6512618',
    'geo_location': 'United States',
    'parse': True,
}

# Get response.
response = requests.request(
    'POST',
    'https://realtime.oxylabs.io/v1/queries',
    auth=('user', 'pass1'),
    json=payload,
)

# Instead of response with job status and results url, this will return the
# JSON response with the result.
pprint(response.json())
```

Find code examples for other programming languages [**here**](https://github.com/oxylabs/best-buy-scraper/tree/main/code%20examples)

#### Output Example

```json
{
    "results": [
        {
            "content": {
                "url": "https://www.bestbuy.com/site/samsung-galaxy-z-flip4-128gb-unlocked-graphite/6512618.p?skuId=6512618&intl=nosplash",
                "price": {
                    "price": 999.99,
                    "currency": "USD"
                },
                "title": "Samsung - Galaxy Z Flip4 128GB (Unlocked) - Graphite",
                "rating": {
                    "count": 0,
                    "score": 0
                },
                "product_id": "6512618",
                "is_sold_out": null,
                "parse_status_code": 12000,
                "additional_information": [
                    {
                        "name": "Model",
                        "value": "SM-F721UZAAXAA"
                    },
                    {
                        "name": "SKU",
                        "value": "6512618"
                    },
                    {
                        "name": "Release Date",
                        "value": "08/26/2022"
                    }
                ]
            },
            "created_at": "2022-08-18 14:00:57",
            "updated_at": "2022-08-18 14:01:01",
            "page": 1,
            "url": "https://www.bestbuy.com/site/samsung-galaxy-z-flip4-128gb-unlocked-graphite/6512618.p?skuId=6512618&intl=nosplash",
            "job_id": "6966031187999462401",
            "status_code": 200,
            "parser_type": "bestbuy_product"
        }
    ]
}
```

What is provided above shows the exact process of how you can extract necessary data effortlessly with Best Buy Scraper. Easily collect product information, ranging from reviews and prices to product descriptions and other features, thus allowing you to retain or gain a competitive advantage.

""",
    long_description_content_type='text/markdown',
    url='https://oxylabs.io/products/scraper-api/ecommerce/bestbuy',
    project_urls={
        'Documentation': 'https://developers.oxylabs.io/scraper-apis/e-commerce-scraper-api/best-buy',
        'Source': 'https://github.com/oxylabs/best-buy-scraper',
        'Bug Reports': 'https://github.com/oxylabs/best-buy-scraper/issues',
    },
    keywords='url-scraper, ecommerce-website, best-buy-scraper, best-buy, e-commerce-scraper-api, e-commerce-scraper,',
    license='MIT',

    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.6',
)









