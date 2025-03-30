import tkinter as tk
import time


# Node class for AVL Tree
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key
        self.height = 1  # For AVL balancing

# AVL Tree with Stepwise Deletion & Message Box
class AVL:
    def __init__(self, visualizer):
        self.root = None
        self.visualizer = visualizer  # GUI reference for visualization

    def insert(self, key):
        self.visualizer.update_message(f"Inserting {key} into the tree...")
        self.visualizer.draw_node(key)
        self.root = self._insert(self.root, key)
        self.visualizer.update_message(f"{key} inserted successfully!")
        self.visualizer.draw_tree()

    def _insert(self, root, key):
        if not root:
            return Node(key)

        self.visualizer.highlight_node(root, "yellow")
        self.visualizer.master.update()
        # time.sleep(2)  # Pause to visualize step

        if key == root.val:
            self.visualizer.update_message(f"{key} already exists")
            time.sleep(2)
            return root
        if key < root.val:
            self.visualizer.update_message(f"Comparing with {root.val}, {key} < {root.val} , inserting on left")
            time.sleep(2)
            root.left = self._insert(root.left, key)
        else:
            self.visualizer.update_message(f"Comparing with {root.val}, {key} > {root.val} , inserting on right")
            time.sleep(2)
            root.right = self._insert(root.right, key)

        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))

        self.visualizer.draw_tree()
        root = self._balance(root)
        self.visualizer.draw_tree()

        return root

    def delete(self, key):
        self.visualizer.update_message(f"Deleting {key}...")
        self.root = self._delete(self.root, key)
        self.visualizer.update_message(f"{key} deleted successfully (if it existed).")
        self.visualizer.draw_tree()

    def _delete(self, root, key):
        if not root:
            self.visualizer.update_message(f"Did not Find {key} for deletion...")
            time.sleep(2)
            return root

        self.visualizer.highlight_node(root, "yellow")
        self.visualizer.master.update()
        # time.sleep(2)

        if key < root.val:
            self.visualizer.update_message(f"Comparing with {root.val}, {key} < {root.val} , searching on left")
            time.sleep(2)
            root.left = self._delete(root.left, key)
            
        elif key > root.val:
            self.visualizer.update_message(f"Comparing with {root.val}, {key} > {root.val} , searching on right")
            time.sleep(2)
            root.right = self._delete(root.right, key)
        else:
            self.visualizer.update_message(f"Found {key}, deleting...")
            time.sleep(2)
            if not root.left:
                return root.right
            elif not root.right:
                return root.left

            min_larger_node = self._min_value_node(root.right)
            self.visualizer.update_message(f"Replacing {key} with {min_larger_node.val}.")
            time.sleep(2)
            
            root.val = min_larger_node.val
            root.right = self._delete(root.right, min_larger_node.val)

        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))
        return self._balance(root)

    def _min_value_node(self, root):
        current = root
        while current.left:
            self.visualizer.highlight_node(current, "yellow")
            self.visualizer.master.update()
            time.sleep(2)
            current = current.left
        return current

    def _get_height(self, node):
        return node.height if node else 0

    def _balance_factor(self, node):
        return self._get_height(node.left) - self._get_height(node.right)

    def _balance(self, root):
        balance = self._balance_factor(root)

        if balance > 1:
            if self._balance_factor(root.left) < 0:
                self.visualizer.update_message("Performing Left Rotation (LR case)")
                time.sleep(0.9)
                root.left = self._rotate_left(root.left)
            self.visualizer.update_message("Performing Right Rotation (LL case)")
            time.sleep(0.9)
            return self._rotate_right(root)

        if balance < -1:
            if self._balance_factor(root.right) > 0:
                self.visualizer.update_message("Performing Right Rotation (RL case)")
                time.sleep(0.9)
                root.right = self._rotate_right(root.right)
            self.visualizer.update_message("Performing Left Rotation (RR case)")
            time.sleep(0.9)
            return self._rotate_left(root)

        return root

    def _rotate_left(self, z):
        y = z.right
        x = y.left  # This is the third node involved in rotation

        # Show rotation in a new window
        self._show_avl_rotation(z, y, x, "Left Rotation")

        z.right = y.left
        y.left = z

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        
        return y

    def _rotate_right(self, z):
        y = z.left
        x = y.right  # This is the third node involved in rotation

        # Show rotation in a new window
        self._show_avl_rotation(z, y, x, "Right Rotation")

        z.left = y.right
        y.right = z

        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        
        return y

    def _show_avl_rotation(self, old_root, new_root, third_node, rotation_type):
        rotation_window = tk.Toplevel(self.visualizer.master)
        rotation_window.title(rotation_type)
        rotation_canvas = tk.Canvas(rotation_window, width=400, height=300, bg="white")
        rotation_canvas.pack()

        rotation_canvas.create_text(200, 20, text=rotation_type, font=("Arial", 14, "bold"), fill="red")

        # Initial state (Before rotation)
        rotation_canvas.create_oval(180, 60, 220, 100, fill="lightblue")
        rotation_canvas.create_text(200, 80, text=str(old_root.val), font=("Arial", 12, "bold"))

        if "Left" in rotation_type:
            rotation_canvas.create_oval(260, 130, 300, 170, fill="lightblue")  # Right child (new root)
            rotation_canvas.create_text(280, 150, text=str(new_root.val), font=("Arial", 12, "bold"))
            if third_node:
                rotation_canvas.create_oval(200, 200, 240, 240, fill="lightgray")  # Third node
                rotation_canvas.create_text(220, 220, text=str(third_node.val), font=("Arial", 12, "bold"))
        else:
            rotation_canvas.create_oval(100, 130, 140, 170, fill="lightblue")  # Left child (new root)
            rotation_canvas.create_text(120, 150, text=str(new_root.val), font=("Arial", 12, "bold"))
            if third_node:
                rotation_canvas.create_oval(160, 200, 200, 240, fill="lightgray")  # Third node
                rotation_canvas.create_text(180, 220, text=str(third_node.val), font=("Arial", 12, "bold"))

        rotation_canvas.create_text(200, 250, text="Rotating...", font=("Arial", 12, "bold"), fill="black")

        rotation_canvas.update()
        time.sleep(1.5)

        # After rotation
        rotation_canvas.delete("all")

        rotation_canvas.create_text(200, 20, text="After " + rotation_type, font=("Arial", 14, "bold"), fill="red")

        rotation_canvas.create_oval(180, 60, 220, 100, fill="lightgreen")  # New root
        rotation_canvas.create_text(200, 80, text=str(new_root.val), font=("Arial", 12, "bold"))

        if "Left" in rotation_type:
            rotation_canvas.create_oval(100, 130, 140, 170, fill="lightblue")  # Left child (old root)
            rotation_canvas.create_text(120, 150, text=str(old_root.val), font=("Arial", 12, "bold"))
            if third_node:
                rotation_canvas.create_oval(260, 200, 300, 240, fill="lightgray")  # Third node
                rotation_canvas.create_text(280, 220, text=str(third_node.val), font=("Arial", 12, "bold"))
        else:
            rotation_canvas.create_oval(260, 130, 300, 170, fill="lightblue")  # Right child (old root)
            rotation_canvas.create_text(280, 150, text=str(old_root.val), font=("Arial", 12, "bold"))
            if third_node:
                rotation_canvas.create_oval(140, 200, 180, 240, fill="lightgray")  # Third node
                rotation_canvas.create_text(160, 220, text=str(third_node.val), font=("Arial", 12, "bold"))

        rotation_canvas.update()
        time.sleep(1.5)

        rotation_window.destroy()


