# User Behavior Anomaly Detection

This project provides a system for generating synthetic user activity logs and detecting anomalous behavior using an Isolation Forest machine learning model.

---

## Prerequisites

Before running the project, ensure you have **Python 3** installed on your Linux system.

### Setting Up the Virtual Environment

To keep your project dependencies isolated, follow these steps to set up a virtual environment (`venv`):

1. **Install the venv package** (if not already installed):
```bash
sudo apt update
sudo apt install python3-venv

```



```
2.  **Create the virtual environment**:
    ```bash
    python3 -m venv myenv

```

3. **Activate the environment**:
```bash
source myenv/bin/activate

```



```
    *Your terminal prompt should now show `(myenv)`.*

4.  **Install required dependencies**:
    ```bash
pip install pandas numpy scikit-learn

```

---

## Project Structure

* **`dataset.py`**: A script that generates a synthetic dataset of user activities (including high-risk behaviors) and saves them to `user_behavior_dataset.csv`.


* **`anomaly.py`**: The core detection script that loads the data, preprocesses it, runs an `IsolationForest` model to detect anomalies, and performs secondary rule-based validation.



---

## Usage

### 1. Generate the Data

Run the dataset generator to create `user_behavior_dataset.csv`:

```bash
python3 dataset.py

```

### 2. Detect Anomalies

Run the detection pipeline to identify and validate suspicious users:

```bash
python3 anomaly.py

```

---

## How it Works

* **Feature Engineering**: The script processes raw logs by grouping user activities and calculating features like hour-of-day statistics and total high-risk activity counts.


* **Isolation Forest**: The model uses a contamination rate (default `0.01`) to identify users whose behavioral patterns deviate significantly from the norm.


* **Secondary Validation**: After initial detection, a secondary rule-based filter checks if the flagged users have performed more than one high-risk activity, reducing the rate of false positives.



---

## Deactivation

When you are finished working on the project, you can exit the virtual environment by running:

```bash
deactivate

```

---

