import osmnx as ox
import matplotlib.pyplot as plt
import os

def load_or_download_map(place_name="Alexanderplatz, Berlin, Germany", dist=1000, network_type="drive"):
    """
    Downloads the OSM map of the given place if not saved locally, otherwise loads it.
    dist specifies the radius in meters from the center of the place.
    """
    filepath = "data/berlin_map.graphml"
    
    # Check if we have already downloaded the map to save time/API calls
    if os.path.exists(filepath):
        print(f"Loading map from {filepath}...")
        G = ox.load_graphml(filepath)
    else:
        print(f"Downloading map for {place_name} with {dist}m radius...")
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Download the graph from OpenStreetMap
        G = ox.graph_from_address(place_name, dist=dist, network_type=network_type)
        
        # Save to disk
        print(f"Saving map to {filepath}...")
        ox.save_graphml(G, filepath)
        
    return G

def show_map(G):
    """
    Visualizes the graph using osmnx/matplotlib.
    """
    print("Plotting the map...")
    fig, ax = ox.plot_graph(G, show=False, close=False, edge_color="w", edge_linewidth=0.5, node_color="r", node_size=2)
    plt.title("Berlin Autonomous Map - Alexanderplatz")
    os.makedirs("data", exist_ok=True)
    plt.savefig("data/berlin_map.png", dpi=300, bbox_inches="tight")
    print("Map saved to data/berlin_map.png")
    plt.close()

if __name__ == "__main__":
    # 1. Provide the place we want to map
    location = "Alexanderplatz, Berlin, Germany"
    
    # 2. Map loading/downloading
    G = load_or_download_map(place_name=location, dist=1500)
    
    # 3. Print information
    print(f"Graph nodes: {len(G.nodes)}")
    print(f"Graph edges: {len(G.edges)}")
    
    # 4. View map
    show_map(G)
