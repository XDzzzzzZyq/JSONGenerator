from UI.UI import Panel
from utils import *

def main():
    panel = Panel(960, 1080)
    generator = JSONGenerator()
    panel.set_generator_instance(generator)
    panel.run()

if __name__ == "__main__":
    main()
    
