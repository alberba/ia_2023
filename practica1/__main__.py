import sys
sys.path.append("c:\\Albert\\ia_2023")

from practica1 import agent, joc
from practica1.agent_profunditat import AgentProfunditat


def main():
    quatre = joc.Taulell([AgentProfunditat("Hola")])
    quatre.comencar()


if __name__ == "__main__":
    main()