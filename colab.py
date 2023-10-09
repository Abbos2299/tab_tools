import subprocess

# Replace the URL with the Google Colab notebook URL you want to run
colab_url = "https://colab.research.google.com/drive/1cn2kF1dbXoHmFpEIS4Rd9nc-YiX0EU4V#scrollTo=JcTwIBkcaveT"

# Command to download and execute the Colab notebook
command = f"jupyter nbconvert --to notebook --execute {colab_url} --output executed_notebook.ipynb"

# Run the command
subprocess.run(command, shell=True)
