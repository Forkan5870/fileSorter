# fileSorter


This Python script sorts PDF files in a directory into folders based on the content of their first two pages. It utilizes the PyPDF2 library to extract text from the PDF files and the Ollama library to analyze the text and classify it into categories. The categories are defined by the user in a `data.json` file within each category folder. The script uses the `phi3` model by default, but it can be easily switched to other models available in the [Ollama library](https://ollama.com/library). All models run locally on the user's machine, ensuring that no data is sent to the cloud or shared with third parties.

## Usage

This script requires Ollama to be installed on your system. It uses the `phi3` model by default. A short installation guide is provided at the end of this README.

### 1. Clone the Repository

```bash
git clone <repository-url>
```

### 2. Install the Required Libraries

```bash
pip install  langchain  PyPDF2
```

### 3. Set the Directory Path

Enter the path of the directory you want to sort in the `path` variable in the `fileSorter.py` script.

### 4. Create the Appropriate Folder Structure

Organize your directory as follows:

```plaintext
train
│
├── trained.json (optional)
│
├── category1_name
│ └── example_any_name.pdf
│
├── category2_name
│ └── any_name_example.pdf
│
└── ...
input
├── input1.pdf
├── input2.pdf
└── ...
output
└── (empty)
```

- **train**: This directory contains training data for categorizing PDFs.
  - **trained.json** (optional): This file includes a hash map with key-value pairs where the key is a category and the value is a sample text that matches this category. If this file is not provided, it will be created from the content in the **train** folder. Example format:
    ```json
    {
        "Category": "Some text that matches this category",
        "Another Category": "Different text matching this category"
    }
    ```
  - **category1_name**, **category2_name**, ...: These folders contain example PDF files that correspond to different categories.
    - Example: `category1_name/example_any_name.pdf`
    - Example: `category2_name/any_name_example.pdf`

- **input**: This folder contains the PDF files that need to be sorted.
  - Example: `input1.pdf`
  - Example: `input2.pdf`

- **output**: This folder will be used to store the sorted PDFs. It can initially be empty, as the necessary folders will be created automatically during the sorting process.
  
### 5. Run the script

```bash
python fileSorter.py
```

## Installation of Ollama (for Windows)

<details>
  <summary>Click to expand</summary>
  
  The installation requires the following repositories:

  - [LangChain](https://github.com/langchain-ai/langchain)
  - [Ollama](https://github.com/ollama/ollama)

  First, install Ollama from [Ollama's website](https://ollama.com/).

  Then, add an environment variable named `Path` with the route `C:\Users\<user_name>\AppData\Local\Programs\Ollama`. Replace `<user_name>` with your actual Windows username.

  1. Press `Win + X` to open the Quick Access Menu.
  2. Select **System** from the menu. This will open the **About** page in the Settings app.
  3. Click on **Advanced system settings** on the right-hand side. This will open the **System Properties** window.
  4. In the **System Properties** window, click on the **Environment Variables** button at the bottom right.
  5. In the **Environment Variables** window, look for the **User variables** section at the top.
  6. Click on the **New** button under the **User variables** section.
  7. In the **New User Variable** dialog box, enter the following:
     - **Variable name:** `Path`
     - **Variable value:** `C:\Users\<user_name>\AppData\Local\Programs\Ollama`
  8. Click **OK** to save the new variable.
  9. Click **OK** again in the **Environment Variables** window to apply the changes.
  10. Click **OK** in the **System Properties** window to close it.

  Now open cmd and type `ollama pull <model>` to download the desired model. This script uses the `phi3` model, but other models can be implemented.

  Note: You can test the installation by typing `ollama run <model>` in the cmd. You can also test the model in Python by running `main.py`.

</details>