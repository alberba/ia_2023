import sys
sys.path.append("c:\\Albert\\ia_2023")

from monedes import agent, joc


def main():
    ag_mon = agent.AgentMoneda()
    joc_mon = joc.Moneda([ag_mon])
    joc_mon.comencar()


if __name__ == "__main__":
    main()