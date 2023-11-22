from setuptools import setup, find_packages

setup(
    name='yctmodel',
    version='2.1.1',
    packages=['yctmodel'],
    description="ModelSelector automates ensemble pipeline creation with optimized hyperparameters for superior predictions. Use start() for ensemble selection and get_pipeline() to retrieve the generated pipeline. Fine-tune existing pipelines with specific models using auto_tuning(). Streamline model selection and hyperparameter tuning with ModelSelector.",
    install_requires=['scikit-learn','pandas','matplotlib',
                        'numpy','scipy','seaborn','xgboost',],
    url='https://github.com/gems-yc4923/thames.git',
    license='MIT',
    author='yc4923'
)