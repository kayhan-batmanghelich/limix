from setuptools import setup

if __name__ == "__main__":
    console_scripts = ["limix = limix:cli"]
    setup(entry_points=dict(console_scripts=console_scripts))
