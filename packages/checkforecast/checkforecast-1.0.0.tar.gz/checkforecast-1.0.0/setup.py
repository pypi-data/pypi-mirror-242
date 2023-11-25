from setuptools import setup


setup(
  name = 'checkforecast',         #* Your package will have this name
  packages = ['checkforecast'],   #* Name the package again
  version = '1.0.0',         #* To be increased every time your change your library
  license='MIT',             # Type of license. More here: https://help.github.com/articles/licensing-a-repository
  description = 'This package is used to check weather data from an api openweather',    # Short description of your library
  author = 'Joywin Gonsalves',                   # Your name
  author_email = 'joywin16us@gmail.com',  # Your email
  url = 'https://github.com/thedowntownboy/weather_forecast_Library.git',              # Homepage of your library (e.g. github or your website)
  keywords = ['weather', 'forecast', 'checkforecast'],   # Keywords users can search on pypi.org
  install_requires=['requests', ],                 # Other 3rd-party libs that pip needs to install
  classifiers=[
    'Development Status :: 3 - Alpha',          # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',          # Who is the audience for your library?
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Type a license again
    'Programming Language :: Python :: 3.8',      # Python versions that your library supports
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
  ],
)
