from mechvibes.impl.constants import PLATFORM
from mechvibes.impl.core import App

app = App()

if __name__ == "__main__":
    app.run(platform=PLATFORM)
else:
    print("Warning: This file is not meant to be imported!")
