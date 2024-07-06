from setuptools import find_packages , setup 
from typing import List

remove_e = "-e ."
def get_requirements(filename:str) -> List[str] :
    requirements = [] 
    with open(filename) as file :
        requirements = file.readlines()
        requirements = [i.replace("\n" , "") for i in requirements]

        if remove_e in requirements :
            requirements.remove(remove_e)

    return requirements

setup (
    name = "RegressionProject" ,
    version='0.0.1',
    author='Maahi',
    author_email='mahendragharad5@gmail.com',
    install_requires = get_requirements('requirements.txt'),
    packages=find_packages()
)

print(get_requirements("requirements.txt"))