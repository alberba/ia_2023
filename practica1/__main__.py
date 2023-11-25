# Autores: Sergi Oliver y Albert Salom


from practica1 import agent, joc
from practica1.agent_profunditat import AgentProfunditat
from practica1.agent_A import AgentA
from practica1.agent_minimax import AgentMinimax


def main():
    #quatre = joc.Taulell([AgentProfunditat("Jorge")])
    #quatre = joc.Taulell([AgentA("Jorge")])
    quatre = joc.Taulell([AgentMinimax("Albert"), AgentMinimax("Pau")])
    quatre.comencar()


if __name__ == "__main__":
    main()
