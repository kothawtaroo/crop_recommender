import os
import matplotlib
matplotlib.use('Agg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt
from sklearn import tree
import joblib
from django.conf import settings
import numpy as np

def get_node_explanation(feature_name, threshold, class_names, samples, value):
    """Generate a human-readable explanation for a decision tree node."""
    if feature_name:
        # Decision node
        total_samples = np.sum(samples)
        class_distribution = [f"{class_names[i]}: {count}" for i, count in enumerate(value[0]) if count > 0]
        return (f"Decision: Is {feature_name} ≤ {threshold:.2f}?\n"
                f"Total Samples: {total_samples}\n"
                f"Class Distribution:\n{', '.join(class_distribution)}")
    else:
        # Leaf node
        majority_class = class_names[np.argmax(value[0])]
        total_samples = np.sum(samples)
        return (f"Prediction: {majority_class}\n"
               f"Total Samples: {total_samples}")

def generate_tree_visualization():
    try:
        # Define paths
        base_dir = settings.BASE_DIR
        static_dir = os.path.join(base_dir, 'static', 'recommender', 'images')
        model_path = os.path.join(base_dir, 'recommender', 'ml_model', 'crop_model.joblib')
        
        print(f"Base directory: {base_dir}")
        print(f"Static directory: {static_dir}")
        print(f"Model path: {model_path}")
        
        # Create the static directory if it doesn't exist
        os.makedirs(static_dir, exist_ok=True)
        
        # Verify model exists
        if not os.path.exists(model_path):
            print(f"Model file not found at: {model_path}")
            return False
            
        # Load the model
        model = joblib.load(model_path)
        
        # Get tree structure
        n_nodes = model.tree_.node_count
        feature = model.tree_.feature
        threshold = model.tree_.threshold
        values = model.tree_.value
        samples = model.tree_.n_node_samples
        
        feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        
        def create_visualization():
            # Create figure
            fig, ax = plt.subplots(figsize=(25, 15))
            
            # Plot the tree
            tree.plot_tree(model, 
                          feature_names=feature_names,
                          class_names=model.classes_, 
                          filled=True, 
                          rounded=True,
                          fontsize=10,
                          ax=ax)
            
            # Add title
            ax.set_title('Crop Recommendation Decision Tree\nWith Feature Explanations', 
                        fontsize=16, pad=20)
            
            # Add legend explaining the colors
            legend_elements = [plt.Rectangle((0,0),1,1, fc=plt.cm.RdYlBu(float(i)/len(model.classes_)),
                                           label=class_name)
                             for i, class_name in enumerate(model.classes_)]
            ax.legend(handles=legend_elements, loc='upper right', 
                     title='Crop Types', bbox_to_anchor=(1.2, 1))
            
            # Get the text annotations (node labels)
            texts = ax.get_children()
            annotations = [t for t in texts if isinstance(t, plt.Text)]
            
            # Add explanations next to each node
            for i, node_text in enumerate(annotations):
                if i < n_nodes:  # Only process actual nodes
                    # Get node position from the existing text
                    pos = node_text.get_position()
                    
                    # Generate explanation text
                    if feature[i] != -2:  # Not a leaf node
                        feature_name = feature_names[feature[i]]
                        explanation = get_node_explanation(feature_name, threshold[i], 
                                                        model.classes_, samples[i], values[i])
                    else:  # Leaf node
                        explanation = get_node_explanation(None, None, 
                                                        model.classes_, samples[i], values[i])
                    
                    # Add explanation text
                    ax.annotate(explanation,
                               xy=pos,
                               xytext=(pos[0] - 0.2, pos[1]),
                               bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.8),
                               fontsize=8,
                               ha='right')
            
            return fig
        
        # Create and save visualization
        fig = create_visualization()
        output_path = os.path.join(static_dir, 'decision_tree.png')
        print(f"Saving visualization to: {output_path}")
        fig.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0.5)
        plt.close(fig)
        
        # Also save to staticfiles if it exists
        staticfiles_path = os.path.join(settings.STATIC_ROOT, 'recommender', 'images', 'decision_tree.png')
        if settings.STATIC_ROOT:
            os.makedirs(os.path.dirname(staticfiles_path), exist_ok=True)
            fig = create_visualization()
            fig.savefig(staticfiles_path, dpi=300, bbox_inches='tight', pad_inches=0.5)
            plt.close(fig)
            print(f"Also saved to staticfiles: {staticfiles_path}")
        
        # Verify the files were created
        if os.path.exists(output_path) or os.path.exists(staticfiles_path):
            print("Visualization file(s) created successfully")
            return True
        else:
            print("Visualization files were not created")
            return False
            
    except Exception as e:
        print(f"Error generating visualization: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False
