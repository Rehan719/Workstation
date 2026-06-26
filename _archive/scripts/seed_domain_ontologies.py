import networkx as nx
import json
import os

DOMAINS = ["religion", "science", "law", "employment", "education", "care"]

def seed_ontologies():
    os.makedirs("agentic_core/data/ontologies", exist_ok=True)

    for domain in DOMAINS:
        G = nx.DiGraph()
        root = f"{domain.capitalize()} Ontology Core"
        G.add_node(root, type="root", level=0)

        pillars = [f"{domain.capitalize()} Pillar {i}" for i in range(1, 6)]
        for pillar in pillars:
            G.add_edge(root, pillar, relation="contains")
            G.add_node(pillar, type="pillar", level=1)

            for j in range(1, 10):
                concept = f"{pillar} - Concept {j}"
                G.add_edge(pillar, concept, relation="defines")
                G.add_node(concept, type="concept", level=2)

                for k in range(1, 3):
                    attribute = f"{concept} - Attribute {k}"
                    G.add_edge(concept, attribute, relation="has_attribute")
                    G.add_node(attribute, type="attribute", level=3)

        data = nx.node_link_data(G)
        with open(f"agentic_core/data/ontologies/{domain}.json", "w") as f:
            json.dump(data, f, indent=2)

        print(f"Seeded {domain} ontology with {G.number_of_nodes()} nodes.")

if __name__ == "__main__":
    seed_ontologies()