# GUI Class using Tkinter
class AVLVisualizer:
    def __init__(self, master):
        self.master = master
        self.master.title("AVL Tree Visualizer")

        self.avl = AVL(self)

        self.canvas = tk.Canvas(master, width=500, height=350, bg="white")
        self.canvas.pack()

        self.entry = tk.Entry(master)
        self.entry.pack()

        self.insert_button = tk.Button(master, text="Insert", command=self.insert_value)
        self.insert_button.pack()

        self.delete_button = tk.Button(master, text="Delete", command=self.delete_value)
        self.delete_button.pack()

        self.message_label = tk.Label(master, text="Welcome!", fg="blue")
        self.message_label.pack()

        self.draw_tree()

    def insert_value(self):
        value = self.entry.get()
        if value.isnumeric():
            self.avl.insert(int(value))
            self.entry.delete(0, tk.END)

    def delete_value(self):
        value = self.entry.get()
        if value.isnumeric():
            self.avl.delete(int(value))
            self.entry.delete(0, tk.END)

    def draw_node(self,key):
        self.canvas.create_oval(20 - 15, 20 - 15, 20 + 15, 20 + 15, fill="lightblue", tags=f"node_{key}")
        self.canvas.create_text(20, 20, text=str(key), font=("Arial", 12, "bold"))
        time.sleep(2)

    def draw_tree(self):
        self.canvas.delete("all")
        self._draw_tree(self.avl.root, 250, 50, 120)

    def _draw_tree(self, node, x, y, dx):
        if node:
            balance_factor = self.avl._balance_factor(node)  # Get balance factor
            
            # Draw node
            self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="lightblue", tags=f"node_{node.val}")
            self.canvas.create_text(x, y, text=str(node.val), font=("Arial", 12, "bold"))
            
            # Draw balance factor on the top-right of the node
            self.canvas.create_text(x + 20, y - 20, text=str(balance_factor), font=("Arial", 10, "bold"), fill="red")
            
            # Draw left and right connections
            if node.left:
                self.canvas.create_line(x - 10, y + 10, x - dx + 10, y + 50, fill="black")
                self._draw_tree(node.left, x - dx, y + 50, dx // 2)

            if node.right:
                self.canvas.create_line(x + 10, y + 10, x + dx - 10, y + 50, fill="black")
                self._draw_tree(node.right, x + dx, y + 50, dx // 2)


    def highlight_node(self, node, color):
        if node:
            self.canvas.itemconfig(f"node_{node.val}", fill=color)
            self.master.update()

    def update_message(self, text):
        self.message_label.config(text=text)
        self.master.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = AVLVisualizer(root)
    root.mainloop()
