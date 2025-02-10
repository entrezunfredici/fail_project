#========================================================================
# This python script created by frederic Macabiau can to help you to create and update your api
# for launch this script you need to have npm, python3.10 and pip installed
# to run the script in Linux or MacOS you can run the following command
# python3.10 api-manager-script.py
# or in windows you can run the following command
# py -3 api_manager_script.py
#========================================================================
#libraries
import os
import subprocess
import json
import pickle
import shutil

try:
    from dotenv import load_dotenv, set_key
except:
    try:
        os.system("pip install python-dotenv")
    except:
        os.system("python.exe -m pip install --upgrade pip")
        os.system("pip install python-dotenv")
    from dotenv import load_dotenv, set_key

print("========================================================================")
print("Welcome to API manager script")

datas = {
    "API_PORT": 8000
}

default_folder_name = "default_microservice"

commands = {
    "get_default_api": "git clone https://github.com/entrezunfredici/default_microservice.git",
    "update_api": "npm i",
    "start_api": "npm run start"
}

files = {
    "data": "datas.pkl",
    "env": ".env",
    "package": "package.json"
}

folder_name = input("What is the name of your API ⇒ ")

def remove_folder(folder_path, folder):
    git_folder = os.path.join(folder_path, folder)
    if os.path.isdir(git_folder):
        try:
            # Supprime les attributs cachés, système et lecture seule
            for root, dirs, files in os.walk(git_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.chmod(file_path, 0o777)  # Donne les permissions complètes
            shutil.rmtree(git_folder)
            print(f"Le dossier caché {git_folder} a été supprimé avec succès.")
        except Exception as e:
            print(f"Erreur lors de la suppression de {git_folder}: {e}")
    else:
        print(f"Le dossier {git_folder} n'existe pas.")

def launch_other_scripts(script_path, script_name):
    try:
        os.chdir(script_path)
        subprocess.run(["python", script_name], check=True)
        print(f"run {script_name}")
    except subprocess.CalledProcessError as e:
        print(f"fail to run {script_name}: {e}")

try:
    if not os.path.exists(folder_name):
        if not os.path.exists(files["data"]):
            # Create and write initial data to the file
            with open(files["data"], "wb") as f:
                pickle.dump(datas, f)
        else:
            # Read existing data, modify and save it back
            with open(files["data"], "rb") as f:
                datas = pickle.load(f)
                datas["API_PORT"] += 1  # Modify the value
            with open(files["data"], "wb") as f:
                pickle.dump(datas, f)
        subprocess.run(commands["get_default_api"], shell=True, text=True)
        # Check if the folder already exists before renaming
        if not os.path.exists(folder_name):
            os.rename(default_folder_name, folder_name)
        os.chdir(folder_name)
        
        # Modify the package.json file
        with open(files["package"], "r", encoding="utf-8") as f:
            data = json.load(f)
        data["name"] = folder_name
        with open(files["package"], "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # Load .env file and set the keys
        file_env = files["env"]
        load_dotenv(file_env)

        for key, value in datas.items():
            print(f"Setting {key} = {value} in .env file")
            set_key(file_env, key, str(value))
        remove_folder("./", ".git")

    else:
        os.chdir(folder_name)

    print(f"Folder {os.getcwd()} opened")
    subprocess.run(commands["update_api"], shell=True, text=True)

except Exception as e:
    print(f"ERROR={e}")
print("========================================================================")