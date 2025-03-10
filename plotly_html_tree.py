import plotly.graph_objects as go
from bs4 import BeautifulSoup
import networkx as nx
import requests
from urllib.parse import urlparse
import random

class HTMLTreeVisualizer:
    def __init__(self):
        self.G = nx.Graph()
        self.pos = {}
        self.node_colors = {}
        self.node_sizes = {}
        self.edge_traces = []
        self.node_traces = []
        
    def get_html_content(self, url_or_file):
        """Get HTML content from URL or local file"""
        try:
            if urlparse(url_or_file).scheme:
                # It's a URL
                response = requests.get(url_or_file)
                return response.text
            else:
                # It's a local file
                with open(url_or_file, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            print(f"Error getting HTML content: {e}")
            return None

    def create_tree(self, html_content):
        """Create a tree structure from HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        self.G.clear()
        self.pos.clear()
        self.node_colors.clear()
        self.node_sizes.clear()
        
        def add_node(element, parent_id=None, level=0, position=0):
            node_id = len(self.G.nodes)
            node_name = element.name if element.name else 'text'
            
            # Add node attributes
            attrs = {}
            if element.attrs:
                attrs = {k: v for k, v in element.attrs.items()}
            
            # Add node to graph
            self.G.add_node(node_id, 
                           name=node_name,
                           level=level,
                           attrs=attrs,
                           text=element.string if element.string else '')
            
            # Calculate position
            self.pos[node_id] = (position, -level)
            
            # Set node color based on tag type
            if element.name in ['div', 'section']:
                self.node_colors[node_id] = '#1f77b4'  # blue
            elif element.name in ['p', 'span', 'text']:
                self.node_colors[node_id] = '#2ca02c'  # green
            elif element.name in ['a', 'button']:
                self.node_colors[node_id] = '#ff7f0e'  # orange
            elif element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                self.node_colors[node_id] = '#d62728'  # red
            else:
                self.node_colors[node_id] = '#7f7f7f'  # gray
            
            # Set node size based on importance
            if element.name in ['html', 'body', 'head']:
                self.node_sizes[node_id] = 20
            elif element.name in ['div', 'section']:
                self.node_sizes[node_id] = 15
            else:
                self.node_sizes[node_id] = 10
            
            # Add edge to parent
            if parent_id is not None:
                self.G.add_edge(parent_id, node_id)
            
            # Process children
            children = list(element.children)
            non_empty_children = [child for child in children if str(child).strip()]
            
            for i, child in enumerate(non_empty_children):
                if isinstance(child, str):
                    if child.strip():
                        # Add text node
                        text_id = len(self.G.nodes)
                        self.G.add_node(text_id, 
                                      name='text',
                                      level=level + 1,
                                      attrs={},
                                      text=child.strip())
                        self.pos[text_id] = (position + i, -(level + 1))
                        self.node_colors[text_id] = '#2ca02c'  # green
                        self.node_sizes[text_id] = 8
                        self.G.add_edge(node_id, text_id)
                else:
                    # Recursively add child elements
                    add_node(child, node_id, level + 1, position + i)
            
            return node_id
        
        add_node(soup)

    def create_edge_traces(self):
        """Create edge traces for plotting"""
        self.edge_traces = []
        
        # Create edges
        edge_x = []
        edge_y = []
        
        for edge in self.G.edges():
            x0, y0 = self.pos[edge[0]]
            x1, y1 = self.pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')
            
        self.edge_traces.append(edge_trace)

    def create_node_traces(self):
        """Create node traces for plotting"""
        self.node_traces = []
        
        # Create nodes
        node_x = []
        node_y = []
        node_colors = []
        node_sizes = []
        node_text = []
        
        for node in self.G.nodes():
            x, y = self.pos[node]
            node_x.append(x)
            node_y.append(y)
            node_colors.append(self.node_colors[node])
            node_sizes.append(self.node_sizes[node])
            
            # Create hover text
            node_info = self.G.nodes[node]
            hover_text = f"Tag: {node_info['name']}<br>"
            if node_info['attrs']:
                hover_text += f"Attributes: {node_info['attrs']}<br>"
            if node_info['text']:
                hover_text += f"Text: {node_info['text']}"
            node_text.append(hover_text)
            
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=False,
                color=node_colors,
                size=node_sizes,
                line_width=2))
            
        node_trace.text = node_text
        self.node_traces.append(node_trace)

    def plot(self, title="HTML Tree Visualization"):
        """Create and show the plot"""
        self.create_edge_traces()
        self.create_node_traces()
        
        # Create figure
        fig = go.Figure(data=self.edge_traces + self.node_traces,
                       layout=go.Layout(
                           title=title,
                           titlefont_size=16,
                           showlegend=False,
                           hovermode='closest',
                           margin=dict(b=20,l=5,r=5,t=40),
                           xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                           yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                           )
        
        return fig

def visualize_html(url_or_file, output_file=None):
    """Main function to visualize HTML structure"""
    visualizer = HTMLTreeVisualizer()
    
    # Get HTML content
    html_content = visualizer.get_html_content(url_or_file)
    if not html_content:
        return None
    
    # Create tree and plot
    visualizer.create_tree(html_content)
    fig = visualizer.plot(f"HTML Tree Structure - {url_or_file}")
    
    # Save or show plot
    if output_file:
        fig.write_html(output_file)
        print(f"Plot saved to {output_file}")
    else:
        fig.show()
    
    return fig

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python plotly_html_tree.py <url_or_file> [output_file]")
        sys.exit(1)
    
    url_or_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    visualize_html(url_or_file, output_file) 