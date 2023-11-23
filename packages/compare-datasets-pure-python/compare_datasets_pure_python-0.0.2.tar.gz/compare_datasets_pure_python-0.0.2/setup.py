# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['compare_datasets_pure_python']

package_data = \
{'': ['*'], 'compare_datasets_pure_python': ['tests/*']}

install_requires = \
['Levenshtein>=0.23.0,<0.24.0',
 'jinja2>=3.1.2,<4.0.0',
 'pandas>=2.1.3,<3.0.0',
 'polars>=0.19.5,<0.20.0',
 'scipy>=1.11.4,<2.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'tqdm>=4.66.1,<5.0.0']

setup_kwargs = {
    'name': 'compare-datasets-pure-python',
    'version': '0.0.2',
    'description': 'The library that compares two dataframes',
    'long_description': '# Compare Dataframes\n\n## Description\nThis powerful Python library is designed to facilitate easy and efficient comparison of data frames.\n\n\n### Key Features\n- Universal Compatibility: The library is designed to work out of the box with data frames of any type, including pandas, polars, or Spark data frames. This flexibility allows you to use the library with your preferred data manipulation framework.\n\n- String Comparison: For string comparison, the library employs the Levenshtein distance algorithm. The Levenshtein distance is a string metric for measuring the difference between two sequences. The algorithm is used to identify the minimum number of single-character edits (insertions, deletions, or substitutions) required to change one word into the other.\n\n- Numeric Comparison: Numeric comparisons are conducted using the Euclidean distance between columns. This method is effective for identifying differences in numeric data, providing insights into variations between datasets.\n\n- Rust-Based Distance Functions: To achieve parallelized and fast performance at native speeds, the distance functions are implemented in Rust. This choice ensures that the library can handle large-scale data comparisons with efficiency. The comparison engine is built over the polars library, providing exceptional performance. The underlying design ensures that the library efficiently handles large datasets for quick and reliable comparisons.\n\n- User-friendly reporting: The library generates a detailed tabular report that provides a comprehensive overview of the differences between the two datasets. \n\n## Example Usage\n```python\nimport polars as pl\ndf = pl.DataFrame(\n    {\n        "a": [\'21-03-2022\', \'soccer\', \'cricket\'],\n        "b": ["21-03-2022", \'soccer\', "cricket"],\n        "c": [1, 2, 3],\n    }\n)\n\ndf1 = pl.DataFrame(\n    {\n        "a": [\'21-03-2022\', \'soccer\', \'cricket\', \'baseball\'],\n        "b": ["21-03-2022", \'sucker\', "cricket", \'man\'],\n        "c": [4, 2, 3, 4],\n        \n    }\n)\nfrom compare_datasets import Compare\ncompared = Compare(df, df1)\nprint(compared) # prints the tabulated result\ncompared.save_report("<PATH_TO_SAVE_REPORT>")\n```\n## Use Cases\nThisis particularly useful (not exhaustive) in the following scenarios:\n\n- Testing: Quickly identify and verify differences between expected and actual data frames during testing phases.\n\n- Analysis: Gain insights into the variations and discrepancies between two datasets, facilitating thorough data analysis.\n\n## Roadmap\n- Add other distance functions\n- Add seamless integration with pytest\n- Write a user guide\n\n## License\nCopyright (c) 2023 Kumar Shantanu\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n\n',
    'author': 'Kumar Shantanu',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.8',
}


setup(**setup_kwargs)
